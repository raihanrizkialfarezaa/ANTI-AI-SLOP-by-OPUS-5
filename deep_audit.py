#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deep_audit.py : Audit lapis probabilitas token untuk ANTI_AI_SLOP_GUARD v4.0.

Alat ini turun ke lapisan arsitektur model bahasa, bukan lagi ke pola permukaan.
Dasar teorinya tiga:

1. Holtzman dkk. (2020), "The Curious Case of Neural Text Degeneration".
   Tulisan manusia tidak menempel pada jalur probabilitas tertinggi. Manusia
   berpindah-pindah antara kata terduga dan kata tak terduga. Keluaran model
   cenderung rata dan terduga.

2. Bao dkk. (2024), "Fast-DetectGPT" (arXiv:2310.05130).
   Conditional Probability Curvature. Teks mesin cenderung berada pada puncak
   lokal kurva probabilitas bersyarat, sehingga log-likelihood teks yang diamati
   mendekati atau melampaui nilai harapan log-likelihood menurut model itu
   sendiri. Skor d dihitung analitik tanpa sampling:

       d(x) = ( log p(x) - SUM_i E_{v~p_i}[log p_i(v)] )
              / sqrt( SUM_i Var_{v~p_i}[log p_i(v)] )

   Nilai d yang tinggi menandakan teks berada di wilayah datar dan terduga.

3. Meister dkk. (2021) via Shaib dkk. (2025), "Measuring AI Slop in Text".
   Uniform Information Density. Densitas informasi diukur melalui rerata dan
   koefisien variasi surprisal token. Rerata surprisal rendah disertai variasi
   rendah menandakan teks banyak kata sedikit isi.

KELUARAN YANG BERGUNA: peringkat kalimat paling "datar" pada naskah, yaitu
kalimat yang paling mendesak ditulis ulang. Alat ini tidak memvonis
kepengarangan. Alat ini menunjuk kalimat mana yang harus dikonkretkan.

PERINGATAN METODOLOGIS (wajib dibaca):
  - Skor ini dihitung dengan model penilai berbahasa Indonesia berukuran kecil.
    Fast-DetectGPT divalidasi untuk bahasa Inggris dengan model penilai yang
    sepadan. Angkanya di sini bersifat relatif, bukan absolut.
  - Gunakan hanya untuk membandingkan kalimat DI DALAM naskah Anda sendiri,
    atau naskah Anda terhadap tulisan lama Anda sendiri (mode --calibrate).
  - Jangan pernah melaporkan skor ini sebagai bukti kepengarangan kepada siapa
    pun. Nilai gunanya adalah menunjuk kalimat yang perlu diperbaiki.

Pemakaian:
    pip install torch transformers
    python deep_audit.py REVISI_BAB_1.md
    python deep_audit.py REVISI_BAB_1.md --model cahya/gpt2-small-indonesian-522M
    python deep_audit.py REVISI_BAB_1.md --topk 15 --json
    python deep_audit.py --calibrate tulisan_lama/*.md      # bangun garis dasar pribadi
    python deep_audit.py --selftest                          # uji matematika tanpa model
"""

import argparse
import glob
import json
import math
import re
import statistics
import sys
from pathlib import Path

MODEL_BAWAAN = "cahya/gpt2-small-indonesian-522M"
MODEL_ALTERNATIF = [
    "cahya/gpt2-small-indonesian-522M",
    "flax-community/gpt2-small-indonesian",
    "indonesian-nlp/gpt2",
    "gpt2",  # cadangan terakhir, kualitas untuk bahasa Indonesia rendah
]


# ---------------------------------------------------------------------------
# Pemuatan teks
# ---------------------------------------------------------------------------
def muat_prosa(path):
    teks = Path(path).read_text(encoding="utf-8", errors="replace")
    teks = re.sub(r"```.*?```", " ", teks, flags=re.DOTALL)
    baris = []
    for b in teks.split("\n"):
        s = b.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith(">"):
            continue
        s = re.sub(r"^([-*+]|\d+\.)\s+", "", s)
        s = re.sub(r"[*_`]", "", s)
        baris.append(s)
    return "\n".join(baris)


def kalimat_dari(prosa):
    hasil = []
    for paragraf in re.split(r"\n\s*\n", prosa):
        satu = re.sub(r"\s+", " ", paragraf).strip()
        if not satu:
            continue
        for k in re.split(r'(?<=[.!?])\s+(?=[A-Z"(])', satu):
            k = k.strip()
            if len(k.split()) >= 5:
                hasil.append(k)
    return hasil


# ---------------------------------------------------------------------------
# Inti matematika (dapat diuji tanpa model)
# ---------------------------------------------------------------------------
def curvature_dari_logprob(logprobs_teramati, mu_per_posisi, var_per_posisi):
    """Fast-DetectGPT conditional probability curvature, bentuk analitik.

    logprobs_teramati : log p(x_i | x_<i) untuk token yang benar-benar muncul
    mu_per_posisi     : E_{v~p_i}[log p_i(v)]  (negatif entropi)
    var_per_posisi    : Var_{v~p_i}[log p_i(v)]
    """
    if not logprobs_teramati:
        return float("nan")
    pembilang = sum(logprobs_teramati) - sum(mu_per_posisi)
    penyebut = math.sqrt(max(1e-12, sum(var_per_posisi)))
    return pembilang / penyebut


def statistik_surprisal(logprobs_teramati):
    """Surprisal dalam bit, beserta rerata dan koefisien variasi (UID)."""
    if not logprobs_teramati:
        return {}
    surprisal = [-lp / math.log(2) for lp in logprobs_teramati]
    rerata = statistics.fmean(surprisal)
    sd = statistics.pstdev(surprisal) if len(surprisal) > 1 else 0.0
    return {
        "rerata_surprisal_bit": round(rerata, 3),
        "sd_surprisal": round(sd, 3),
        "cv_surprisal": round(sd / rerata, 3) if rerata else 0.0,
        "n_token": len(surprisal),
    }


def selftest():
    """Uji matematika dengan distribusi buatan, tanpa mengunduh model apa pun."""
    print("SELFTEST deep_audit.py")
    print("-" * 60)

    # Kasus 1: teks "mesin" = selalu memilih token dengan probabilitas tertinggi.
    # log p teramati mendekati 0, sedangkan mu (harapan) jauh lebih rendah.
    logp_mesin = [-0.05] * 200
    mu = [-2.0] * 200
    var = [1.5] * 200
    d_mesin = curvature_dari_logprob(logp_mesin, mu, var)

    # Kasus 2: teks "manusia" = sering memilih token berprobabilitas rendah.
    logp_manusia = [-2.4 if i % 3 else -0.3 for i in range(200)]
    d_manusia = curvature_dari_logprob(logp_manusia, mu, var)

    print(f"  curvature d (pola mesin)   = {d_mesin:.3f}")
    print(f"  curvature d (pola manusia) = {d_manusia:.3f}")
    assert d_mesin > d_manusia, "arah skor curvature terbalik"

    s_mesin = statistik_surprisal(logp_mesin)
    s_manusia = statistik_surprisal(logp_manusia)
    print(f"  surprisal mesin   : rerata {s_mesin['rerata_surprisal_bit']} bit, "
          f"CV {s_mesin['cv_surprisal']}")
    print(f"  surprisal manusia : rerata {s_manusia['rerata_surprisal_bit']} bit, "
          f"CV {s_manusia['cv_surprisal']}")
    assert s_manusia["cv_surprisal"] > s_mesin["cv_surprisal"], "arah CV terbalik"

    print("-" * 60)
    print("LULUS. Rumus curvature dan surprisal berperilaku sesuai teori.")
    print("Jalankan tanpa --selftest (dan dengan torch + transformers terpasang)")
    print("untuk mengaudit naskah sungguhan.")
    return 0


# ---------------------------------------------------------------------------
# Penilaian dengan model
# ---------------------------------------------------------------------------
class Penilai:
    def __init__(self, nama_model, device=None):
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError:
            print("torch dan transformers belum terpasang.\n"
                  "  pip install torch transformers\n"
                  "Atau jalankan: python deep_audit.py --selftest", file=sys.stderr)
            raise SystemExit(2)
        self.torch = torch
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        print(f"[memuat {nama_model} pada {device}]", file=sys.stderr)
        self.tok = AutoTokenizer.from_pretrained(nama_model)
        self.model = AutoModelForCausalLM.from_pretrained(nama_model).to(device).eval()
        self.maks = getattr(self.model.config, "n_positions", 1024)

    def nilai(self, teks):
        """Kembalikan logprob teramati, mu, dan var per posisi."""
        torch = self.torch
        ids = self.tok(teks, return_tensors="pt", truncation=True,
                       max_length=self.maks).input_ids.to(self.device)
        if ids.shape[1] < 3:
            return [], [], []
        with torch.no_grad():
            logits = self.model(ids).logits[0, :-1].float()
        sasaran = ids[0, 1:]
        logprob = torch.log_softmax(logits, dim=-1)
        prob = logprob.exp()

        teramati = logprob.gather(-1, sasaran.unsqueeze(-1)).squeeze(-1)
        mu = (prob * logprob).sum(dim=-1)                       # E[log p]
        ex2 = (prob * logprob.pow(2)).sum(dim=-1)               # E[(log p)^2]
        var = (ex2 - mu.pow(2)).clamp(min=0)
        return (teramati.tolist(), mu.tolist(), var.tolist())

    def skor(self, teks):
        lp, mu, var = self.nilai(teks)
        if not lp:
            return None
        d = curvature_dari_logprob(lp, mu, var)
        s = statistik_surprisal(lp)
        # rasio token yang berada di antara 1 prediksi teratas model
        s["curvature_d"] = round(d, 3)
        return s

    def skor_prediktabilitas(self, teks, k=1):
        torch = self.torch
        ids = self.tok(teks, return_tensors="pt", truncation=True,
                       max_length=self.maks).input_ids.to(self.device)
        if ids.shape[1] < 3:
            return 0.0
        with torch.no_grad():
            logits = self.model(ids).logits[0, :-1]
        sasaran = ids[0, 1:]
        topk = logits.topk(k, dim=-1).indices
        cocok = (topk == sasaran.unsqueeze(-1)).any(dim=-1).float().mean().item()
        return round(cocok, 3)


# ---------------------------------------------------------------------------
# Laporan
# ---------------------------------------------------------------------------
def audit_berkas(path, penilai, topk):
    prosa = muat_prosa(path)
    kalimat = kalimat_dari(prosa)
    if not kalimat:
        return None

    dokumen = penilai.skor(prosa[:20000])
    top1 = penilai.skor_prediktabilitas(prosa[:20000], k=1)
    top10 = penilai.skor_prediktabilitas(prosa[:20000], k=10)

    baris = []
    for k in kalimat:
        s = penilai.skor(k)
        if s and s["n_token"] >= 8:
            baris.append({"kalimat": k, **s})
    baris.sort(key=lambda r: -r["curvature_d"])

    return {
        "berkas": str(path),
        "dokumen": dokumen,
        "prediktabilitas_top1": top1,
        "prediktabilitas_top10": top10,
        "jumlah_kalimat_dinilai": len(baris),
        "kalimat_paling_datar": baris[:topk],
        "kalimat_paling_manusiawi": baris[-5:][::-1],
    }


def cetak(hasil):
    garis = "=" * 78
    print(garis)
    print(f"AUDIT LAPIS PROBABILITAS : {Path(hasil['berkas']).name}")
    print(garis)
    d = hasil["dokumen"]
    print(f"Curvature d (dokumen)     : {d['curvature_d']}")
    print(f"Rerata surprisal          : {d['rerata_surprisal_bit']} bit")
    print(f"CV surprisal (UID)        : {d['cv_surprisal']}")
    print(f"Token tertebak peringkat 1: {int(hasil['prediktabilitas_top1']*100)}%")
    print(f"Token tertebak 10 besar   : {int(hasil['prediktabilitas_top10']*100)}%")
    print()
    print("Bacaan: curvature tinggi, surprisal rendah, dan CV rendah menandakan")
    print("prosa yang terlalu terduga. Itu wilayah yang paling perlu dikonkretkan.")
    print()
    print(f"--- {len(hasil['kalimat_paling_datar'])} KALIMAT PALING DATAR "
          f"(prioritas tulis ulang) ---")
    for i, r in enumerate(hasil["kalimat_paling_datar"], start=1):
        print(f"\n [{i}] d={r['curvature_d']:>6}  surprisal={r['rerata_surprisal_bit']:>5} bit  "
              f"CV={r['cv_surprisal']}")
        teks = r["kalimat"]
        print(f"     {teks[:300]}{'...' if len(teks) > 300 else ''}")
    print()
    print("--- KALIMAT PALING TIDAK TERDUGA (pertahankan, ini suara Anda) ---")
    for r in hasil["kalimat_paling_manusiawi"]:
        print(f"  d={r['curvature_d']:>6}  {r['kalimat'][:110]}")
    print()


def kalibrasi(paths, penilai):
    nilai_d, nilai_s, nilai_cv = [], [], []
    for p in paths:
        prosa = muat_prosa(p)
        s = penilai.skor(prosa[:20000])
        if not s:
            continue
        nilai_d.append(s["curvature_d"])
        nilai_s.append(s["rerata_surprisal_bit"])
        nilai_cv.append(s["cv_surprisal"])
        print(f"  {Path(p).name:<45} d={s['curvature_d']:>6}  "
              f"surprisal={s['rerata_surprisal_bit']:>5}  CV={s['cv_surprisal']}")
    if not nilai_d:
        print("tidak ada berkas yang dapat dinilai", file=sys.stderr)
        return 1
    print("\nGARIS DASAR PRIBADI (pakai ini sebagai pembanding, bukan angka mutlak)")
    print(f"  curvature d  : median {statistics.median(nilai_d):.3f}")
    print(f"  surprisal    : median {statistics.median(nilai_s):.3f} bit")
    print(f"  CV surprisal : median {statistics.median(nilai_cv):.3f}")
    print("\nNaskah baru yang curvature-nya jauh DI ATAS median tulisan lama Anda,")
    print("dan surprisal-nya jauh DI BAWAH median, adalah naskah yang perlu dikerjakan.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Audit lapis probabilitas token")
    ap.add_argument("berkas", nargs="*")
    ap.add_argument("--model", default=MODEL_BAWAAN)
    ap.add_argument("--device", default=None, help="cpu atau cuda")
    ap.add_argument("--topk", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--calibrate", nargs="+", metavar="BERKAS",
                    help="bangun garis dasar dari tulisan lama Anda sendiri")
    ap.add_argument("--selftest", action="store_true",
                    help="uji rumus tanpa memuat model")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.calibrate:
        paths = []
        for pola in args.calibrate:
            paths.extend(glob.glob(pola))
        penilai = Penilai(args.model, args.device)
        return kalibrasi(sorted(paths), penilai)

    if not args.berkas:
        ap.error("berikan minimal satu berkas, atau gunakan --selftest / --calibrate")

    penilai = Penilai(args.model, args.device)
    semua = []
    for pola in args.berkas:
        for p in sorted(glob.glob(pola)) or [pola]:
            if not Path(p).exists():
                print(f"[lewat] {p}", file=sys.stderr)
                continue
            h = audit_berkas(p, penilai, args.topk)
            if h:
                semua.append(h)
                if not args.json:
                    cetak(h)
    if args.json:
        print(json.dumps(semua, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
