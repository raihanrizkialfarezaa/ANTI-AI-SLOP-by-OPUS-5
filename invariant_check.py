#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
invariant_check.py : Penjaga Kontrak Invarian ANTI_AI_SLOP_GUARD v4.0.

Membandingkan naskah SEBELUM dan SESUDAH de-slopping, lalu memastikan
substansi bertahan 100 persen. Alat ini menjawab satu pertanyaan tunggal:
"apakah penyuntingan gaya mengubah isi?"

Yang diperiksa:
  1. Angka dan satuan          (hilang = temuan; muncul baru = risiko fabrikasi)
  2. Sitasi (Penulis, Tahun)   (hilang, berubah, atau bertambah)
  3. Istilah terkunci          (dari terms.json; wajib tetap dan tidak disinonimkan)
  4. Nama diri dan narasumber  (Ibu Atik, Apotek Bisma, RabbitMQ, dan sebagainya)
  5. Kode identifier           (F1..F6, RM1..RM3, Tabel 3.6, Gambar 3.1)
  6. Span kode inline          (`orders`, `outbox`)
  7. Struktur                  (jumlah dan urutan heading, jumlah paragraf per subbab)
  8. Kalimat yang lenyap       (paragraf yang kehilangan proposisi, bukan hanya kata)

Pemakaian:
    python invariant_check.py SEBELUM.md SESUDAH.md
    python invariant_check.py SEBELUM.md SESUDAH.md --terms tools/terms.json
    python invariant_check.py SEBELUM.md SESUDAH.md --json
    python invariant_check.py --init-terms tools/terms.json

Exit code 0 bila seluruh invarian aman, 1 bila ada pelanggaran.
Alat ini bersifat konservatif: lebih baik melaporkan temuan palsu daripada
meloloskan angka yang menguap.
"""

import argparse
import difflib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

TERMS_DEFAULT = {
    "istilah_terkunci": [
        "outbox", "idempotency key", "Monolith Terpusat", "EDA Tanpa Proteksi",
        "EDA dengan Proteksi", "konsistensi data", "recovery window",
        "publisher confirm", "oversell", "lost update", "duplicate effect",
        "permanent mismatch", "untraceable event", "terminal-state coverage",
    ],
    "sinonim_terlarang": {
        "outbox": ["tabel perantara", "buffer kejadian", "penampung pesan",
                   "tabel penampung", "buffer peristiwa"],
        "konsistensi data": ["efektivitas", "keandalan sistem", "kualitas data"],
        "Monolith Terpusat": ["arsitektur konvensional", "sistem lama",
                              "monolitik tradisional", "Kondisi A"],
        "EDA Tanpa Proteksi": ["EDA dasar", "EDA polos", "Kondisi B"],
        "EDA dengan Proteksi": ["EDA lengkap", "EDA termitigasi", "Kondisi C"],
        "recovery window": ["masa pemulihan", "periode stabilisasi"],
    },
    "nama_diri": [
        "Apotek Bisma", "Ibu Atik", "Ibu Sri Utami", "Mojokerto", "UNESA",
        "RabbitMQ", "MySQL", "Docker Compose", "Sooko",
    ],
}

# ---------------------------------------------------------------------------
# Ekstraktor
# ---------------------------------------------------------------------------
RE_ANGKA = re.compile(
    r"(?<![\w.])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)\s*"
    r"(ms|milidetik|detik|menit|jam|%|persen|persentil|req/detik|"
    r"permintaan per detik|run|blok|cabang|unit|kali|GB|MB|KB|rps)?",
    re.IGNORECASE)
RE_SITASI = re.compile(r"\(([A-Z][A-Za-z\u00C0-\u017F'’-]+(?:\s+(?:dkk\.|et\s+al\.|&|dan)\s+"
                       r"[A-Z][A-Za-z\u00C0-\u017F'’-]+)?),?\s*(\d{4})[a-z]?\)")
RE_SITASI_NARATIF = re.compile(r"\b([A-Z][A-Za-z\u00C0-\u017F'’-]{2,})\s*\((\d{4})[a-z]?\)")
RE_KODE = re.compile(r"\b(F\d[ab]?|RM\d|H-\d{2}|G-\d{2}|"
                     r"(?:Tabel|Gambar|Persamaan|Lampiran|Bagian|Bab)\s+[\dIVXA-Z]+(?:\.\d+)*)\b")
RE_INLINE_CODE = re.compile(r"`([^`\n]{1,60})`")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def normalisasi(teks):
    return unicodedata.normalize("NFC", teks)


def buang_kode_blok(teks):
    return re.sub(r"```.*?```", " ", teks, flags=re.DOTALL)


def angka_dari(teks):
    hasil = []
    for m in RE_ANGKA.finditer(teks):
        nilai = m.group(1)
        satuan = (m.group(2) or "").lower().strip()
        if satuan in {"", None} and len(nilai) <= 1:
            continue  # angka tunggal tanpa satuan terlalu berisik
        hasil.append(f"{nilai} {satuan}".strip())
    return Counter(hasil)


def sitasi_dari(teks):
    hasil = []
    for m in RE_SITASI.finditer(teks):
        hasil.append(f"{m.group(1)} {m.group(2)}")
    for m in RE_SITASI_NARATIF.finditer(teks):
        hasil.append(f"{m.group(1)} {m.group(2)}")
    return Counter(hasil)


def kode_dari(teks):
    return Counter(m.group(1) for m in RE_KODE.finditer(teks))


def inline_code_dari(teks):
    return Counter(m.group(1) for m in RE_INLINE_CODE.finditer(teks))


def heading_dari(teks):
    return [f"{m.group(1)} {m.group(2).strip()}" for m in RE_HEADING.finditer(teks)]


def paragraf_dari(teks):
    bersih = buang_kode_blok(teks)
    baris = [b for b in bersih.split("\n")]
    paragraf, buf = [], []
    for b in baris:
        if b.strip().startswith("#"):
            if buf:
                paragraf.append(" ".join(buf).strip())
                buf = []
            continue
        if not b.strip():
            if buf:
                paragraf.append(" ".join(buf).strip())
                buf = []
            continue
        buf.append(b.strip())
    if buf:
        paragraf.append(" ".join(buf).strip())
    return [p for p in paragraf if p]


def hitung_frasa(teks, daftar):
    rendah = teks.lower()
    return {f: rendah.count(f.lower()) for f in daftar}


def kalimat_dari(paragraf):
    potong = re.split(r'(?<=[.!?])\s+(?=[A-Z"(`])', re.sub(r"\s+", " ", paragraf))
    return [k.strip() for k in potong if len(k.strip()) > 1]


def isi_kata(teks):
    """Kata isi (content words) untuk uji proposisi hilang."""
    kata = re.findall(r"[A-Za-z\u00C0-\u017F][\w\u00C0-\u017F-]{3,}", teks.lower())
    henti = {
        "yang", "dan", "dengan", "untuk", "pada", "dari", "dalam", "atau", "juga",
        "tidak", "akan", "telah", "oleh", "sebagai", "tersebut", "adalah", "dapat",
        "lebih", "karena", "serta", "agar", "bahwa", "para", "suatu", "secara",
        "ini", "itu", "setiap", "seluruh", "antara", "ketika", "sehingga", "namun",
        "tetapi", "hanya", "masih", "sudah", "belum", "sangat", "maka", "kemudian",
    }
    return {k for k in kata if k not in henti}


# ---------------------------------------------------------------------------
# Pemeriksaan
# ---------------------------------------------------------------------------
def banding_counter(nama, sebelum, sesudah, arah_tambah_berbahaya=True):
    temuan = []
    for item, n in sebelum.items():
        m = sesudah.get(item, 0)
        if m < n:
            temuan.append({
                "jenis": f"{nama} HILANG",
                "detail": f"'{item}' muncul {n}x pada naskah awal, {m}x pada hasil suntingan",
                "berat": True,
            })
    if arah_tambah_berbahaya:
        for item, m in sesudah.items():
            n = sebelum.get(item, 0)
            if m > n:
                temuan.append({
                    "jenis": f"{nama} BERTAMBAH",
                    "detail": f"'{item}' muncul {m}x pada hasil suntingan, {n}x pada naskah awal",
                    "berat": True,
                })
    return temuan


def periksa(sebelum_teks, sesudah_teks, terms):
    a = normalisasi(sebelum_teks)
    b = normalisasi(sesudah_teks)
    a_p, b_p = buang_kode_blok(a), buang_kode_blok(b)
    temuan = []

    temuan += banding_counter("ANGKA", angka_dari(a_p), angka_dari(b_p))
    temuan += banding_counter("SITASI", sitasi_dari(a_p), sitasi_dari(b_p))
    temuan += banding_counter("KODE/RUJUKAN", kode_dari(a_p), kode_dari(b_p))
    temuan += banding_counter("IDENTIFIER KODE", inline_code_dari(a), inline_code_dari(b))

    # Istilah terkunci
    ha = hitung_frasa(a_p, terms["istilah_terkunci"])
    hb = hitung_frasa(b_p, terms["istilah_terkunci"])
    for istilah, n in ha.items():
        if n > 0 and hb[istilah] < n:
            temuan.append({
                "jenis": "ISTILAH TERKUNCI BERKURANG",
                "detail": f"'{istilah}': {n}x -> {hb[istilah]}x (cek apakah disinonimkan)",
                "berat": True,
            })

    # Sinonim terlarang yang baru muncul
    for istilah, sinonim in terms.get("sinonim_terlarang", {}).items():
        for s in sinonim:
            na, nb = a_p.lower().count(s.lower()), b_p.lower().count(s.lower())
            if nb > na:
                temuan.append({
                    "jenis": "SINONIMISASI TERDETEKSI",
                    "detail": f"'{s}' bertambah ({na} -> {nb}); istilah terkunci seharusnya '{istilah}'",
                    "berat": True,
                })

    # Nama diri
    hna = hitung_frasa(a_p, terms["nama_diri"])
    hnb = hitung_frasa(b_p, terms["nama_diri"])
    for nama, n in hna.items():
        if n > 0 and hnb[nama] < n:
            temuan.append({
                "jenis": "NAMA DIRI BERKURANG",
                "detail": f"'{nama}': {n}x -> {hnb[nama]}x",
                "berat": True,
            })

    # Struktur heading
    ha_h, hb_h = heading_dari(a), heading_dari(b)
    if ha_h != hb_h:
        sm = difflib.SequenceMatcher(None, ha_h, hb_h)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            temuan.append({
                "jenis": "STRUKTUR HEADING BERUBAH",
                "detail": f"{tag}: awal {ha_h[i1:i2]} -> hasil {hb_h[j1:j2]}",
                "berat": True,
            })

    # Jumlah paragraf
    pa, pb = paragraf_dari(a), paragraf_dari(b)
    if len(pa) != len(pb):
        temuan.append({
            "jenis": "JUMLAH PARAGRAF BERUBAH",
            "detail": f"{len(pa)} paragraf -> {len(pb)} paragraf "
                      f"(kontrak: satu paragraf masuk, satu paragraf keluar)",
            "berat": True,
        })

    # Proposisi hilang per paragraf (hanya bila jumlah paragraf sama)
    if len(pa) == len(pb):
        for i, (x, y) in enumerate(zip(pa, pb), start=1):
            hilang = isi_kata(x) - isi_kata(y)
            # buang kata yang memang sasaran de-slopping
            sasaran = {
                "krusial", "fundamental", "holistik", "komprehensif", "menyeluruh",
                "signifikan", "optimal", "esensial", "vital", "melainkan", "demikian",
                "menariknya", "digarisbawahi", "paradigma", "kesenjangan", "menjembatani",
                "efektivitas", "dikarenakan", "supaya", "sekali", "merupakan",
                "berangkat", "konteks", "lanskap", "inovatif", "canggih", "mutakhir",
            }
            hilang = {h for h in hilang if h not in sasaran}
            if len(hilang) > 3:
                temuan.append({
                    "jenis": "KATA ISI HILANG DARI PARAGRAF",
                    "detail": f"Paragraf {i}: {sorted(hilang)[:12]}",
                    "berat": len(hilang) > 6,
                })
            # perubahan panjang ekstrem
            la, lb = len(x.split()), len(y.split())
            if lb < 0.55 * la:
                temuan.append({
                    "jenis": "PARAGRAF MENYUSUT DRASTIS",
                    "detail": f"Paragraf {i}: {la} kata -> {lb} kata ({int(100*lb/max(1,la))}%)",
                    "berat": True,
                })

    return temuan, {
        "paragraf_awal": len(pa), "paragraf_hasil": len(pb),
        "heading_awal": len(ha_h), "heading_hasil": len(hb_h),
        "angka_awal": sum(angka_dari(a_p).values()),
        "angka_hasil": sum(angka_dari(b_p).values()),
        "sitasi_awal": sum(sitasi_dari(a_p).values()),
        "sitasi_hasil": sum(sitasi_dari(b_p).values()),
    }


def main():
    ap = argparse.ArgumentParser(description="Penjaga Kontrak Invarian de-slopping")
    ap.add_argument("sebelum", nargs="?", help="naskah sebelum disunting")
    ap.add_argument("sesudah", nargs="?", help="naskah sesudah disunting")
    ap.add_argument("--terms", help="berkas JSON istilah terkunci")
    ap.add_argument("--init-terms", help="tulis berkas terms.json bawaan lalu keluar")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.init_terms:
        Path(args.init_terms).parent.mkdir(parents=True, exist_ok=True)
        Path(args.init_terms).write_text(
            json.dumps(TERMS_DEFAULT, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"terms bawaan ditulis ke {args.init_terms}")
        return 0

    if not args.sebelum or not args.sesudah:
        ap.error("perlu dua berkas: SEBELUM.md SESUDAH.md")

    terms = TERMS_DEFAULT
    if args.terms and Path(args.terms).exists():
        terms = json.loads(Path(args.terms).read_text(encoding="utf-8"))
        terms.setdefault("sinonim_terlarang", {})
        terms.setdefault("nama_diri", [])
        terms.setdefault("istilah_terkunci", [])

    a = Path(args.sebelum).read_text(encoding="utf-8", errors="replace")
    b = Path(args.sesudah).read_text(encoding="utf-8", errors="replace")
    temuan, ringkas = periksa(a, b, terms)

    if args.json:
        print(json.dumps({"temuan": temuan, "ringkasan": ringkas},
                         ensure_ascii=False, indent=2))
    else:
        garis = "=" * 78
        print(garis)
        print(f"KONTRAK INVARIAN : {Path(args.sebelum).name} -> {Path(args.sesudah).name}")
        print(garis)
        print(f"Paragraf : {ringkas['paragraf_awal']} -> {ringkas['paragraf_hasil']}   "
              f"Heading : {ringkas['heading_awal']} -> {ringkas['heading_hasil']}")
        print(f"Angka    : {ringkas['angka_awal']} -> {ringkas['angka_hasil']}   "
              f"Sitasi  : {ringkas['sitasi_awal']} -> {ringkas['sitasi_hasil']}")
        print()
        berat = [t for t in temuan if t["berat"]]
        if not temuan:
            print("HIJAU. Substansi bertahan 100 persen. Perubahan murni bergaya bahasa.")
        elif not berat:
            print(f"HIJAU dengan catatan. {len(temuan)} temuan ringan, nol temuan berat.")
            print("Periksa sekilas, biasanya berupa diksi slop yang memang sengaja dibuang.\n")
        else:
            print(f"MERAH. {len(temuan)} temuan ({len(berat)} berat). Revisi ditolak "
                  f"sampai seluruh temuan berat diperbaiki.\n")
            for t in temuan:
                tanda = "!!" if t["berat"] else " ~"
                print(f" {tanda} [{t['jenis']}] {t['detail']}")
        print()
    return 1 if any(t["berat"] for t in temuan) else 0


if __name__ == "__main__":
    sys.exit(main())
