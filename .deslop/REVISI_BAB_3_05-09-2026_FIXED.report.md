# Laporan De-Slopping Bab 3 (Gerbang 5)

Berkas: `documents/REVISI_BAB_3_05-09-2026_FIXED.md`
Pembanding: `.deslop/REVISI_BAB_3_05-09-2026_FIXED.before.md`
Tanggal: 2026-09-18

## 1. ASI sebelum / sesudah
- Sebelum: 16.3 MERAH (BLOCKER B3/B8/B9/B11)
- Sesudah: 12.8, BLOCKER tersisa hanya B3/B9 (mermaid) + B8 (disclaimer inferensial) yang false positive/by-design (lihat butir 3)
- Korpus: 74 paragraf, 183 -> 188 kalimat, 4302 -> 4307 kata
- Irama: kalimat pendek 31% -> 33%, CV 0.856 -> 0.863

## 2. Temuan per kode guard (diperbaiki)
- G-31/B11 (register, 2x): "basis data yang dipakai bersama" -> "yang digunakan bersama"; "pemberitahuan lewat event" -> "melalui event".
- G-04/R1: "yang dibandingkan ... bukan hasil tiap permintaan ... melainkan kondisi akhir satu run" -> deklaratif ("satuan yang dibandingkan ... adalah kondisi akhir satu run secara utuh ... Hasil tiap permintaan secara terpisah tidak dibandingkan karena ... saling memengaruhi").
- G-19/S3 (4x): "Pada kondisi ini" -> "Pada kondisi kedua"; "Kondisi ini berfungsi" -> "Susunan tersebut berfungsi"; "Kondisi ini mengukur" -> "Kondisi kedua mengukur"; "Kondisi ini menguji" -> "Kondisi ketiga menguji".
- G-39/K3 (konjungsi ganda, 2x): "karena ... sehingga ..." (pilot test; split-brain) -> kalimat terpisah tanpa konjungsi ganda.

## 3. Paragraf tak disentuh + alasan
- Blok ```mermaid x3 (Gambar 3.1/3.2/3.3) + baris "class ..."/"ass N1..." (B3/B9): TIDAK dihapus (sumber diagram; render saat kompilasi `.docx`).
- B8 (Friedman/Wilcoxon, §3.3.3): dipertahankan. Konteksnya larangan eksplisit ("bukan uji signifikansi ... seperti uji Friedman atau Wilcoxon"), justru bukti kepatuhan G-10 (statistik deskriptif non-inferensial). Menghapusnya menghilangkan jejak keputusan metodologis.
- S1 ("menghasilkan 25 sel perlakuan"): dipertahankan. Itu predikat aritmetika faktual (15+10=25), bukan ekor partisipial kosong.
- R2 (9x): daftar berjumlah faktual (4 domain, 4 dimensi, 5 tahap, 4 skenario, 4 layanan) + baris tabel. Jumlah objek terkunci; variasi artifisial = pemalsuan.
- I5 (8,5%), S7 (0,0775), S8 (0,421): sedikit di atas ambang, diterima. Metodologi terkendali menuntut kalimat pasif (objektivitas, Koreksi-2 guard) dan istilah -an terkunci; ambang S8 (0,42) terlampaui 0,001.

## 4. Paragraf butuh data penulis
- Nihil. Seluruh parameter (60 detik warm-up/recovery window, 10/50/100 req/s, 30 blok, 3.330 run, Tabel 3.1-3.10, F1-F6) sudah terkunci di naskah.

## 5. Gerbang 4 apa adanya
- `invariant_check.py --terms terms.json`: HIJAU murni. "Substansi bertahan 100 persen. Perubahan murni bergaya bahasa."
- Paragraf 84->84, heading 14->14, angka 71->71, sitasi 0->0.
