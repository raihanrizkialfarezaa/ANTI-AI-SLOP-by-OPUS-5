#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slop_audit.py : Auditor AI-Slop untuk naskah tugas akhir berbahasa Indonesia.

Pendamping wajib ANTI_AI_SLOP_GUARD.md v4.0.
Menghitung AI-Slop Index (ASI) 0..100 dari delapan dimensi:
  L  Leksikal      (frasa blacklist, kata sifat kosong, transisi filler)
  R  Retoris       (negasi paralel, trikolon, puffery, rekap penutup, aside editorial)
  S  Sintaksis     (nominalisasi, klausa partisipial, "yang mana", pasif berlebih, rantai anafora)
  I  Irama         (rendahnya variasi panjang kalimat dan panjang paragraf)
  N  Register      (ragam percakapan, sapaan pembaca, kata ganti, diksi takbaku)
  E  Ejaan         (kata depan di/ke, "di mana" relatif, tanda baca, angka desimal)
  K  Kalimat       (kesepadanan struktur, pemborosan kata, konjungsi ganda)
  B  Blocker       (residu prompt, placeholder, mermaid mentah, label terlarang)
  D  Densitas      (propositional idea density, compression ratio, templatedness,
                    subjektivitas, simetri paralel, listifikasi) -- taksonomi
                    Shaib dkk. 2025 "Measuring AI Slop in Text" (arXiv:2509.19163)

Pemakaian:
    python slop_audit.py NASKAH.md [NASKAH2.md ...]
    python slop_audit.py --json NASKAH.md
    python slop_audit.py --show 8 NASKAH.md     # tampilkan maksimal 8 contoh per temuan

Keluaran: laporan per berkas + nomor baris setiap temuan.
Exit code 1 jika ada temuan BLOCKER atau ASI di atas ambang (default 25).

Catatan kejujuran metodologis: ambang di bawah ini adalah heuristik kerja yang
dikalibrasi terhadap prosa teknis Indonesia, bukan standar baku dari literatur.
Angka ini dipakai untuk mengarahkan revisi, bukan untuk membuktikan
sesuatu ditulis mesin atau manusia.
"""

import argparse
import gzip
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# ----------------------------------------------------------------------------
# 1. AMBANG (dapat diubah sesuai kesepakatan bimbingan)
# ----------------------------------------------------------------------------
AMBANG = {
    "asi_maks": 25.0,            # AI-Slop Index maksimum agar dinyatakan lolos
    "cv_panjang_kalimat_min": 0.40,   # koefisien variasi panjang kalimat
    "sd_panjang_kalimat_min": 7.0,    # simpangan baku panjang kalimat (kata)
    "rasio_kalimat_pendek_min": 0.18, # proporsi kalimat < 15 kata
    "rerata_kalimat_maks": 26.0,      # rerata panjang kalimat (kata)
    "kalimat_sangat_panjang_maks": 0.08,  # proporsi kalimat > 40 kata
    "cv_panjang_paragraf_min": 0.25,
    "densitas_nominalisasi_maks": 0.075,  # nominalisasi per kata
    "rasio_pasif_maks": 0.42,         # verba di- per (verba di- + verba me-)
    "transisi_awal_kalimat_maks": 0.14,   # kalimat yang dibuka konektor filler
    "yang_per_kalimat_maks": 1.35,
}

# ----------------------------------------------------------------------------
# 2. KAMUS POLA
# ----------------------------------------------------------------------------

# --- B: BLOCKER -------------------------------------------------------------
POLA_BLOCKER = [
    ("B1 residu instruksi prompt",
     r"(dijelaskan\s+kebutuhannya|kebutuhannya\s+apa|sesuai\s+komentar|perlu\s+diperjelas|"
     r"tambahkan\s+sitasi|masukkan\s+data\s+di\s+sini|isi\s+dengan|silakan\s+sesuaikan|"
     r"berikut\s+adalah\s+versi|versi\s+revisi\s+di\s+bawah|semoga\s+membantu|"
     r"tentu,?\s+berikut|sebagai\s+model\s+bahasa)"),
    ("B2 placeholder belum diisi",
     r"(\[TODO\]|\[Nama\]|\[Tahun\]|\[Kutipan\]|\[Gambar[^\]]*\]|\[Tabel[^\]]*\]|\bTBD\b|\bXXX\b|"
     r"\blorem ipsum\b|\(\?\?\?\)|\bdst\.\.\.)"),
    ("B3 blok kode mentah / markdown bocor",
     r"(```mermaid|```python|^\s*```|<<<<<<<|>>>>>>>)"),
    ("B4 catatan editorial tertinggal",
     r"(Catatan\s+revisi|Catatan\s+untuk\s+pembimbing|CATATAN:|NB:|TODO:|FIXME|# ?draft)"),
    ("B5 label terlarang Kondisi/Artefak A-B-C",
     r"\b(Kondisi|Artefak|Skenario)\s+[ABC]\b"),
    ("B6 konstruk 'efektivitas' yang dilarang",
     r"\befektivitas\b"),
    ("B7 istilah metodologi yang dilarang",
     r"\b(DSRM|Design\s+Science\s+Research\s+Methodology|Peffers\s+enam\s+tahap)\b"),
    ("B8 statistik inferensial yang dilarang",
     r"\b(H0|H1|p-?value|nilai\s+p\b|uji\s+Wilcoxon|uji\s+Friedman|signifikan\s+secara\s+statistik)\b"),
    ("B9 kalimat patah / kata ganda (splice glitch)",
     r"\b(\w{4,})\s+\1\b|,\s*,|\.\s*\.|\s+,\s*[A-Z][a-z]+kan\b"),
    ("B11 ragam percakapan (register turun)",
     r"\b(memakai|dipakai|kepakai|lewat|bikin|dibikin|ketahuan|kelihatan|ngecek|"
     r"gara-gara|kayak|banget|nggak|ndak|udah|dapetin|ngasih|naruh|bareng|"
     r"seperti\s+misalnya)\b"),
    ("B12 sapaan pembaca / ajakan",
     r"\b(Anda|kamu|mari\s+kita|mari\s+|bayangkan|perhatikan\s+bahwa|coba\s+lihat|ingat\s+bahwa)\b"),
    ("B13 kata ganti orang yang dilarang",
     r"\b(saya|aku|kami|kita)\b"),
    ("B14 diksi takbaku (KBBI / EYD V)",
     r"\b(analisa|analisanya|praktek|resiko|sistim|obyek|subyek|hakekat|standarisasi|"
     r"frekwensi|kwalitas|kwantitas|managemen|aktifitas|produktifitas|apotik|nomer|ijin|"
     r"nasehat|jadual|propinsi|silahkan|antri|merubah|mempengaruhi|difinisi|komplek|"
     r"metoda|hipotesa|sintesa|disain|konkrit|karir|sekedar|terlanjur|himbau|lembab|nampak|"
     r"disamping\s+itu|kedepan|dimana)\b"),
    ("B15 kata depan / awalan di- keliru (EYD V)",
     r"\b(digudang|dicabang|dirumah|dikantor|dimeja|dilapangan|kegudang|kecabang|"
     r"disini|disitu|disana|keatas|kebawah|keluar\s+kota\b(?!))\b|"
     r"\bdi\s+(catat|simpan|kirim|uji|ukur|lakukan|gunakan|bandingkan|terapkan|jalankan)\b"),
    ("B16 'di mana' sebagai penanda klausa relatif",
     r",\s*di\s+mana\b|\bdi\s+mana\s+(setiap|seluruh|masing-masing|data|sistem|layanan)\b"),
    ("B17 kalimat kehilangan subjek (kesepadanan struktur)",
     r"(^|\.\s|\n)\s*(Dalam|Berdasarkan|Menurut|Pada|Dengan|Melalui)\b[^.\n]{0,70}?\b"
     r"(menunjukkan|menjelaskan|membandingkan|menyatakan|menguraikan|memaparkan|menghasilkan)\b"),
    ("B10 karakter tipografi terlarang",
     r"(\u2014|\u2013\s|\u201c|\u201d|\u2018|\u2019)"),
]

# --- R: RETORIS -------------------------------------------------------------
POLA_RETORIS = [
    ("R1 negasi paralel (bukan X melainkan Y)", 3.0,
     r"\b(bukan(lah)?\s+(lagi\s+|sekadar\s+|semata\s+|hanya\s+)?[^.;]{2,70}?\b(melainkan|tetapi|namun|tapi)\b|"
     r"tidak\s+hanya\s+[^.;]{2,70}?\btetapi\s+juga\b|"
     r"alih-alih\s+[^.;]{2,70}?,\s*(justru|malah))"),
    ("R2 trikolon / rangkaian tiga sejajar", 1.5,
     r"\b[A-Za-z]{4,},\s+[A-Za-z]{4,},\s+dan\s+[A-Za-z]{4,}\b"),
    ("R3 puffery dan hiperbola generik", 2.0,
     r"\b(sangat\s+(krusial|penting|vital|fundamental)|memegang\s+peranan\s+(penting|kunci|vital)|"
     r"menjadi\s+kunci\s+utama|tak\s+dapat\s+dipungkiri|tidak\s+dapat\s+dipungkiri|"
     r"era\s+(digital|modern|revolusi\s+industri)|di\s+tengah\s+(pesatnya|derasnya)|"
     r"semakin\s+(pesat|kompleks|dinamis)|lanskap\s+(bisnis|teknologi|digital))"),
    ("R4 aside editorial / menggurui", 2.0,
     r"\b(patut\s+(digarisbawahi|dicatat|diperhatikan)|penting\s+untuk\s+dicatat|perlu\s+dicatat\s+bahwa|"
     r"menariknya|yang\s+lebih\s+penting\s+lagi|tidak\s+berlebihan\s+jika|sudah\s+barang\s+tentu)"),
    ("R5 kalimat rekap penutup paragraf", 2.0,
     r"(^|\n)\s*(Dengan\s+demikian|Singkatnya|Secara\s+keseluruhan|Pada\s+akhirnya|Kesimpulannya|"
     r"Hal\s+ini\s+menunjukkan\s+bahwa|Hal\s+ini\s+menegaskan)\b"),
    ("R6 pertanyaan retoris", 2.0,
     r"\?[\s\n]"),
    ("R7 keberatan semu / false balance", 1.5,
     r"\b(memang\s+benar\s+bahwa|meskipun\s+demikian,\s+perlu|di\s+satu\s+sisi[^.]{0,80}di\s+sisi\s+lain|"
     r"tentu\s+saja,\s+hal\s+ini)"),
    ("R8 metafora kosong", 2.5,
     r"\b(menjembatani\s+kesenjangan|tulang\s+punggung|jantung\s+dari|pilar\s+utama|batu\s+loncatan|"
     r"membuka\s+jalan\s+bagi|paradigma\s+baru|terobosan|game\s+changer|kunci\s+sukses)"),
]

# --- L: LEKSIKAL ------------------------------------------------------------
POLA_LEKSIKAL = [
    ("L1 kata sifat kosong tanpa metrik", 2.0,
     r"\b(holistik|komprehensif|menyeluruh\s+dan|krusial|esensial|signifikan(?!si)|optimal|"
     r"robust|seamless|mulus|andal\s+dan\s+efisien|inovatif|canggih|mutakhir|multifaset)\b"),
    ("L2 transisi filler", 2.0,
     r"(^|\n|\.\s)(Dalam\s+konteks\s+ini|Lebih\s+lanjut|Lebih\s+jauh\s+lagi|Selanjutnya,|Di\s+sisi\s+lain|"
     r"Sehubungan\s+dengan\s+hal\s+tersebut|Berangkat\s+dari|Terkait\s+hal\s+tersebut|"
     r"Sejalan\s+dengan\s+itu|Adapun\s+demikian|Selain\s+itu,\s+perlu)"),
    ("L3 pemborosan kata", 1.5,
     r"\b(hal\s+ini\s+dikarenakan\s+oleh\s+fakta\s+bahwa|dapat\s+dikatakan\s+bahwa|"
     r"merupakan\s+salah\s+satu\s+hal\s+yang|dalam\s+rangka\s+untuk|guna\s+untuk|"
     r"sebagaimana\s+yang\s+telah\s+dijelaskan\s+sebelumnya|seperti\s+yang\s+kita\s+ketahui|"
     r"perlu\s+diketahui\s+bahwa|pada\s+dasarnya|secara\s+umum,)"),
    ("L4 jargon humas dan manajemen", 2.5,
     r"\b(harmonisasi|sinergi|sinergitas|ekosistem\s+digital|transformasi\s+digital|"
     r"nilai\s+tambah|solusi\s+terpadu|berdaya\s+saing|stakeholder|end-to-end\s+solution)\b"),
    ("L5 residu diksi Inggris khas LLM", 3.0,
     r"\b(delve|menyelami\s+lebih\s+dalam|underscore|menggarisbawahi\s+pentingnya|showcase|"
     r"mengupas\s+tuntas|tapestry|permadani|realm|ranah\s+yang\s+luas|pivotal|meticulous|"
     r"leverage|memanfaatkan\s+kekuatan|testament|bukti\s+nyata\s+akan|navigasi\s+tantangan|"
     r"interplay|keterkaitan\s+yang\s+kompleks|foster|menumbuhkan|elevate|mengangkat\s+ke\s+level)\b"),
    ("L6 atribusi kabur tanpa sitasi", 3.0,
     r"\b(banyak\s+penelitian\s+menunjukkan|berbagai\s+studi\s+(telah\s+)?membuktikan|para\s+ahli\s+berpendapat|"
     r"penelitian\s+terbaru\s+mengungkap|secara\s+luas\s+diakui|umumnya\s+dipahami\s+bahwa|"
     r"sejumlah\s+literatur\s+menyebutkan)\b(?![^.]{0,60}\(\w+,?\s*\d{4})"),
    ("L7 hedging berlebihan", 1.5,
     r"\b(kemungkinan\s+besar|cenderung\s+dapat|dapat\s+saja|mungkin\s+saja|relatif\s+cukup|"
     r"secara\s+umum\s+dapat|berpotensi\s+untuk|diharapkan\s+mampu)\b"),
]

# --- S: SINTAKSIS -----------------------------------------------------------
POLA_SINTAKSIS = [
    ("S1 klausa partisipial tempelan (ekor -ing)", 3.0,
     r",\s+(sehingga\s+)?(memastikan|menghasilkan|menciptakan|memungkinkan|mencerminkan|menegaskan|"
     r"menunjukkan|menjadikan|mendukung|memperkuat|menyoroti)\s+\w+"),
    ("S2 relativisasi 'yang mana'", 3.0,
     r"\byang\s+mana\b"),
    ("S3 rantai anafora 'hal ini/hal tersebut'", 1.5,
     r"\b(hal\s+ini|hal\s+tersebut|kondisi\s+ini|kondisi\s+tersebut)\b"),
    ("S4 subjek klausa 'bahwa' di awal kalimat", 2.0,
     r"(^|\n|\.\s)(Bahwa|Fakta\s+bahwa|Kenyataan\s+bahwa)\b"),
    ("S5 koordinasi frasal bertumpuk", 1.5,
     r"\b\w+\s+dan\s+\w+\s+serta\s+\w+\s+(dan|maupun)\s+\w+\b"),
    ("S6 kopula definisi berantai", 1.5,
     r"\b(merupakan|adalah)\s+\w+\s+yang\s+(berfungsi|bertujuan|digunakan)\s+untuk\b"),
]

# --- K: KALIMAT EFEKTIF (berbobot) -----------------------------------------
POLA_KALIMAT = [
    ("K2 pemborosan kata / pleonasme", 2.5,
     r"\b(adalah\s+merupakan|agar\s+supaya|demi\s+untuk|disebabkan\s+karena|namun\s+tetapi|"
     r"sejak\s+dari|dalam\s+rangka\s+untuk|guna\s+untuk|dapat\s+dikatakan\s+bahwa|"
     r"merupakan\s+salah\s+satu\s+hal\s+yang|sangat\s+\w+\s+sekali|naik\s+ke\s+atas|"
     r"turun\s+ke\s+bawah|saling\s+\w+\s+satu\s+sama\s+lain|para\s+\w+-\w+|"
     r"beberapa\s+\w+-\w+|terlebih\s+dahulu\s+terlebih)\b"),
    ("K3 konjungsi ganda", 3.0,
     r"\b(Karena|karena)\b[^.\n]{0,80}\bsehingga\b|\b(Walaupun|Meskipun|walaupun|meskipun)\b[^.\n]{0,80}\b(namun|tetapi)\b"),
    ("K4 verba hampa (melakukan + nomina)", 2.0,
     r"\b(melakukan|mengadakan|memberikan|melaksanakan)\s+(pengujian|analisis|pengukuran|"
     r"penjelasan|perbandingan|implementasi|perancangan|evaluasi|pencatatan|pengamatan)\b"),
]

# --- E: EJAAN (berbobot, selain blocker) ------------------------------------
POLA_EJAAN = [
    ("E4 spasi sebelum tanda baca", 1.5, r"\s+[.,;:]\s"),
    ("E5 desimal memakai titik (seharusnya koma)", 2.0,
     r"\b\d+\.\d{1,2}\s*(ms|detik|persen|%|s\b)"),
    ("E6 bentuk terikat ditulis terpisah", 2.0,
     r"\b(antar|non|pasca|sub|multi|pra|semi|swa)\s+[a-z]{3,}\b"),
    ("E7 singkatan takresmi pada badan teks", 2.0,
     r"\b(yg|dgn|tsb|dsb|dst|utk|krn)\b"),
]

# Kata yang diawali "di" tetapi bukan verba pasif
BUKAN_PASIF = {
    "dia", "dini", "digital", "dinas", "diagram", "dimensi", "diameter", "diagnosa",
    "diagnosis", "dialog", "diaspora", "dividen", "divisi", "diskusi", "distribusi",
    "disertasi", "disiplin", "diskrit", "direktori", "direktur", "dinamis", "dinamika",
    "dilema", "diploma", "diagonal", "dialek", "difusi", "digit", "diskon", "dikte",
}

KATA_HENTI = {
    "yang", "dan", "di", "ke", "dari", "pada", "untuk", "dengan", "dalam", "ini", "itu",
    "atau", "juga", "tidak", "akan", "telah", "oleh", "sebagai", "tersebut", "adalah",
    "dapat", "lebih", "karena", "serta", "agar", "bahwa", "para", "suatu", "secara",
}


# ----------------------------------------------------------------------------
# 3. PREPROSES
# ----------------------------------------------------------------------------
def muat_prosa(teks):
    """Buang blok kode, tabel, heading, dan blockquote. Kembalikan (prosa, peta_baris)."""
    baris = teks.split("\n")
    hasil, peta = [], []
    dalam_kode = False
    for i, b in enumerate(baris, start=1):
        s = b.strip()
        if s.startswith("```"):
            dalam_kode = not dalam_kode
            continue
        if dalam_kode:
            continue
        if not s:
            hasil.append("")
            peta.append(i)
            continue
        if s.startswith("#") or s.startswith(">") or s.startswith("|"):
            continue
        if re.match(r"^[-*+]\s", s) or re.match(r"^\d+\.\s", s):
            s = re.sub(r"^([-*+]|\d+\.)\s+", "", s)
        hasil.append(s)
        peta.append(i)
    return "\n".join(hasil), peta


def paragraf_dari(prosa):
    return [p.strip() for p in re.split(r"\n\s*\n", prosa) if p.strip()]


def kalimat_dari(paragraf):
    teks = re.sub(r"\s+", " ", paragraf)
    potongan = re.split(r'(?<=[.!?])\s+(?=[A-Z"(\u201c])', teks)
    return [k.strip() for k in potongan if len(k.strip()) > 1]


def kata_dari(teks):
    bersih = re.sub(r"[*_`\[\]()]", " ", teks)
    return re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]*", bersih)


# ----------------------------------------------------------------------------
# 4. PENCARIAN POLA
# ----------------------------------------------------------------------------
def cari(teks_asli, pola, batas_contoh):
    """Cari pola pada teks asli (per baris) agar nomor baris akurat."""
    temuan = []
    for nomor, baris in enumerate(teks_asli.split("\n"), start=1):
        for m in re.finditer(pola, baris, flags=re.IGNORECASE | re.MULTILINE):
            cuplik = baris[max(0, m.start() - 35): m.end() + 35].strip()
            temuan.append({"baris": nomor, "cuplikan": cuplik, "kena": m.group(0).strip()})
            if len(temuan) >= batas_contoh * 6:
                return temuan
    return temuan


def jalankan_kelompok(teks_asli, daftar, batas_contoh, berbobot=True):
    hasil = []
    for item in daftar:
        if berbobot:
            nama, bobot, pola = item
        else:
            nama, pola = item
            bobot = 0.0
        t = cari(teks_asli, pola, batas_contoh)
        if t:
            hasil.append({"nama": nama, "bobot": bobot, "jumlah": len(t),
                          "contoh": t[:batas_contoh]})
    return hasil



# ============================================================================
# MODUL D : DENSITAS INFORMASI DAN STRUKTUR
# Operasionalisasi taksonomi Shaib dkk. (2025), disesuaikan untuk bahasa
# Indonesia. Setiap metrik menyebut sumber aslinya.
# ============================================================================

PREPOSISI = {
    "di", "ke", "dari", "pada", "dalam", "untuk", "dengan", "oleh", "terhadap",
    "kepada", "bagi", "antara", "atas", "tentang", "melalui", "sejak", "hingga",
    "sampai", "menurut", "selama", "tanpa", "demi", "seperti", "sebagai",
}
KONJUNGSI = {
    "dan", "atau", "tetapi", "namun", "karena", "sehingga", "agar", "supaya",
    "jika", "apabila", "ketika", "saat", "sedangkan", "sementara", "meskipun",
    "walaupun", "bahwa", "yaitu", "yakni", "serta", "maupun", "lalu", "kemudian",
    "sebab", "maka", "bila", "seandainya", "kecuali", "selain",
}
ADVERBIA = {
    "tidak", "belum", "sudah", "telah", "akan", "sedang", "masih", "hanya",
    "juga", "selalu", "sering", "jarang", "kadang", "segera", "hampir", "sangat",
    "lebih", "paling", "cukup", "terlalu", "pernah", "baru", "justru", "bahkan",
    "tetap", "kembali", "langsung", "secara", "amat", "makin", "semakin",
}
PRONOMINA = {"ini", "itu", "tersebut", "nya", "mereka", "beliau", "sendiri", "masing"}

# Leksikon subjektivitas ringkas untuk bahasa Indonesia.
# Padanan fungsi dari subjectivity lexicon Wiebe dkk. (2004) yang dipakai
# Shaib dkk. untuk mengukur kode Bias. Daftar ini sengaja kecil dan hanya memuat
# kata sifat evaluatif yang tidak pantas muncul pada naskah rekayasa.
LEKSIKON_SUBJEKTIF = {
    "krusial", "vital", "fundamental", "esensial", "penting", "luar biasa",
    "hebat", "menakjubkan", "sempurna", "unggul", "terbaik", "canggih",
    "inovatif", "revolusioner", "mutakhir", "signifikan", "dramatis", "masif",
    "pesat", "menarik", "sayangnya", "untungnya", "jelas", "tentu", "pasti",
    "mustahil", "sempurna", "ideal", "optimal", "robust", "andal", "tangguh",
    "mengesankan", "memprihatinkan", "mengkhawatirkan",
}
LEKSIKON_HEDGE = {
    "mungkin", "barangkali", "kemungkinan", "cenderung", "tampaknya",
    "sepertinya", "diperkirakan", "diduga", "relatif", "umumnya", "biasanya",
    "sebagian", "beberapa", "kurang", "agak", "sedikit", "berpotensi",
}


def tag_kasar(kata):
    """Penanda kelas kata kasar untuk bahasa Indonesia (heuristik afiks).

    Bukan pengganti POS tagger sungguhan. Cukup untuk metrik compression ratio
    dan templatedness yang hanya membutuhkan urutan kelas yang konsisten.
    """
    k = kata.lower()
    if k in PREPOSISI:
        return "PREP"
    if k in KONJUNGSI:
        return "CONJ"
    if k in ADVERBIA:
        return "ADV"
    if k in PRONOMINA:
        return "PRON"
    if re.match(r"^\d", k):
        return "NUM"
    if re.match(r"^(pe|per|peng|pen|pem|penye|ke)\w{3,}an$", k):
        return "NOMN"          # nominalisasi
    if re.match(r"^(me|mem|men|meng|meny|mempe|memper)\w{3,}$", k):
        return "VERB"
    if re.match(r"^(di|diper|ter|ber)\w{3,}$", k):
        return "VPAS"
    if k == "yang":
        return "REL"
    return "NOUN"


def rasio_kompresi(urutan):
    """Compression ratio ala Shaib dkk. (2024a).

    Nilai lebih tinggi berarti teks lebih repetitif dan lebih templatik.
    """
    data = " ".join(urutan).encode("utf-8")
    if len(data) < 64:
        return 0.0
    return round(len(data) / max(1, len(gzip.compress(data, 6))), 3)


def templat_per_token(tag, n_min=5, n_max=8):
    """Templates-per-token ala Shaib dkk. (2024b).

    Menghitung proporsi token yang tercakup oleh n-gram kelas kata yang muncul
    lebih dari sekali. Semakin tinggi, semakin formulaik susunan kalimatnya.
    """
    if len(tag) < n_max * 2:
        return 0.0, []
    tertutup = [False] * len(tag)
    contoh = Counter()
    for n in range(n_max, n_min - 1, -1):
        hitung = Counter(tuple(tag[i:i + n]) for i in range(len(tag) - n + 1))
        ulang = {g for g, c in hitung.items() if c >= 2}
        if not ulang:
            continue
        for i in range(len(tag) - n + 1):
            g = tuple(tag[i:i + n])
            if g in ulang and not any(tertutup[i:i + n]):
                for j in range(i, i + n):
                    tertutup[j] = True
                contoh[" ".join(g)] += 1
    return round(sum(tertutup) / len(tag), 3), contoh.most_common(5)


def densitas_gagasan(kata):
    """Propositional idea density ala Brown dkk. (2008), adaptasi Indonesia.

    Gagasan didekati melalui verba, adverbia, preposisi, dan konjungsi, dibagi
    jumlah kata. Nilai tinggi berarti banyak proposisi per kata, yaitu ciri
    prosa manusia yang padat isi. Nilai rendah adalah ciri prosa banyak kata
    sedikit isi.
    """
    if not kata:
        return 0.0
    tag = [tag_kasar(k) for k in kata]
    gagasan = sum(1 for t in tag if t in {"VERB", "VPAS", "ADV", "PREP", "CONJ"})
    return round(gagasan / len(kata), 4)


def simetri_paralel(kalimat):
    """Deteksi premature symmetry: kalimat berurutan dengan pembuka sepola."""
    if len(kalimat) < 3:
        return 0.0, []
    pola, contoh = [], []
    for k in kalimat:
        kata = kata_dari(k)[:3]
        pola.append(tuple(tag_kasar(x) for x in kata))
    sama = 0
    for i in range(1, len(pola)):
        if pola[i] and pola[i] == pola[i - 1]:
            sama += 1
            if len(contoh) < 4:
                contoh.append(kalimat[i][:90])
    return round(sama / max(1, len(pola) - 1), 3), contoh


def proporsi_leksikon(kata, leksikon):
    if not kata:
        return 0.0
    return round(sum(1 for k in kata if k.lower() in leksikon) / len(kata), 4)


def metrik_densitas(prosa):
    paras = paragraf_dari(prosa)
    kalimat = []
    for p in paras:
        kalimat.extend(kalimat_dari(p))
    kata = kata_dari(prosa)
    if not kata:
        return None
    tag = [tag_kasar(k) for k in kata]
    tpt, contoh_templat = templat_per_token(tag)
    sim, contoh_sim = simetri_paralel(kalimat)
    return {
        "densitas_gagasan": densitas_gagasan(kata),
        "cr_kata": rasio_kompresi(kata),
        "cr_pos": rasio_kompresi(tag),
        "templat_per_token": tpt,
        "contoh_templat": contoh_templat,
        "simetri_pembuka": sim,
        "contoh_simetri": contoh_sim,
        "proporsi_subjektif": proporsi_leksikon(kata, LEKSIKON_SUBJEKTIF),
        "proporsi_hedge": proporsi_leksikon(kata, LEKSIKON_HEDGE),
    }


# CATATAN KALIBRASI (penting, jangan dihapus).
# densitas_gagasan, cr_pos, dan templat_per_token TIDAK memiliki ambang mutlak.
# Pengukuran pada korpus 150 sampai 4.300 kata menunjukkan cr_pos dan
# templat_per_token naik tajam mengikuti panjang teks (cr_pos 4,3 pada 165 kata
# menjadi 9,7 pada 4.258 kata), sehingga angka mutlak tidak bermakna.
# Arah densitas gagasan pun tidak stabil pada prosa Indonesia berpreposisi padat.
# Karena itu ketiganya hanya dilaporkan, dan baru dibandingkan bila tersedia
# garis dasar pribadi hasil `--calibrate` pada tulisan lama Anda sendiri.
# Yang dijadikan ambang mutlak hanyalah tiga metrik yang stabil terhadap panjang:
# simetri pembuka, diksi evaluatif, dan hedging.
AMBANG_D = {
    "simetri_pembuka_maks": 0.30,
    "proporsi_subjektif_maks": 0.012,
    "proporsi_hedge_maks": 0.018,
    "toleransi_baseline": 1.20,   # 20 persen di atas garis dasar pribadi
    "kata_minimum_struktur": 400,
}


def periksa_ambang_d(d, baseline=None):
    langgar = []
    if baseline:
        for kunci, kode, arah in (
            ("densitas_gagasan", "D1 densitas gagasan di bawah kebiasaan Anda", "bawah"),
            ("cr_pos", "D2 struktur lebih repetitif daripada tulisan lama Anda", "atas"),
            ("templat_per_token", "D3 lebih templatik daripada tulisan lama Anda", "atas"),
        ):
            ref = baseline.get(kunci)
            if not ref:
                continue
            nilai = d[kunci]
            if arah == "atas" and nilai > ref * AMBANG_D["toleransi_baseline"]:
                langgar.append(f"{kode}: {nilai} vs garis dasar {ref}")
            if arah == "bawah" and nilai < ref / AMBANG_D["toleransi_baseline"]:
                langgar.append(f"{kode}: {nilai} vs garis dasar {ref}")
    if d["simetri_pembuka"] > AMBANG_D["simetri_pembuka_maks"]:
        langgar.append(f"D4 simetri pembuka kalimat: {d['simetri_pembuka']} > "
                       f"{AMBANG_D['simetri_pembuka_maks']}")
    if d["proporsi_subjektif"] > AMBANG_D["proporsi_subjektif_maks"]:
        langgar.append(f"D5 diksi evaluatif berlebih: {d['proporsi_subjektif']} > "
                       f"{AMBANG_D['proporsi_subjektif_maks']}")
    if d["proporsi_hedge"] > AMBANG_D["proporsi_hedge_maks"]:
        langgar.append(f"D6 hedging berlebih: {d['proporsi_hedge']} > "
                       f"{AMBANG_D['proporsi_hedge_maks']}")
    return langgar


# ----------------------------------------------------------------------------
# 5. METRIK IRAMA DAN SINTAKSIS KUANTITATIF
# ----------------------------------------------------------------------------
def hitung_metrik(prosa):
    paras = paragraf_dari(prosa)
    kalimat = []
    for p in paras:
        kalimat.extend(kalimat_dari(p))
    panjang = [len(kata_dari(k)) for k in kalimat if len(kata_dari(k)) > 0]
    if not panjang:
        return None

    rerata = statistics.fmean(panjang)
    sd = statistics.pstdev(panjang) if len(panjang) > 1 else 0.0
    cv = sd / rerata if rerata else 0.0
    pendek = sum(1 for x in panjang if x < 15) / len(panjang)
    sangat_panjang = sum(1 for x in panjang if x > 40) / len(panjang)

    pjg_para = [len(kata_dari(p)) for p in paras]
    cv_para = (statistics.pstdev(pjg_para) / statistics.fmean(pjg_para)) if len(pjg_para) > 1 and statistics.fmean(pjg_para) else 0.0

    semua_kata = kata_dari(prosa)
    n = len(semua_kata) or 1
    rendah = [w.lower() for w in semua_kata]

    nominalisasi = [w for w in rendah
                    if re.match(r"^(pe|per|peng|pen|pem|penye|ke)\w{3,}an$", w)]
    pasif = [w for w in rendah if w.startswith("di") and len(w) > 5 and w not in BUKAN_PASIF
             and not w.startswith("dia")]
    aktif = [w for w in rendah if re.match(r"^(me|mem|men|meng|meny|mempe)\w{3,}$", w)]
    yang = rendah.count("yang")

    pembuka = 0
    for k in kalimat:
        if re.match(r"^(Selain\s+itu|Lebih\s+lanjut|Di\s+sisi\s+lain|Dengan\s+demikian|"
                    r"Oleh\s+karena\s+itu|Sementara\s+itu|Dalam\s+konteks|Selanjutnya|"
                    r"Namun\s+demikian|Di\s+samping\s+itu|Sehubungan\s+dengan)", k, re.IGNORECASE):
            pembuka += 1

    # MATTR jendela 50 kata sebagai proksi keragaman leksikal
    jendela, nilai = 50, []
    if len(rendah) >= jendela:
        for i in range(0, len(rendah) - jendela + 1, 10):
            potong = rendah[i:i + jendela]
            nilai.append(len(set(potong)) / jendela)
    mattr = statistics.fmean(nilai) if nilai else 0.0

    return {
        "jumlah_paragraf": len(paras),
        "jumlah_kalimat": len(panjang),
        "jumlah_kata": n,
        "rerata_panjang_kalimat": round(rerata, 2),
        "sd_panjang_kalimat": round(sd, 2),
        "cv_panjang_kalimat": round(cv, 3),
        "rasio_kalimat_pendek": round(pendek, 3),
        "rasio_kalimat_sangat_panjang": round(sangat_panjang, 3),
        "cv_panjang_paragraf": round(cv_para, 3),
        "densitas_nominalisasi": round(len(nominalisasi) / n, 4),
        "rasio_pasif": round(len(pasif) / max(1, len(pasif) + len(aktif)), 3),
        "yang_per_kalimat": round(yang / max(1, len(panjang)), 3),
        "transisi_awal_kalimat": round(pembuka / max(1, len(panjang)), 3),
        "mattr_50": round(mattr, 3),
    }


def periksa_ambang(m):
    langgar = []
    def cek(kondisi, pesan):
        if kondisi:
            langgar.append(pesan)
    cek(m["cv_panjang_kalimat"] < AMBANG["cv_panjang_kalimat_min"],
        f"I1 irama monoton: CV panjang kalimat {m['cv_panjang_kalimat']} < {AMBANG['cv_panjang_kalimat_min']}")
    cek(m["sd_panjang_kalimat"] < AMBANG["sd_panjang_kalimat_min"]
        and m["cv_panjang_kalimat"] < AMBANG["cv_panjang_kalimat_min"],
        f"I2 variasi rendah: SD {m['sd_panjang_kalimat']} < {AMBANG['sd_panjang_kalimat_min']} kata")
    cek(m["rasio_kalimat_pendek"] < AMBANG["rasio_kalimat_pendek_min"],
        f"I3 kekurangan kalimat pendek tegas: {m['rasio_kalimat_pendek']} < {AMBANG['rasio_kalimat_pendek_min']}")
    cek(m["rerata_panjang_kalimat"] > AMBANG["rerata_kalimat_maks"],
        f"I4 kalimat terlalu panjang rata-rata: {m['rerata_panjang_kalimat']} > {AMBANG['rerata_kalimat_maks']} kata")
    cek(m["rasio_kalimat_sangat_panjang"] > AMBANG["kalimat_sangat_panjang_maks"],
        f"I5 terlalu banyak kalimat > 40 kata: {m['rasio_kalimat_sangat_panjang']} > {AMBANG['kalimat_sangat_panjang_maks']}")
    cek(m["jumlah_paragraf"] >= 6 and m["cv_panjang_paragraf"] < AMBANG["cv_panjang_paragraf_min"],
        f"I6 paragraf terlalu seragam: CV {m['cv_panjang_paragraf']} < {AMBANG['cv_panjang_paragraf_min']}")
    cek(m["densitas_nominalisasi"] > AMBANG["densitas_nominalisasi_maks"],
        f"S7 nominalisasi padat: {m['densitas_nominalisasi']} > {AMBANG['densitas_nominalisasi_maks']}")
    cek(m["rasio_pasif"] > AMBANG["rasio_pasif_maks"],
        f"S8 pasif berlebih: {m['rasio_pasif']} > {AMBANG['rasio_pasif_maks']}")
    cek(m["transisi_awal_kalimat"] > AMBANG["transisi_awal_kalimat_maks"],
        f"L8 konektor pembuka kalimat berlebih: {m['transisi_awal_kalimat']} > {AMBANG['transisi_awal_kalimat_maks']}")
    cek(m["yang_per_kalimat"] > AMBANG["yang_per_kalimat_maks"],
        f"S9 'yang' terlalu rapat: {m['yang_per_kalimat']} > {AMBANG['yang_per_kalimat_maks']} per kalimat")
    return langgar


# ----------------------------------------------------------------------------
# 6. SKOR
# ----------------------------------------------------------------------------
def hitung_asi(temuan_r, temuan_l, temuan_s, langgar, jumlah_kata):
    per_seribu = 1000.0 / max(1, jumlah_kata)
    skor = 0.0
    for kelompok in (temuan_r, temuan_l, temuan_s):
        for t in kelompok:
            skor += t["bobot"] * t["jumlah"] * per_seribu
    skor += 3.0 * len(langgar)
    return round(min(100.0, skor), 1)


def verdikt(asi, blocker):
    if blocker:
        return "MERAH (BLOCKER)", "Jangan kirim ke pembimbing. Bersihkan seluruh temuan blocker lebih dulu."
    if asi <= 12:
        return "HIJAU", "Siap dibaca pembimbing. Lanjut ke uji baca nyaring."
    if asi <= AMBANG["asi_maks"]:
        return "KUNING", "Layak, tetapi rapikan temuan berbobot tinggi sebelum bimbingan."
    return "MERAH", "Naskah masih berpola mesin. Jalankan protokol tulis ulang per paragraf."


# ----------------------------------------------------------------------------
# 7. LAPORAN
# ----------------------------------------------------------------------------
def laporkan(nama_berkas, data, batas_contoh):
    garis = "=" * 78
    print(garis)
    print(f"BERKAS : {nama_berkas}")
    print(garis)
    m = data["metrik"]
    if m is None:
        print("Tidak ada prosa yang dapat dianalisis.")
        return
    print(f"AI-SLOP INDEX : {data['asi']}  ->  {data['verdikt'][0]}")
    print(f"{data['verdikt'][1]}")
    print()
    print(f"Korpus  : {m['jumlah_paragraf']} paragraf, {m['jumlah_kalimat']} kalimat, {m['jumlah_kata']} kata")
    print(f"Irama   : rerata {m['rerata_panjang_kalimat']} kata, SD {m['sd_panjang_kalimat']}, "
          f"CV {m['cv_panjang_kalimat']}, kalimat pendek {int(m['rasio_kalimat_pendek']*100)}%")
    print(f"Sintaks : nominalisasi {m['densitas_nominalisasi']}, pasif {m['rasio_pasif']}, "
          f"'yang'/kalimat {m['yang_per_kalimat']}, MATTR {m['mattr_50']}")
    print()

    if data["blocker"]:
        print("--- BLOCKER (wajib nol) ---")
        for t in data["blocker"]:
            print(f"  [{t['jumlah']:>3}x] {t['nama']}")
            for c in t["contoh"]:
                print(f"         baris {c['baris']:>5} | ...{c['cuplikan']}...")
        print()

    for judul, kunci in (("RETORIS", "retoris"), ("LEKSIKAL", "leksikal"),
                         ("SINTAKSIS", "sintaksis"), ("KALIMAT EFEKTIF", "kalimat"),
                         ("EJAAN", "ejaan")):
        if data[kunci]:
            print(f"--- {judul} ---")
            for t in sorted(data[kunci], key=lambda x: -x["bobot"] * x["jumlah"]):
                print(f"  [{t['jumlah']:>3}x] (bobot {t['bobot']}) {t['nama']}")
                for c in t["contoh"][:batas_contoh]:
                    print(f"         baris {c['baris']:>5} | ...{c['cuplikan']}...")
            print()

    d = data.get("densitas")
    if d:
        print("--- DENSITAS INFORMASI DAN STRUKTUR (taksonomi Shaib dkk. 2025) ---")
        print(f"  densitas gagasan   : {d['densitas_gagasan']}   (makin tinggi makin padat isi)")
        print(f"  compression ratio  : kata {d['cr_kata']} | POS {d['cr_pos']}   (makin tinggi makin repetitif)")
        print(f"  templat per token  : {d['templat_per_token']}   (proporsi token dalam templat sintaksis berulang)")
        print(f"  simetri pembuka    : {d['simetri_pembuka']}")
        if data["metrik"] and data["metrik"]["jumlah_kata"] < AMBANG_D["kata_minimum_struktur"]:
            print(f"  (korpus {data['metrik']['jumlah_kata']} kata: cr dan templat belum stabil, "
                  f"baca sebagai indikasi saja)")
        print(f"  diksi evaluatif    : {d['proporsi_subjektif']} | hedging {d['proporsi_hedge']}")
        if d["contoh_templat"]:
            print("  templat tersering  :")
            for pola, n in d["contoh_templat"]:
                print(f"      {n}x  {pola}")
        if d["contoh_simetri"]:
            print("  kalimat sepola     :")
            for c in d["contoh_simetri"]:
                print(f"      {c}")
        print()

    if data["pelanggaran_ambang"]:
        print("--- IRAMA DAN AMBANG KUANTITATIF ---")
        for p in data["pelanggaran_ambang"]:
            print(f"  ! {p}")
        print()


def audit(path, batas_contoh, baseline=None):
    teks = Path(path).read_text(encoding="utf-8", errors="replace")
    teks = unicodedata.normalize("NFC", teks)
    prosa, _ = muat_prosa(teks)

    blocker = jalankan_kelompok(teks, POLA_BLOCKER, batas_contoh, berbobot=False)
    retoris = jalankan_kelompok(prosa, POLA_RETORIS, batas_contoh)
    leksikal = jalankan_kelompok(prosa, POLA_LEKSIKAL, batas_contoh)
    sintaksis = jalankan_kelompok(prosa, POLA_SINTAKSIS, batas_contoh)
    kalimat_ef = jalankan_kelompok(prosa, POLA_KALIMAT, batas_contoh)
    ejaan = jalankan_kelompok(prosa, POLA_EJAAN, batas_contoh)

    metrik = hitung_metrik(prosa)
    langgar = periksa_ambang(metrik) if metrik else []
    densitas = metrik_densitas(prosa)
    if densitas:
        langgar = langgar + periksa_ambang_d(densitas, baseline)
    asi = hitung_asi(retoris + kalimat_ef + ejaan, leksikal, sintaksis, langgar,
                     metrik["jumlah_kata"] if metrik else 1)
    return {
        "berkas": str(path),
        "asi": asi,
        "verdikt": verdikt(asi, blocker),
        "blocker": blocker,
        "retoris": retoris,
        "leksikal": leksikal,
        "sintaksis": sintaksis,
        "kalimat": kalimat_ef,
        "ejaan": ejaan,
        "metrik": metrik,
        "densitas": densitas,
        "pelanggaran_ambang": langgar,
    }


def main():
    ap = argparse.ArgumentParser(description="Auditor AI-Slop naskah tugas akhir")
    ap.add_argument("berkas", nargs="+")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    ap.add_argument("--show", type=int, default=4, help="jumlah contoh per temuan")
    ap.add_argument("--calibrate", action="store_true",
                    help="bangun garis dasar pribadi dari berkas yang diberikan "
                         "(pakai tulisan lama Anda sendiri), tulis ke .slop_baseline.json")
    ap.add_argument("--baseline", default=".slop_baseline.json",
                    help="berkas garis dasar pribadi yang dipakai saat audit")
    args = ap.parse_args()

    if args.calibrate:
        nilai = {}
        for b in args.berkas:
            p = Path(b)
            if not p.exists():
                continue
            prosa, _ = muat_prosa(p.read_text(encoding="utf-8", errors="replace"))
            d = metrik_densitas(prosa)
            m = hitung_metrik(prosa)
            if not d or not m:
                continue
            print(f"  {p.name:<40} kata={m['jumlah_kata']:<6} "
                  f"gagasan={d['densitas_gagasan']} cr_pos={d['cr_pos']} "
                  f"tpt={d['templat_per_token']}")
            for k in ("densitas_gagasan", "cr_pos", "templat_per_token"):
                nilai.setdefault(k, []).append(d[k])
        if not nilai:
            print("tidak ada berkas yang dapat dinilai", file=sys.stderr)
            sys.exit(1)
        garis_dasar = {k: round(statistics.median(v), 4) for k, v in nilai.items()}
        Path(args.baseline).write_text(
            json.dumps(garis_dasar, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nGaris dasar pribadi ditulis ke {args.baseline}: {garis_dasar}")
        print("Audit berikutnya akan membandingkan naskah baru terhadap kebiasaan menulis Anda,")
        print("bukan terhadap angka mutlak yang tidak bermakna lintas panjang teks.")
        sys.exit(0)

    baseline = None
    if Path(args.baseline).exists():
        try:
            baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        except Exception:
            baseline = None

    semua, gagal = [], False
    for b in args.berkas:
        p = Path(b)
        if not p.exists():
            print(f"[lewat] berkas tidak ditemukan: {b}", file=sys.stderr)
            continue
        d = audit(p, args.show, baseline)
        semua.append(d)
        if d["blocker"] or d["asi"] > AMBANG["asi_maks"]:
            gagal = True
        if not args.json:
            laporkan(p.name, d, args.show)

    if args.json:
        print(json.dumps(semua, ensure_ascii=False, indent=2))
    sys.exit(1 if gagal else 0)


if __name__ == "__main__":
    main()
