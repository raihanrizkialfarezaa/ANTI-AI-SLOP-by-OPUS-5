# Laporan De-Slopping Bab 2 (Gerbang 5)

Berkas: `documents/REVISI_BAB_2_05-09-2026_FIXED.md`
Pembanding: `.deslop/REVISI_BAB_2_05-09-2026_FIXED.before.md`
Tanggal: 2026-09-18

## 1. ASI sebelum / sesudah
- Sebelum: 8.5 MERAH (BLOCKER B3/B9/B11/B14)
- Sesudah: 4.3, BLOCKER tersisa hanya B3/B9 di dalam blok mermaid (false positive, lihat butir 3)
- Korpus: 32 paragraf, 93 -> 95 kalimat, 2266 -> 2272 kata
- Irama: kalimat pendek 26% -> 29%, CV 0.70 -> 0.709

## 2. Temuan per kode guard (diperbaiki)
- G-04/R1: "bukan menuntut angka ... melainkan apakah setelah ..." -> 4 kalimat deklaratif ("Ukuran keberhasilan ... adalah keadaan data setelah seluruh pesan selesai diproses. Penelitian ini tidak menuntut angka ... sama persis pada setiap detik. ... Inilah yang disebut *konsistensi data*.").
- G-13/L1: "evaluasi komprehensif" -> "evaluasi" (puffery dibuang, cakupan empat dimensi tetap disebut eksplisit).
- G-19/S3 (3x): "Hal ini membuat *monolith*" -> "Susunan tunggal tersebut membuat"; "mengatasi hal ini" -> "mengatasi risiko kehilangan pesan tersebut"; "Hal ini mencegah dua kasir" -> "Penolakan tertib tersebut mencegah dua kasir".
- G-31/B11 (register): "yang dipakai" -> "yang digunakan".
- G-33/B14 (kebakuan): "standarisasi" (2x, Tab. 2.1 + §2.2) -> "standardisasi".

## 3. Paragraf tak disentuh + alasan
- Blok ```mermaid (Gambar 2.1) + baris "class ..." (B3/B9): TIDAK dihapus. Itu sumber diagram kerangka berpikir; GUARD 9 memerintahkan pembersihan hanya saat kompilasi `.docx` (render PNG/SVG), bukan di sumber `.md`. Menghapusnya menghancurkan Gambar 2.1.
- R2 (2x): daftar 4 layanan (Penjualan/Persediaan/Pembayaran/Pelaporan) dan 4 dimensi evaluasi. Jumlah objek memang empat; bukan trikolon.
- §2.1.1-§2.1.4 mekanisme (outbox/inbox/OCC/saga/broker): selain anafora di atas, tidak disentuh. Definisi + sitasi (Richardson 2018; Yadav & Mantri 2024; Kung & Robinson 1981; Garcia-Molina & Salem 1987; Karabey Aksakalli et al. 2021) sudah konkret dan terkunci.
- I5 kalimat >40 kata (15,8%): diterima. Penjelas mekanisme lintas-layanan membutuhkan klausa lengkap; pemecahan agresif memicu risiko invarian tanpa menambah fakta.

## 4. Paragraf butuh data penulis
- Nihil. Tidak ada klaim yang membutuhkan fakta lapangan baru.

## 5. Gerbang 4 apa adanya
- `invariant_check.py --terms terms.json`: HIJAU murni. "Substansi bertahan 100 persen. Perubahan murni bergaya bahasa."
- Paragraf 33->33, angka 27->27, sitasi 11->11.
