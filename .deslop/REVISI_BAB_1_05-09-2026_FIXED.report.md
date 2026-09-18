# Laporan De-Slopping Bab 1 (Gerbang 5)

Berkas: `documents/REVISI_BAB_1_05-09-2026_FIXED.md`
Pembanding: `.deslop/REVISI_BAB_1_05-09-2026_FIXED.before.md`
Tanggal: 2026-09-18

## 1. ASI sebelum / sesudah
- Sebelum: 18.0 MERAH (BLOCKER B1)
- Sesudah: 8.6 HIJAU (ideal <= 12 terpenuhi)
- Korpus: 15 paragraf, 63 -> 71 kalimat, 1613 -> 1596 kata
- Irama: kalimat pendek 15% -> 22%, CV 0.644 -> 0.687

## 2. Temuan per kode guard (diperbaiki)
- G-01/B1 (BLOCKER): "Berangkat dari kebutuhan dijelaskan kebutuhannya apa" -> "Untuk memenuhi kebutuhan integrasi tersebut". Prompt leakage terhapus.
- G-02/B9 (BLOCKER): splice "Ibu Atik, tiga, Berdasarkan hasil wawancara dan pengamatan apotek" -> kalimat tunggal bersih dengan pemilik + wawancara + pengamatan dipertahankan.
- G-04/R1: kontras retoris pembuka "bukan lagi apakah ... melainkan apakah" -> deklaratif dua kalimat pendek ("Kemampuan sistem pencatatannya sanggup menampung ... jarang menjadi hambatan utama. Keterpercayaan catatan ... menentukan apakah sistem masih dapat dipercaya.").
- G-06/L2: "Dalam konteks ini," -> "Penelitian ini mendefinisikan"; bold dekoratif "**penyajian informasi**" -> polos.
- G-07/S3: "Kedua kondisi ini" -> "Keduanya".
- G-12/G-25: "*monolith* terpusat" -> "Monolith Terpusat" (istilah terkunci).
- G-15/E6: "antar sistem" -> "antarsistem".
- G-17/G-39/G-40: verba hampa + kalimat >40 kata dipecah ("secara alami", "bertumpu pada", "saling menukar" disederhanakanSTART; struktur S-P ditegaskan).
- G-37: "apotek bisma" -> "Apotek Bisma"; "Selisih" setelah "bahwa" -> "selisih".

## 3. Paragraf tak disentuh + alasan
- 1.2 Identifikasi Masalah (5 butir), 1.3 Batasan Masalah (6 butir), 1.4 Rumusan Masalah (3 butir), 1.5 Tujuan (3 butir), 1.6 Manfaat (2+3 butir): tidak disentuh. Butir-butir konvensi skripsi ringkas, padat fakta, nol temuan BLOCKER. Mengubahnya berisiko merusak paralelisme RM-tujuan dan traceability judul.
- R2 trikolon (6x) disengaja dipertahankan: seluruhnya daftar 4 unsur faktual (4 domain: transaksi/persediaan/pembayaran/pelaporan; 4 dimensi: konsistensi/keandalan/performa/kompleksitas). Bukan trikolon mekanis; memecahnya memalsukan jumlah objek.
- S7 nominalisasi 0.0952 (> 0.075) diterima: didorong istilah terkunci berakhiran -an (pencatatan, persediaan, pembayaran, pelaporan, konsistensi, keandalan). Menurunkannya berarti menyinonimkan istilah terkunci (melanggar G-25).

## 4. Paragraf butuh data penulis
- Nihil. Seluruh paragraf 1.1 dapat dikonkretkan dari fakta yang sudah ada (450 transaksi/hari, tiga cabang + satu gudang, Kabupaten Mojokerto, Ibu Atik).

## 5. Gerbang 4 apa adanya
- `invariant_check.py --terms terms.json`: HIJAU dengan catatan, 4 temuan ringan, nol berat. Paragraf 15->15, heading 9->9, angka 3->3, sitasi 1->1.
- 4 ringan = diksi slop yang memang wajib dibuang: bingkai retoris "pertanyaan mendasar ... muncul" (G-04), "saling/akibat/meningkatnya" (G-40), "alami/bertumpu/efisiensi" (filler). Subjek, angka, nama, sitasi, istilah terkunci utuh.
- Catatan alat: pola "kondisi arsitektur" sempat memicu false positive "Kondisi A" (pencocokan substring tanpa batas kata); dihindari dengan diksi "Kedua kondisi tersebut" -> "Keduanya".
