# DESLOP_AGENT.md : Prosedur Operasi Agen De-Slopping

> Berkas ini adalah instruksi kerja untuk agen AI (opencode, Claude Code, atau sejenisnya)
> yang menyunting naskah skripsi di repositori ini. Agen wajib membaca
> `ANTI_AI_SLOP_GUARD.md` lebih dahulu, lalu menjalankan prosedur di bawah.
> Agen tidak diperkenankan menyunting naskah tanpa menjalankan Gerbang 1 dan Gerbang 4.

---

## 0. Kontrak Tunggal

Tugas agen bukan menulis ulang skripsi. Tugas agen adalah **memindahkan gaya bahasa
dari pola mesin ke pola penulis manusia, dengan substansi terkunci 100 persen**.

Satu kalimat keputusan: **bila sebuah suntingan mengubah apa yang diketahui pembaca
setelah membaca paragraf itu, suntingan tersebut salah, sebagus apa pun bunyinya.**

---

## 1. Persiapan Sekali Jalan

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r tools/requirements.txt

# Berkas istilah terkunci (sunting bila ada istilah baru)
python tools/invariant_check.py --init-terms tools/terms.json

# Garis dasar gaya pribadi, dibangun dari tulisan LAMA Anda sendiri
# (laporan PKL, makalah kuliah, proposal lama, apa pun yang Anda tulis sendiri)
python tools/slop_audit.py --calibrate tulisan_lama/*.md
python tools/deep_audit.py --calibrate tulisan_lama/*.md    # opsional, perlu torch
```

Garis dasar itu penting. Tanpa garis dasar, agen mengejar angka mutlak yang tidak
bermakna. Dengan garis dasar, agen mengejar **kebiasaan menulis Anda sendiri**.

---

## 2. Siklus Kerja Per Berkas

Agen menjalankan siklus berikut untuk satu berkas naskah, satu subbab per iterasi.
Dilarang memproses seluruh bab sekaligus. Pemrosesan borongan adalah asal-muasal
*splice glitch* (Kasus 2 pada guard).

```
GERBANG 1  audit awal        -> tahu apa yang salah dan di baris berapa
GERBANG 2  tulis ulang       -> delapan lintasan, satu paragraf per satu paragraf
GERBANG 3  audit ulang       -> pastikan pola mesin turun
GERBANG 4  kontrak invarian  -> pastikan substansi utuh (WAJIB, tidak boleh dilewati)
GERBANG 5  laporan           -> tulis ringkasan perubahan untuk penulis
```

### Gerbang 1: Audit awal

```bash
cp REVISI_BAB_1.md .deslop/REVISI_BAB_1.before.md
python tools/slop_audit.py REVISI_BAB_1.md --show 6
python tools/deep_audit.py REVISI_BAB_1.md --topk 12     # bila torch tersedia
```

Agen membaca keluarannya dan menyusun daftar kerja berisi: nomor baris, kode guard,
dan kalimat sasaran. `deep_audit.py` memberi urutan prioritas, yaitu kalimat paling
datar secara probabilitas. Kerjakan dari nomor satu.

### Gerbang 2: Tulis ulang, delapan lintasan

Untuk **setiap paragraf**, berurutan, jangan melompat:

| Lintasan | Tindakan | Guard |
|---|---|---|
| 1 | Catat semua angka, nama, istilah terkunci, sitasi pada paragraf itu | Kontrak Invarian |
| 2 | Perbaiki kalimat pembuka menjadi fakta entitas riil | G-05 |
| 3 | Potong ekor mesin (", sehingga memastikan", "yang mana", rantai "hal ini") | G-17, G-18, G-19 |
| 4 | Perbaiki struktur kalimat (subjek, konjungsi ganda, keparalelan) | G-39, G-41 |
| 5 | Bersihkan pemborosan dan verba hampa | G-40 |
| 6 | Atur irama, pastikan ada kalimat pendek baku | G-07 |
| 7 | Buang kalimat rekap penutup | G-14 |
| 8 | Periksa register dan ejaan EYD V | G-31 sampai G-38 |

Aturan keras selama Gerbang 2:

1. **Satu paragraf masuk, satu paragraf keluar.** Jumlah paragraf tidak berubah.
2. **Dilarang menambah kalimat yang tidak membawa fakta baru.** Bila paragraf terasa
   kurang, jangan menambah kata sifat. Laporkan ke penulis bahwa paragraf itu
   membutuhkan data, lalu lanjut.
3. **Dilarang mengganti angka, nama, atau istilah terkunci** dengan alasan apa pun.
4. **Dilarang menurunkan register.** Padanan baku ada pada Lampiran A.2 guard.
5. **Dilarang menyisipkan kesalahan** ejaan atau gramatika agar tampak manusiawi.
6. Bila agen ragu antara dua rumusan, pilih yang lebih konkret, bukan yang lebih indah.

### Gerbang 3: Audit ulang

```bash
python tools/slop_audit.py REVISI_BAB_1.md --show 4
```

Target: nol temuan BLOCKER, ASI turun di bawah 25, ideal di bawah 12. Bila masih
merah, kembali ke Gerbang 2 pada paragraf yang ditunjuk. Maksimum tiga putaran.
Bila setelah tiga putaran tetap merah, hentikan dan laporkan ke penulis. Memutar
lebih dari tiga kali biasanya berarti masalahnya bukan gaya, melainkan data.

### Gerbang 4: Kontrak invarian (tidak boleh dilewati)

```bash
python tools/invariant_check.py .deslop/REVISI_BAB_1.before.md REVISI_BAB_1.md \
    --terms tools/terms.json
```

* Exit code 0 berarti substansi aman, pekerjaan boleh diserahkan.
* Exit code 1 berarti ada temuan berat. **Agen wajib mengembalikan berkas ke keadaan
  semula** (`git checkout -- REVISI_BAB_1.md` atau salin ulang dari `.before.md`),
  lalu mengulang Gerbang 2 dengan lebih konservatif. Dilarang menyerahkan hasil yang
  gagal Gerbang 4, walaupun skor ASI-nya bagus.

### Gerbang 5: Laporan

Agen menulis `.deslop/REVISI_BAB_1.report.md` berisi:

1. ASI sebelum dan sesudah.
2. Daftar temuan yang diperbaiki, dikelompokkan per kode guard.
3. Daftar paragraf yang **tidak** disentuh beserta alasannya.
4. Daftar paragraf yang membutuhkan tambahan data dari penulis (paragraf abstrak yang
   tidak bisa dikonkretkan tanpa fakta baru). Ini bagian terpenting bagi penulis.
5. Hasil Gerbang 4, disalin apa adanya.

---

## 3. Prompt Sistem untuk Agen

Tempelkan ini sebagai system prompt agen penyunting.

```
Anda menyunting naskah skripsi Teknik Informatika berbahasa Indonesia milik penulis.
Wajib patuh pada ANTI_AI_SLOP_GUARD.md di repositori ini.

TUJUAN: menghapus pola gaya mesin, mempertahankan substansi 100 persen,
menjaga ragam ilmiah resmi bahasa Indonesia sesuai EYD Edisi V.

HARAM BERUBAH: struktur bab dan subbab, urutan dan jumlah paragraf, seluruh angka,
satuan, nama entitas, nama narasumber, kode F1-F6 dan RM1-RM3, nomor tabel dan gambar,
seluruh sitasi, serta istilah terkunci (outbox, idempotency key, Monolith Terpusat,
EDA Tanpa Proteksi, EDA dengan Proteksi, konsistensi data, recovery window).

DILARANG (pola mesin):
"bukan X melainkan Y" dan variannya; rangkaian tiga sejajar yang dipaksakan;
ekor partisipial ", sehingga memastikan / menghasilkan / mencerminkan";
"yang mana"; lebih dari satu "hal ini" per paragraf; kalimat rekap penutup paragraf;
puffery (krusial, fundamental, holistik, komprehensif, robust, optimal, signifikan);
sisipan editorial (patut digarisbawahi, menariknya); pertanyaan retoris;
atribusi kabur tanpa sitasi; em dash; kutip melengkung; boldface dekoratif;
kata "efektivitas"; label Kondisi/Artefak A/B/C; istilah DSRM; statistik inferensial.

DILARANG (register turun): memakai, lewat, bikin, ketahuan, kelihatan, dipakai,
kayak, banget, nggak, tapi di awal kalimat, terus sebagai konektor, saya, kami, kita, Anda.
Gunakan: menggunakan, melalui, membuat, teridentifikasi, tampak, digunakan, seperti,
sangat, tidak, tetapi, kemudian, peneliti.

DILARANG (kaidah): kata depan di/ke/dari ditulis serangkai; awalan di- ditulis terpisah;
"di mana" atau "dimana" sebagai penanda klausa relatif; kalimat tanpa subjek
("Dalam penelitian ini membandingkan ..."); konjungsi ganda ("Karena ... sehingga ...");
pemborosan (adalah merupakan, agar supaya, disebabkan karena, sangat ... sekali);
bentuk takbaku (analisa, praktek, resiko, sistim, obyek, merubah, apotik).

DILARANG JUGA: menambah kalimat tanpa fakta baru, menyisipkan salah ketik yang disengaja,
menurunkan tingkat keformalan, dan mengarang angka atau sitasi baru.

JANGAN DIHAPUS (konvensi skripsi Indonesia yang sah): "Penelitian ini bertujuan untuk",
"Berdasarkan latar belakang tersebut", "Rumusan masalah dalam penelitian ini adalah",
"Batasan masalah meliputi", "Hasil wawancara dengan Ibu Atik menunjukkan",
"Tahapan penelitian ditunjukkan pada Gambar", "Bab ini menguraikan".

WAJIB: kalimat pembuka paragraf memuat fakta entitas riil; variasi panjang kalimat
dengan minimal satu kalimat di bawah 15 kata per paragraf yang tetap baku dan
berpredikat lengkap; setiap tiga baris prosa teknis memuat minimal satu elemen konkret
(nama tabel, nama layanan, kode gangguan, satuan, atau angka).

KELUARAN: hanya naskah hasil suntingan. Tanpa pengantar, tanpa penutup, tanpa penjelasan,
tanpa ringkasan perubahan, tanpa tawaran bantuan lanjutan.
```

---

## 4. Perintah Ringkas

```bash
make audit          # slop_audit pada seluruh REVISI_*.md
make deep           # deep_audit pada seluruh REVISI_*.md (perlu torch)
make check          # invariant_check seluruh pasangan before/after di .deslop/
make calibrate      # bangun garis dasar dari tulisan_lama/
make all            # audit lalu check
```

---

## 5. Kapan Agen Harus Berhenti dan Bertanya

Agen berhenti, tidak menebak, dan melaporkan ke penulis bila menemukan salah satu dari:

1. Paragraf yang tidak dapat dikonkretkan tanpa data yang belum ada.
2. Klaim tanpa sitasi yang tidak dapat ditelusuri ke sumber di repositori.
3. Angka yang saling bertentangan antarbagian naskah.
4. Istilah teknis baru yang belum ada pada `terms.json`.
5. Gerbang 4 gagal tiga kali berturut-turut pada berkas yang sama.
6. Permintaan penulis yang berbenturan dengan Kontrak Invarian.

Menebak pada keenam situasi itu menghasilkan naskah yang lolos audit tetapi gugur
di ruang sidang. Bertanya selalu lebih murah.
