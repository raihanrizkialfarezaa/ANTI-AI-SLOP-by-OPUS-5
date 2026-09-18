# ANTI_AI_SLOP_GUARD v4.0 : Standar Anti-AI Slop dari Lapis Token sampai Lapis Wacana

> **Status:** Mengikat (*Mandatory Guard*) untuk seluruh draf naskah tugas akhir/skripsi (Bab I, II, III, dan seterusnya) di repositori ini.
> **Konteks:** Ditetapkan berdasarkan evaluasi kritis pembimbing (**Dr. I Made Suartana, S.Kom., M.Kom.**), audit forensik atas residu teks dan glitch regenerasi pada naskah Apotek Bisma, temuan empiris stilometri 2024 sampai 2026 tentang pembeda terukur antara prosa manusia dan prosa model bahasa, serta kaidah **EYD Edisi V**, **kalimat efektif**, dan **ragam bahasa ilmiah** sebagaimana dirumuskan dalam literatur pengajaran bahasa Indonesia (Lampiran E).
> **Guard Pendamping:** `FORMAT_GUARD.md` (tata tulis dan tipografi A5) dan `DOCX_GUARD.md` (ketertelusuran berkas).
> **Alat Pendamping:**
> `tools/slop_audit.py` (auditor sembilan dimensi, tanpa dependensi, wajib dijalankan sebelum bimbingan),
> `tools/invariant_check.py` (penjaga substansi 100 persen, wajib dijalankan setelah setiap suntingan),
> `tools/deep_audit.py` (audit lapis probabilitas token berbasis Fast-DetectGPT dan Uniform Information Density, opsional, memerlukan torch),
> `DESLOP_AGENT.md` (prosedur operasi agen AI di opencode), `Makefile`, `tools/terms.json`.
> **Versi:** 4.0. Menggantikan v3.0 secara penuh. Penomoran guard lama dipertahankan (G-01 sampai G-48), lalu diperluas sampai G-60.

---

## 0. Perubahan dari v2.0 ke v3.0

v2.0 menangani pola mesin berbahasa Inggris yang diterjemahkan ke bahasa Indonesia. v2.0 belum menangani satu hal yang justru dinilai pertama kali oleh penguji, yaitu **kepatuhan pada ragam ilmiah bahasa Indonesia**.

| Aspek | v2.0 | v3.0 |
|---|---|---|
| Lapis kebahasaan | Leksikal, retoris, sintaksis, irama, tipografi | Ditambah lapis **ejaan (EYD V)**, **kalimat efektif**, **kebakuan diksi**, dan **register ilmiah** |
| Jumlah guard | 30 | 48 |
| Risiko over-koreksi | Belum ditangani | Ditambah **Daftar Putih Konvensi Skripsi** (GUARD 19) dan **Larangan Pemalsuan Kemanusiaan** (GUARD 20) |
| Rujukan | 6 sumber stilometri | Ditambah 8 sumber kebahasaan Indonesia (Lampiran E) |
| Auditor | 5 dimensi | Ditambah dimensi **E** (ejaan), **K** (kalimat efektif), **N** (nonbaku) |

### 0.0. Perubahan dari v3.0 ke v4.0

v3.0 berhenti pada pola yang dapat dilihat mata, yaitu diksi, kalimat, paragraf, dan ejaan.
v4.0 turun satu lapis lagi, ke tempat pola itu sebenarnya lahir, yaitu distribusi
probabilitas token pada saat teks dihasilkan.

| Aspek | v3.0 | v4.0 |
|---|---|---|
| Lapis terdalam | Ejaan dan kalimat | Ditambah **lapis probabilitas token** (curvature, surprisal, prediktabilitas) |
| Dasar taksonomi slop | Daftar ciri komunitas | Ditambah **taksonomi akademik Shaib dkk. (2025)**: Information Utility, Information Quality, Style Quality |
| Metrik struktur | Panjang kalimat dan paragraf | Ditambah **compression ratio**, **templates-per-token**, **propositional idea density**, **simetri paralel**, **proporsi subjektivitas** |
| Jaminan substansi | Prosedur manual (`git diff`) | Ditambah **`invariant_check.py`**, penolakan otomatis bila satu angka saja menguap |
| Kalibrasi | Ambang mutlak | Ditambah **garis dasar gaya pribadi** dari tulisan lama penulis sendiri |
| Otomasi | Skrip audit | Ditambah **prosedur agen lima gerbang** (`DESLOP_AGENT.md`) |
| Bibliografi | 14 rujukan | Ditambah **verifikasi metadata**, tiga kekeliruan sitasi dikoreksi (Lampiran F) |
| Jumlah guard | 48 | 60 |

### 0.1. Dua koreksi atas kesalahan v2.0 (wajib dibaca)

**Koreksi 1: penurunan register bukan humanisasi.**
v2.0 menganjurkan pengganti seperti *memakai*, *lewat*, *ketahuan*, dan *bikin*. Anjuran itu **dicabut**. Kata-kata tersebut tergolong ragam takresmi atau ragam percakapan, sehingga menurunkan naskah dari ragam ilmiah ke ragam populer. Penguji akan menandainya sebagai kesalahan berbahasa, bukan sebagai tanda kemanusiaan.

> **Aturan induk v3.0:** naskah dibuat terasa ditulis manusia melalui **kekonkretan fakta** dan **variasi struktur kalimat**, bukan melalui penurunan tingkat keformalan. Register tetap di ragam ilmiah resmi sepanjang naskah, dari kalimat pertama sampai kalimat terakhir.

Padanan yang benar ada di **Lampiran A.2**. Contoh: *memakai* menjadi **menggunakan**, *lewat* menjadi **melalui**, *ketahuan* menjadi **teridentifikasi** atau **terdeteksi**, *bikin* menjadi **membuat**, *dipakai* menjadi **digunakan**, *ngecek* menjadi **memeriksa**.

**Koreksi 2: kalimat pasif bukan cacat.**
v2.0 menganjurkan pemakaian verba aktif bila pelakunya jelas. Anjuran itu **dibatasi**. Ragam ilmiah bahasa Indonesia justru bertumpu pada kalimat pasif dan kata ganti impersonal demi objektivitas. Yang menjadi penanda mesin bukan kepasifan itu sendiri, melainkan **pasif tanpa pelaku yang ditumpuk dengan nominalisasi berlapis**, misalnya *"dilakukan pelaksanaan pengujian terhadap penerapan mekanisme"*. Ambang rasio pasif dinaikkan dari 0,42 menjadi 0,55, dan fokus dipindahkan ke GUARD 16 (nominalisasi) serta GUARD 17 (kesepadanan struktur).

---

## 1. Kontrak Invarian Revisi (Aturan Nol Perubahan)

Setiap kali naskah disentuh untuk keperluan de-slopping, berlaku kontrak berikut. Pelanggaran kontrak ini lebih berat daripada AI slop itu sendiri, karena merusak substansi ilmiah.

**YANG HARAM BERUBAH:**

1. **Struktur.** Nomor bab, urutan subbab, judul subbab, urutan paragraf, dan jumlah paragraf per subbab tetap. Satu paragraf masuk, satu paragraf keluar.
2. **Substansi.** Klaim, temuan, angka, satuan, nama entitas, nama narasumber, kode gangguan (F1 sampai F6), nama metrik, dan nama arsitektur tidak boleh bergeser maknanya sedikit pun.
3. **Sitasi.** Jumlah, penempatan, dan pemilik sitasi tetap. Pemindahan sitasi ke kalimat lain hanya karena kalimat dipecah tidak diperkenankan, kecuali sitasi tetap melekat pada klaim yang sama.
4. **Terminologi.** Istilah teknis yang telah dikunci tidak boleh disinonimkan (GUARD 12).
5. **Nomor objek.** Nomor tabel, nomor gambar, nomor persamaan, dan rujukan silang terhadap nomor tersebut tetap.
6. **Register.** Tingkat keformalan tidak boleh turun. Naskah tetap berada pada ragam ilmiah resmi (GUARD 15).

**YANG BOLEH DAN WAJIB BERUBAH:**

Diksi (selama tetap baku), panjang kalimat, batas antarkalimat di dalam satu paragraf, urutan klausa di dalam satu kalimat, pemilihan bentuk aktif atau pasif, konektor antarkalimat, dan pola pembuka paragraf.

**Uji kepatuhan kontrak:** setelah revisi, jalankan `git diff --word-diff`. Setiap angka, nama, dan sitasi yang hilang di sisi kiri wajib muncul kembali di sisi kanan. Apabila terdapat angka yang menguap, revisi ditolak.

---

## 2. Peta Guard : Audit Mesin dan Verifikasi Manual

| ID | Kode Guard | Level | Metode Pengecekan | Kriteria Lolos (Green) |
|---|---|---|---|---|
| **G-01** | Zero Prompt Leakage | 🔴 BLOCKER | Regex `B1` | Nol teks instruksi prompt atau reviewer yang tertinggal |
| **G-02** | Zero Syntax Splice / Glitch | 🔴 BLOCKER | Regex `B9` dan audit gramatikal | Nol kalimat patah, kata ganda, tanda baca bertabrakan |
| **G-03** | Zero Raw Code / Placeholder | 🔴 BLOCKER | Regex `B2`, `B3` | Nol kode mermaid mentah atau penanda sementara |
| **G-04** | No Rhetorical Contrast Trap | 🟡 HIGH | Regex `R1` | Nol pola "bukan (lagi) X, melainkan Y" pada pembuka paragraf |
| **G-05** | Direct Fact-First Opening | 🟡 HIGH | Telaah paragraf pembuka | Dibuka dengan fakta entitas riil, bukan renungan umum |
| **G-06** | Vocabulary Slop Blacklist | 🟡 HIGH | Regex `L1` sampai `L5`, Lampiran A.1 | Nol frasa klise AI generik |
| **G-07** | Burstiness and Asymmetric Cadence | 🟢 MANUAL | Metrik `I1` sampai `I5` | CV panjang kalimat >= 0,40 dan kalimat pendek >= 18% |
| **G-08** | Grounded Technical Specificity | 🟡 HIGH | Audit substansi rekayasa | Menyebut objek, tabel, payload, kontainer riil |
| **G-09** | Strict Title-to-Method Traceability | 🔴 BLOCKER | Regex `B6`, audit konsistensi | "Konsistensi data", bukan "efektivitas"; RM1 sampai RM3 utuh |
| **G-10** | Pre-Declaration Before Reference | 🔴 BLOCKER | Urutan pembacaan teks | Definisi F1 sampai F6 dan metrik mendahului tabel matriks |
| **G-11** | No Negative Parallelism Anywhere | 🟡 HIGH | Regex `R1` | Maksimum 2 kemunculan pada seluruh naskah |
| **G-12** | No Mechanical Tricolon | 🟡 HIGH | Regex `R2` | Rangkaian tiga hanya apabila objeknya memang berjumlah tiga |
| **G-13** | No Puffery / Editorializing Aside | 🟡 HIGH | Regex `R3`, `R4` | Nol penilaian penting, krusial, menarik, patut dicatat |
| **G-14** | No Paragraph-Ending Recap | 🟡 HIGH | Regex `R5` | Paragraf berhenti pada fakta terakhir |
| **G-15** | No Rhetorical Question | 🟡 HIGH | Regex `R6` | Nol tanda tanya di luar rumusan masalah dan kutipan wawancara |
| **G-16** | Nominalization Budget | 🟡 HIGH | Metrik `S7` | Densitas nominalisasi pe-an dan ke-an <= 0,075 per kata |
| **G-17** | No Participial Tail | 🟡 HIGH | Regex `S1` | Nol ekor ", sehingga memastikan/menghasilkan/mencerminkan" |
| **G-18** | No "yang mana" | 🟡 HIGH | Regex `S2` | Nol kemunculan |
| **G-19** | Anaphora Chain Limit | 🟢 MANUAL | Regex `S3` | Maksimum 1 "hal ini/tersebut" per paragraf |
| **G-20** | Passive Voice Budget | 🟢 MANUAL | Metrik `S8` | Rasio verba di- <= 0,55 (pasif sah dalam ragam ilmiah) |
| **G-21** | Connector Opening Budget | 🟡 HIGH | Metrik `L8` | <= 14% kalimat dibuka konektor filler |
| **G-22** | No Vague Attribution | 🔴 BLOCKER | Regex `L6` | Setiap klaim literatur memiliki sitasi bernama dan bertahun |
| **G-23** | No Symmetric Hedging | 🟡 HIGH | Regex `L7`, `R7` | Keterbatasan dinyatakan spesifik dan terukur |
| **G-24** | Paragraph Architecture Variance | 🟢 MANUAL | Metrik `I6` | CV panjang paragraf >= 0,25 pada korpus >= 6 paragraf |
| **G-25** | Terminology Lock (Anti-Sinonimisasi) | 🔴 BLOCKER | Audit istilah, GUARD 12 | Satu konsep satu istilah pada seluruh naskah |
| **G-26** | Typography Residue Zero | 🔴 BLOCKER | Regex `B10` | Nol em dash, kutip melengkung, sisa markdown pada `.docx` |
| **G-27** | Human Signature Density | 🟢 MANUAL | Daftar periksa Bagian 6 | Minimal 7 dari 12 penanda hadir per subbab |
| **G-28** | Claim-Evidence Pairing | 🟡 HIGH | Audit manual | Setiap klaim operasional memiliki narasumber atau angka |
| **G-29** | AI-Slop Index Threshold | 🟡 HIGH | `slop_audit.py` | ASI <= 25, ideal <= 12 |
| **G-30** | Reviewer Simulation Pass | 🟢 MANUAL | Bagian 9 Lapis 4 | Lolos lima pertanyaan penguji standar |
| **G-31** | Register Ilmiah Terjaga | 🔴 BLOCKER | Regex `N1`, `N2` | Nol kata ragam percakapan dan nol kata sapaan |
| **G-32** | Kata Ganti Impersonal | 🔴 BLOCKER | Regex `N3` | Nol "saya", "kami", "kita", "Anda"; gunakan "peneliti" |
| **G-33** | Kebakuan Diksi (KBBI) | 🔴 BLOCKER | Regex `N4`, Lampiran A.3 | Nol bentuk takbaku (analisa, praktek, resiko, dan sejenisnya) |
| **G-34** | Kata Depan di, ke, dari Terpisah | 🔴 BLOCKER | Regex `E1` | Kata depan terpisah, awalan di- serangkai |
| **G-35** | Larangan "di mana" Relatif | 🔴 BLOCKER | Regex `E2` | Nol "di mana" atau "dimana" sebagai penanda klausa relatif |
| **G-36** | Huruf Miring Istilah Asing | 🟡 HIGH | Regex `E3`, audit manual | Istilah asing dimiringkan secara konsisten |
| **G-37** | Konsistensi Huruf Kapital | 🟡 HIGH | Audit manual | Kapital hanya untuk nama diri, awal kalimat, dan judul resmi |
| **G-38** | Ketepatan Tanda Baca | 🟡 HIGH | Regex `E4` | Koma anak kalimat mendahului induk; nol spasi sebelum titik |
| **G-39** | Kesepadanan Struktur (S-P jelas) | 🔴 BLOCKER | Regex `K1` | Nol kalimat berawalan preposisi yang menghilangkan subjek |
| **G-40** | Kehematan Kata (Antipleonasme) | 🟡 HIGH | Regex `K2`, Lampiran A.4 | Nol "agar supaya", "adalah merupakan", "sangat ... sekali" |
| **G-41** | Keparalelan Bentuk | 🟡 HIGH | Audit manual | Perincian sejajar bentuknya (semua nomina atau semua verba) |
| **G-42** | Kelogisan Makna | 🟡 HIGH | Audit manual | Pelaku dan perbuatan logis ("waktu dipersilakan", bukan objek bertindak sendiri) |
| **G-43** | Kecermatan (Nol Ketaksaan) | 🟡 HIGH | Audit manual | Nol kalimat bermakna ganda |
| **G-44** | Kepaduan (Koherensi Antarkalimat) | 🟢 MANUAL | Baca nyaring | Rujukan pronomina jelas acuannya |
| **G-45** | Daftar Putih Konvensi Skripsi | 🟢 MANUAL | GUARD 19 | Frasa konvensi skripsi tidak ikut dihapus |
| **G-46** | Larangan Pemalsuan Kemanusiaan | 🔴 BLOCKER | GUARD 20 | Nol salah ketik atau kesalahan gramatikal yang disengaja |
| **G-47** | Konsistensi Istilah Asing vs Serapan | 🟡 HIGH | Audit manual | Satu bentuk dipilih dan dipertahankan (*event* atau kejadian) |
| **G-48** | Keajegan Sistem Penulisan Angka | 🟡 HIGH | Regex `E5` | Desimal koma, ribuan titik, satuan konsisten |
| **G-49** | Densitas Gagasan Terjaga | 🟢 MANUAL | Metrik `D1` vs garis dasar | Propositional idea density tidak turun dari kebiasaan penulis |
| **G-50** | Anti-Repetisi Struktural | 🟢 MANUAL | Metrik `D2` (compression ratio POS) | Tidak lebih repetitif daripada tulisan lama penulis |
| **G-51** | Anti-Templatedness Sintaksis | 🟡 HIGH | Metrik `D3` (templates-per-token) | Tidak lebih templatik daripada garis dasar |
| **G-52** | Anti-Simetri Pembuka | 🟡 HIGH | Metrik `D4` | < 30% kalimat berurutan berpola pembuka sama |
| **G-53** | Anggaran Diksi Evaluatif | 🔴 BLOCKER | Metrik `D5` (leksikon subjektivitas) | <= 1,2% kata bersifat evaluatif |
| **G-54** | Anggaran Hedging | 🟡 HIGH | Metrik `D6` | <= 1,8% kata berupa pemagaran |
| **G-55** | Anti-Listifikasi Paksa | 🟡 HIGH | Audit manual, GUARD 24 | Perincian hanya bila objeknya memang berbutir |
| **G-56** | Curvature Terkendali | 🟢 MANUAL | `deep_audit.py` | Curvature dokumen tidak jauh di atas garis dasar pribadi |
| **G-57** | Surprisal Tidak Rata | 🟢 MANUAL | `deep_audit.py` (UID) | CV surprisal tidak jauh di bawah garis dasar pribadi |
| **G-58** | Prioritas Kalimat Terdatar | 🟢 MANUAL | `deep_audit.py --topk` | 10 kalimat terdatar wajib ditinjau tiap putaran |
| **G-59** | Kontrak Invarian Terverifikasi | 🔴 BLOCKER | `invariant_check.py` | Exit code 0, nol angka dan sitasi yang menguap |
| **G-60** | Ketertelusuran Rujukan Metodologis | 🔴 BLOCKER | Lampiran F | Nol sitasi dengan metadata keliru atau tidak terverifikasi |

---

## 3. Dasar Empiris

### 3.1. Kosakata berlebih
Kobak dkk. (2025) menganalisis lebih dari 15 juta abstrak PubMed 2010 sampai 2024 dan menemukan lonjakan mendadak frekuensi kata gaya tertentu setelah kemunculan ChatGPT, dengan *delves*, *underscores*, *showcasing*, *crucial*, dan *potential* sebagai penanda terkuat. Padanan Indonesianya (menyelami, menggarisbawahi, menampilkan, krusial, potensial) masuk daftar hitam Lampiran A.1.

### 3.2. Preferensi sintaksis
Reinhart dkk. (2025) membandingkan 66 fitur gramatikal dan menemukan model instruction-tuned memakai klausa partisipial, klausa "that" sebagai subjek, nominalisasi, dan koordinasi frasal jauh di atas laju manusia, dengan GPT-4o pada klausa partisipial mencapai 5,3 kali laju manusia. Dalam bahasa Indonesia, gejala tersebut menjelma menjadi ekor kalimat ", sehingga memastikan ...", ", menghasilkan ...", dan ", mencerminkan ...".

### 3.3. Irama seragam
Muñoz-Ortiz dkk. (2024) menemukan teks manusia memiliki sebaran panjang kalimat yang lebih berserak, kosakata lebih beragam, serta jarak dependensi lebih pendek, sedangkan keluaran model memakai lebih banyak angka, simbol, dan verba bantu. Nilai dispersi (penanda *burstiness*) model berada jauh di bawah manusia.

### 3.4. Anti-pengulangan yang justru mencurigakan
Model menghindari pengulangan lokal dan mencari variasi diksi. Dalam naskah rekayasa perangkat lunak, variasi istilah teknis merupakan cacat, bukan kekayaan. Lihat GUARD 12.

### 3.5. Pola retoris
Panduan komunitas penyunting Wikipedia (*Signs of AI writing*) mencatat paralelisme negatif, rangkaian tiga mekanis, puffery, sisipan editorial, kalimat rekap penutup, serta kebiasaan tipografi seperti boldface berlebih. Penentunya bukan satu kemunculan, melainkan akumulasinya.

### 3.6. Keterbatasan detektor otomatis
Detektor berbasis perplexity rapuh, terutama untuk penulis non-penutur asli bahasa Inggris dan untuk bahasa dengan data latih terbatas seperti bahasa Indonesia. Guard ini tidak menargetkan skor detektor.

### 3.7. Temuan literatur kebahasaan Indonesia (baru di v3.0)

Bagian ini menjelaskan apa yang sebenarnya dinilai penguji ketika membaca naskah berbahasa Indonesia.

1. **Kesalahan berbahasa pada skripsi bersifat khas dan berulang.** Penelitian atas skripsi mahasiswa Program Studi Sistem Informasi STMIK Kharisma Makassar menemukan kesalahan pada empat wilayah, yaitu ejaan (huruf kapital, huruf miring, tanda baca), penulisan kata, kalimat, dan pembentukan paragraf. Kesalahan huruf miring merupakan yang terbanyak. Temuan ini relevan langsung bagi naskah ini, karena naskah memuat puluhan istilah asing seperti *event-driven*, *outbox*, dan *idempotency key*. Karena itu GUARD 36 dan GUARD 47 dibuat berkategori tinggi.
2. **Ketidakefektifan kalimat didominasi pemborosan kata.** Kajian atas skripsi mahasiswa Universitas Malikussaleh lulusan 2019 menemukan 339 kalimat tidak efektif, dengan sebab berupa kekeliruan bentukan bagian kalimat, kesalahan struktur, serta pemborosan kata. Pemborosan kata juga dicatat sebagai salah satu faktor utama ketidakefektifan kalimat dalam kajian pleonasme berbahasa Indonesia. Karena itu GUARD 40 dibuat berdiri sendiri dengan daftar tertutup pada Lampiran A.4.
3. **Kekeliruan kata depan di dan ke sangat lazim.** Kajian kesalahan berbahasa mencatat kata depan sering ditulis serangkai, sementara awalan di- justru ditulis terpisah. EYD Edisi V menegaskan kata depan di, ke, dan dari ditulis terpisah dari kata yang mengikutinya. Karena itu GUARD 34 dinaikkan ke level BLOCKER.
4. **Ragam ilmiah memiliki ciri baku yang dapat diperiksa.** Literatur ragam bahasa ilmiah merumuskan ciri cendekia, lugas dan jelas, formal, objektif, ringkas dan padat, bertolak dari gagasan, serta konsisten. Objektivitas diwujudkan melalui kata ganti impersonal dan kalimat pasif, sedangkan kata ganti "saya" dan "kami" digantikan "peneliti" atau "penulis". Dua ciri terakhir, yaitu bertolak dari gagasan dan konsisten, sejalan persis dengan GUARD 5 dan GUARD 25.
5. **Implikasi terpenting untuk naskah ini.** Sebagian besar kesalahan tersebut **tidak pernah dilakukan model bahasa**. Model menulis ejaan rapi, kata baku, dan kalimat gramatikal. Maka jalan menuju naskah yang meyakinkan **bukan** dengan meniru kesalahan mahasiswa, melainkan dengan menghilangkan ciri gaya mesin sambil mempertahankan kebenaran kaidah. Larangan tegas atas peniruan kesalahan diatur pada GUARD 20.

---

### 3.8. Lapis arsitektur: dari mana pola itu sebenarnya lahir (baru di v4.0)

Lima subbagian sebelumnya menjelaskan **apa** yang terlihat. Subbagian ini menjelaskan
**mengapa** pola itu ada. Tanpa bagian ini, guard hanya berupa daftar larangan yang harus
dihafal. Dengan bagian ini, penulis dapat menilai sendiri kalimat yang belum pernah masuk
daftar mana pun.

**3.8.1. Model memilih jalur berprobabilitas tinggi, manusia tidak.**
Holtzman dkk. (2020) menunjukkan bahwa pencarian jalur berprobabilitas maksimum
menghasilkan teks yang membosankan dan berulang, sedangkan teks manusia justru
berosilasi antara kata yang terduga dan kata yang tidak terduga. Itulah alasan
metode *nucleus sampling* diperlukan. Implikasi langsungnya bagi naskah ini:
**kalimat yang terasa mesin adalah kalimat yang bisa ditebak kata per kata.**
Kalimat *"Sistem informasi memiliki peran penting dalam menunjang kegiatan operasional
perusahaan"* dapat ditebak hampir seluruhnya. Kalimat *"Petugas gudang mencatat mutasi
pada akhir hari, bukan pada saat barang keluar"* tidak dapat ditebak, karena memuat
fakta yang hanya diketahui orang yang pernah berada di sana. Inilah dasar teoretis
GUARD 3 dan Bagian 6.

**3.8.2. Teks mesin berada di puncak lokal kurva probabilitas bersyarat.**
Bao dkk. (2024) merumuskan *conditional probability curvature*. Secara ringkas, untuk
setiap posisi token, model memiliki harapan log-likelihood atas seluruh kemungkinan
kata. Teks yang dihasilkan mesin cenderung memiliki log-likelihood teramati yang
mendekati atau melampaui harapan tersebut, sehingga skor

    d(x) = ( log p(x) - SUM E[log p] ) / sqrt( SUM Var[log p] )

bernilai tinggi. Teks manusia memiliki d yang jauh lebih rendah karena manusia rutin
memilih kata yang menurut model tidak optimal. Metode ini diturunkan dari DetectGPT
(Mitchell dkk. 2023) dan menghilangkan kebutuhan sampling perturbasi, sehingga dapat
dijalankan di laptop. `tools/deep_audit.py` mengimplementasikan rumus ini secara
analitik dan, yang jauh lebih berguna daripada vonis global, **mengurutkan kalimat
dalam naskah berdasarkan kedataran probabilitasnya**. Kalimat peringkat teratas adalah
kalimat yang paling mendesak dikonkretkan.

**3.8.3. Sidik jari statistik tetap ada tanpa akses ke bobot model.**
Verma dkk. (2024) pada Ghostbuster menunjukkan bahwa kombinasi nonlinier fitur
probabilitas unigram, bigram, dan trigram dari model penilai yang lebih lemah sudah
cukup untuk membedakan teks mesin, tanpa akses ke model penghasilnya. Artinya, jejak
itu bukan artefak satu model tertentu, melainkan sifat umum penulisan berbasis
prediksi token. Konsekuensinya bagi penulis: mengganti model, memarafrase ulang, atau
menyuruh model "menulis seperti manusia" tidak menghapus jejak, karena jejaknya
terletak pada cara teks diproduksi, bukan pada kosakatanya.

**3.8.4. Sebagian model komersial menyisipkan bias statistik secara sengaja.**
Kirchenbauer dkk. (2023) merancang skema tanda air yang membagi kosakata menjadi daftar
hijau dan merah pada setiap langkah, lalu menaikkan peluang daftar hijau. Hasilnya
adalah z-score yang dapat diuji secara statistik pada teks keluaran. Penulis tidak perlu
melakukan apa pun terhadap hal ini, tetapi perlu mengetahui satu konsekuensinya:
**menyalin utuh keluaran model ke naskah akademik menyimpan risiko yang tidak dapat
dihapus dengan penyuntingan gaya.** Satu-satunya jalan aman adalah naskah yang gagasan,
fakta, dan angkanya memang berasal dari pekerjaan penulis sendiri, sedangkan model hanya
membantu merapikan kalimat. Guard ini dirancang untuk skenario itu, bukan untuk
menyamarkan keluaran mentah.

**3.8.5. Taksonomi akademik pertama tentang slop.**
Shaib dkk. (2025) menyusun taksonomi slop melalui wawancara 19 pakar NLP, linguistik,
penulisan, dan filsafat, lalu memvalidasinya dengan anotasi rentang teks oleh penyunting
profesional atas 150 artikel berita dan 100 paragraf tanya jawab. Taksonominya bertumpu
pada tiga tema: **Information Utility** (Density, Relevance), **Information Quality**
(Factuality, Bias), dan **Style Quality** (Repetition, Templatedness, Coherence, Fluency,
Verbosity, Word Complexity, Tone). Tiga temuan yang langsung dipakai guard ini:

1. Prediktor terkuat label slop adalah Relevance, Density, dan Tone. Artinya, penilaian
   pembaca lebih ditentukan oleh **kepadatan informasi** daripada oleh kosakata.
2. Sebagian dimensi memiliki metrik otomatis yang sahih, yaitu Density melalui surprisal,
   Repetition melalui *compression ratio*, Templatedness melalui *templates-per-token*,
   Bias melalui leksikon subjektivitas, dan Verbosity melalui panjang. `slop_audit.py`
   mengimplementasikan seluruhnya dengan penyesuaian bahasa Indonesia.
3. Dimensi yang paling menentukan justru belum memiliki metrik otomatis yang andal,
   yaitu Relevance, Coherence, dan Tone. Penulis wajib membaca sendiri, dan penelitian
   itu juga menemukan bahwa model penalar sekelas GPT-5 pun gagal mengekstraksi rentang
   slop secara andal. Ini alasan mengapa Lapis 3 dan Lapis 4 pada Bagian 9 tetap manual
   dan tidak boleh diserahkan kepada alat mana pun.

**3.8.6. Nada menjilat dan pemagaran berasal dari proses pelatihan.**
Sharma dkk. (2023) menunjukkan bahwa umpan balik manusia pada RLHF mendorong model
menyetujui pengguna, sedangkan Bharadwaj dkk. (2025) menemukan model penghadiah
memberi bobot berlebih pada lima isyarat permukaan, yaitu panjang, struktur, jargon,
sikap menjilat, dan kekaburan. Dua temuan itu menjelaskan mengapa keluaran model
cenderung panjang, terstruktur rapi berlebihan, penuh jargon, dan penuh pemagaran.
Dalam naskah skripsi, gejalanya muncul sebagai kalimat yang menyenangkan pembaca tetapi
tidak menyatakan apa pun. GUARD 23, GUARD 53, dan GUARD 54 menargetkan gejala ini.

**3.8.7. Ringkasan operasional.** Empat lapis jejak, empat cara menghapusnya:

| Lapis | Jejak | Cara menghapus | Alat |
|---|---|---|---|
| Token | Kalimat terlalu terduga | Tambah fakta yang hanya Anda ketahui | `deep_audit.py` |
| Sintaksis | Templat kelas kata berulang | Variasikan susunan, bukan kosakata | `slop_audit.py` (D2, D3) |
| Leksikal | Kosakata penanda | Ganti dengan istilah teknis terkunci | `slop_audit.py` (L, R) |
| Wacana | Densitas rendah, simetri, rekap | Buang kalimat kosong, jangan ganti dengan kalimat kosong lain | `slop_audit.py` (D1, D4), baca nyaring |

Perhatikan bahwa ketiga baris pertama menyarankan hal yang sama: **tambahkan informasi
yang hanya dimiliki penulis.** Itulah satu-satunya operasi yang menurunkan skor pada
keempat lapis sekaligus. Seluruh trik lain hanya memindahkan masalah.

---

## 4. Studi Kasus Forensik

### Kasus 1 : Kebocoran Instruksi (*Prompt Leakage*)
> *"... **Berangkat dari kebutuhan dijelaskan kebutuhannya apa**, penelitian merancang dan mengevaluasi arsitektur event-driven microservices ..."*

Kalimat instruksi pengguna ikut tertelan ke dalam teks hasil regenerasi. Penguji langsung menyimpulkan drafnya tidak dibaca ulang.

### Kasus 2 : Glitch Penggabungan Teks (*Splice Glitch*)
> *"... Berdasarkan penjajakan awal bersama pemiliknya, Ibu Atik, **tiga, Berdasarkan hasil wawancara dan pengamatan** apotek dengan tiga cabang aktif ..."*

Dua alternatif kalimat hasil generasi disalin sebagian tanpa penghapusan sisa potongan lama.

### Kasus 3 : Dikotomi Retoris Monoton
> *"... **pertanyaan mendasar yang muncul bukan lagi apakah** sistem pencatatannya sanggup menampung volume transaksi yang bertambah, **melainkan apakah** sistem tersebut masih dapat dipercaya ..."*

Pola bawaan model yang mendramatisasi pembuka paragraf dengan kontras retoris palsu.

### Kasus 4 : Ekor Partisipial (*Participial Tail*)
> *"Setiap layanan menulis kejadian ke basis datanya sendiri, **sehingga memastikan konsistensi data tetap terjaga di seluruh cabang**."*

Terjemahan harfiah konstruksi *"..., ensuring data consistency across branches"*. Perbaikan: pecah menjadi dua kalimat atau letakkan klausa tujuan di depan. *"Agar saldo stok tetap sama pada ketiga cabang, setiap layanan menulis kejadian ke basis datanya sendiri."*

### Kasus 5 : Sinonimisasi Istilah Teknis
Satu paragraf menyebut `outbox`, paragraf berikutnya menyebut "tabel penampung kejadian", paragraf ketiga menyebut "buffer peristiwa keluar". Penguji membacanya sebagai penulis yang tidak menguasai istilahnya sendiri.

### Kasus 6 : Kalimat Rekap Penutup Paragraf
Hampir setiap paragraf ditutup pola "Dengan demikian, ..." atau "Hal ini menunjukkan bahwa ...". Perbaikan: hapus kalimat terakhir, lalu periksa apakah paragraf kehilangan informasi. Pada sebagian besar kasus, tidak.

### Kasus 7 : Paragraf dan Kalimat Seragam
Lima paragraf berturut-turut masing-masing terdiri atas empat kalimat, dengan setiap kalimat berkisar 25 sampai 32 kata.

### Kasus 8 : Penurunan Register akibat Humanisasi yang Keliru (baru)
> ❌ *"Kasir **memakai** aplikasi kasir yang datanya dikirim **lewat** jaringan lokal, dan selisihnya baru **ketahuan** saat stok opname."*
> ✅ *"Kasir menggunakan aplikasi penjualan yang datanya dikirim melalui jaringan lokal. Selisih tersebut baru teridentifikasi pada saat stok opname."*

Penyebab: upaya membuat kalimat terdengar manusiawi dengan menurunkan tingkat keformalan. Akibatnya naskah keluar dari ragam ilmiah. Kalimat kedua tetap pendek, tetap tegas, tetap berirama manusia, dan tetap baku.

### Kasus 9 : Subjek Hilang karena Preposisi di Awal Kalimat (baru)
> ❌ *"**Dalam** penelitian ini membandingkan tiga arsitektur pada beban yang sama."*
> ✅ *"Penelitian ini membandingkan tiga arsitektur pada beban yang sama."*

Ini kesalahan kesepadanan struktur yang paling sering ditemukan pada skripsi. Ironisnya, model bahasa jarang melakukannya. Kesalahan ini tetap wajib diperbaiki, karena penguji menilai kebenaran kaidah, bukan keaslian penulis semata. Lihat GUARD 39 dan GUARD 20.

---

## 5. Rincian Guard

---

### GUARD 1 : Eliminasi Total Residu Prompt dan Teks Editorial (BLOCKER)

1. **Pola instruksi bocor.** Dilarang: `dijelaskan kebutuhannya apa`, `masukkan data di sini`, `sesuai komentar reviewer`, `perlu diperjelas`, `tambahkan sitasi`, `silakan sesuaikan`, `berikut adalah versi revisi`, `semoga membantu`, `tentu, berikut`.
2. **Penanda sementara.** Dilarang: `[TODO]`, `[Nama]`, `[Tahun]`, `[Kutipan]`, `XXX`, `TBD`, `[Gambar ...]`, `[Tabel ...]`, `lorem ipsum`.
3. **Metadata diagram.** Baris editorial seperti `**Catatan revisi diagram:**` dibersihkan sebelum kompilasi ke `.docx`. Diagram dirender menjadi PNG atau SVG. Blok ```mermaid dilarang tersisa pada badan dokumen.
4. **Kalimat asisten.** Dilarang kalimat yang menyapa pembaca sebagai pengguna, misalnya *"Perlu diketahui bahwa"*, *"Seperti yang kita ketahui bersama"*, *"Mari kita lihat"*.

---

### GUARD 2 : Struktur Paragraf dan Anti-Retorika Klise (HIGH)

#### 2.1. Larangan pola "bukan (lagi) X, melainkan Y"
* ❌ *"Fokus penelitian bukan lagi pada ..., melainkan pada ..."*, *"Tantangan utama bukanlah keterbatasan komputasi, melainkan konsistensi data ..."*, *"Tidak hanya berdampak pada kasir, tetapi juga pada gudang ..."*
* ✅ *"Penelitian ini berfokus pada konsistensi data dan keandalan transaksi persediaan."*
* **Kuota:** maksimum dua kemunculan pada seluruh naskah, dan tidak boleh berada pada kalimat pembuka paragraf.

#### 2.2. Pembukaan paragraf berbasis fakta entitas riil
* ❌ *"Di era perkembangan teknologi informasi yang pesat ..."*, *"Dalam lanskap bisnis modern yang dinamis ..."*
* ✅ *"Apotek Bisma mengoperasikan tiga cabang aktif dan satu gudang pusat di Kabupaten Mojokerto dengan sistem pencatatan transaksi yang berdiri sendiri pada setiap unit."*
* **Uji cepat:** apabila kalimat pertama sebuah paragraf tetap benar ketika "Apotek Bisma" diganti "PT Maju Jaya", kalimat tersebut terlalu umum.

#### 2.3. Larangan rangkaian tiga mekanis
* ❌ *"sistem yang cepat, andal, dan aman"*.
* ✅ Gunakan dua atau empat butir apabila memang demikian jumlahnya. Apabila objeknya memang tiga (tiga cabang, tiga arsitektur, tiga tingkat beban), rangkaian tiga sah dan wajib dipertahankan.

#### 2.4. Larangan kalimat rekap penutup paragraf
* ❌ *"Dengan demikian, dapat disimpulkan bahwa integrasi data menjadi kebutuhan mendesak."*
* ✅ Berhenti pada fakta terakhir. Penyimpulan merupakan tugas Bab V.

#### 2.5. Larangan sisipan editorial dan puffery
* ❌ *"Patut digarisbawahi bahwa ..."*, *"Menariknya, ..."*, *"memegang peranan penting"*, *"tidak dapat dipungkiri"*.

#### 2.6. Larangan pertanyaan retoris
Tanda tanya hanya sah pada rumusan masalah dan pada kutipan wawancara.

---

### GUARD 3 : Konkretisasi Keteknikan dan Basis Data

1. **Entitas data nyata.** Bukan *"sistem mencatat transaksi"*, melainkan *"layanan Penjualan mencatat nota transaksi ke tabel `orders` dan pesan kejadian ke tabel `outbox` dalam satu transaksi lokal MySQL"*.
2. **Kondisi gagal nyata.** Bukan *"ketika terjadi kegagalan jaringan yang tidak terduga"*, melainkan *"ketika koneksi TCP ke RabbitMQ terputus sesaat sebelum publisher confirm diterima (F1)"*.
3. **Parameter eksperimen terukur.** Sebutkan parameter yang telah dikunci: warm-up 60 detik, *recovery window* 60 detik, beban 10, 50, dan 100 permintaan per detik, 30 blok replikasi berpasangan, total 3.330 run, serta jam host tunggal Docker Compose.
4. **Aturan tiga baris.** Pada setiap tiga baris prosa teknis, minimal satu elemen konkret wajib muncul, yaitu nama tabel, nama layanan, nama berkas, kode gangguan, satuan, atau angka.
5. **Larangan tumpukan nomina.** Hindari *"proses implementasi penerapan mekanisme penanganan kegagalan"*. Uraikan menjadi predikat yang jelas.

---

### GUARD 4 : Irama Kalimat dan Burstiness

| Metrik | Target | Kode |
|---|---|---|
| Rerata panjang kalimat | <= 26 kata | I4 |
| Simpangan baku panjang kalimat | >= 7 kata | I2 |
| Koefisien variasi panjang kalimat | >= 0,40 | I1 |
| Proporsi kalimat < 15 kata | >= 18% | I3 |
| Proporsi kalimat > 40 kata | <= 8% | I5 |

**Teknik pencapaian:**
1. **Pola panjang lalu pendek.** Setelah kalimat teknis panjang yang menguraikan mekanisme, letakkan kalimat pendek yang menyatakan akibatnya. *"Selisih tersebut baru teridentifikasi pada stok opname."*
2. **Satu kalimat inti per paragraf maksimal 12 kata.**
3. **Dilarang tiga kalimat berturut-turut dengan selisih panjang di bawah 4 kata.**
4. **Dilarang tiga kalimat berturut-turut dibuka pola gramatikal yang sama.**

Catatan penting: kalimat pendek tidak sama dengan kalimat takbaku. *"Selisih tersebut baru teridentifikasi pada stok opname."* hanya terdiri atas tujuh kata, tetap berpredikat lengkap, dan tetap berada dalam ragam ilmiah.

---

### GUARD 5 : Arsitektur Paragraf

1. **Larangan corong universal.** Model selalu membuka paragraf dari yang umum menuju yang khusus. Sebagian paragraf wajib dibuka langsung dari temuan spesifik.
2. **Larangan paragraf seragam.** Pada korpus enam paragraf atau lebih, koefisien variasi panjang paragraf minimal 0,25.
3. **Larangan redundansi antarparagraf.** Apabila dua paragraf dapat ditukar posisinya tanpa mengganggu logika, salah satunya tidak diperlukan.
4. **Satu paragraf satu gagasan pokok.** Kalimat utama berada pada kalimat pertama atau kedua. Paragraf sekurang-kurangnya terdiri atas dua kalimat, yaitu kalimat utama dan kalimat penjelas.

---

### GUARD 6 : Daftar Hitam Leksikal AI Slop

Daftar lengkap pada **Lampiran A.1**. Inti:

| Frasa Klise AI | Alasan Penolakan | Alternatif Baku dan Teknis |
|---|---|---|
| Bukan lagi ..., melainkan ... | Retorika dramatis generik | Nyatakan fakta secara deklaratif |
| Berangkat dari kebutuhan ... | Frasa transisi khas AI | *"Untuk memenuhi kebutuhan integrasi tersebut ..."* |
| Dalam konteks ini, ... | Transisi tanpa nilai tambah | Hapus, mulai dari subjek |
| Memiliki peran krusial | Jargon hiperbolis | Sebutkan fungsi konkret |
| Secara komprehensif dan holistik | Adjektiva kosong | Sebutkan cakupan terukur |
| Menjembatani kesenjangan | Metafora klise | *"Menghubungkan aliran data antara unit kasir dan gudang"* |
| Menghadirkan paradigma baru | Melebihkan hal lumrah | *"Menerapkan pendekatan modular berbasis kejadian"* |
| Efektivitas | Melanggar arahan pembimbing | **konsistensi data** atau **keandalan transaksi** |
| Kondisi / Artefak A, B, C | Dilarang pembimbing | Monolith Terpusat, EDA Tanpa Proteksi, EDA dengan Proteksi |
| Harmonisasi / sinergi sistem | Bahasa kehumasan | *"Sinkronisasi data antarbasis data"* |
| Hal ini dikarenakan oleh fakta bahwa | Pemborosan kata | *"Penyebabnya adalah ..."* |
| Patut digarisbawahi bahwa | Retorika menggurui | Hapus, langsung tulis intinya |

---

### GUARD 7 : Sintaksis Mesin

#### 7.1. Ekor partisipial
❌ *", sehingga memastikan konsistensi data."* Pecah menjadi dua kalimat atau ubah menjadi klausa tujuan di depan.

#### 7.2. "yang mana"
Nol toleransi. Ganti menjadi "yang", ubah menjadi kalimat baru, atau gunakan "dan keadaan tersebut".

#### 7.3. Rantai anafora
Maksimum satu "hal ini" atau "hal tersebut" per paragraf. Sisanya diganti nomina yang dirujuk secara eksplisit, misalnya *"selisih saldo tersebut"*, *"kegagalan publikasi pesan tersebut"*.

#### 7.4. Nominalisasi berlebih
Densitas maksimum 0,075 per kata.
* ❌ *"Pelaksanaan pengujian terhadap penerapan mekanisme kompensasi dilakukan oleh peneliti."*
* ✅ *"Peneliti menguji mekanisme kompensasi."* atau *"Mekanisme kompensasi diuji pada tiga tingkat beban."*

#### 7.5. Pasif tanpa pelaku yang bertumpuk
Kalimat pasif sah dan dianjurkan dalam ragam ilmiah. Yang dilarang adalah pasif bertumpuk yang mengaburkan pelaku sekaligus memadatkan nomina.
* ❌ *"Dilakukan pelaksanaan pengukuran terhadap dilakukannya proses sinkronisasi."*
* ✅ *"Waktu sinkronisasi diukur pada setiap blok replikasi."*

#### 7.6. Koordinasi frasal bertumpuk
❌ *"perancangan dan implementasi serta pengujian dan evaluasi sistem"*. Uraikan menjadi perincian bernomor atau dua kalimat.

#### 7.7. Kopula definisi berantai
❌ *"Outbox adalah sebuah tabel yang berfungsi untuk menyimpan ..."* ✅ *"Tabel `outbox` menyimpan ..."*

---

### GUARD 8 : Epistemik, Sitasi, dan Kejujuran Klaim

1. **Larangan atribusi kabur (BLOCKER).** Dilarang *"banyak penelitian menunjukkan"*, *"para ahli berpendapat"*, *"secara luas diakui"* tanpa sitasi bernama dan bertahun pada kalimat yang sama.
2. **Larangan hedging simetris.** ❌ *"Hasil ini kemungkinan besar dapat berbeda pada kondisi lain."* ✅ *"Pengujian dijalankan pada satu host Docker Compose, sehingga latensi antarsimpul fisik tidak terwakili."*
3. **Larangan klaim tanpa angka.** Setiap pernyataan perbandingan performa atau integritas wajib memuat median, IQR, atau persentil ke-95.
4. **Larangan klaim berlebih.** Dilarang *"membuktikan"*, *"menjamin"*, *"menghilangkan sepenuhnya"*. Gunakan *"menunjukkan"*, *"menurunkan jumlah"*, *"tidak ditemukan pada 30 blok pengujian"*.
5. **Pasangan klaim dan bukti.** Setiap klaim masalah operasional menunjuk narasumber sah, yaitu **Ibu Atik (pemilik)** atau **Ibu Sri Utami (kepala operasional)** sesuai perannya.

---

### GUARD 9 : Tipografi dan Residu Markdown (BLOCKER)

1. Nol em dash (U+2014) dan nol en dash (U+2013) sebagai pemisah retoris. Gunakan koma, titik, atau tanda kurung.
2. Nol kutip melengkung hasil salin dari antarmuka percakapan (U+201C, U+201D, U+2018, U+2019).
3. Nol boldface dekoratif. Penebalan hanya untuk judul subbab resmi.
4. Nol sisa markdown (`**`, `##`, `- `, `|`) pada badan `.docx`.
5. Nol emoji dan nol ikon pada naskah.
6. Kapitalisasi judul mengikuti kaidah bahasa Indonesia, bukan Title Case gaya Inggris.

---

### GUARD 10 : Keterikatan Judul, Metodologi, dan Rumusan Masalah

1. **Traceability judul ke rumusan masalah.** Kata kunci utama judul adalah **"Konsistensi Data"**. Kata "efektivitas" dilarang menjadi konstruk pengganti.
2. **Metodologi mandiri (non-DSRM).** Gunakan istilah **Alur Penelitian dan Pengembangan Sistem** lima tahap. Label DSRM dan enam tahap Peffers dilarang.
3. **Statistik deskriptif non-inferensial.** Dilarang H0/H1, p-value, uji Wilcoxon, dan uji Friedman. Gunakan Median, *Interquartile Range*, Persentil ke-95, dan kelulusan *test oracle*.
4. **Kelengkapan pemetaan RM3 pada Bab III.** Paragraf pengantar Bagian E memetakan RM1 ke perancangan arsitektur, RM2 ke simulasi gangguan F1 sampai F6, dan RM3 ke perbandingan berpasangan ketiga arsitektur pada Bagian H.4.

---

### GUARD 11 : Kaidah Urutan Penyajian

Urutan wajib: (1) narasi pengantar subbab, (2) definisi kode gangguan F1, F2, F3, F4a, F4b, F5, F6 beserta definisi metrik *oversell*, *lost update*, *duplicate effect*, *permanent mismatch*, *untraceable event*, dan *terminal-state coverage*, lalu (3) tabel matriks pengujian (Tabel 3.6 dan 3.7).

---

### GUARD 12 : Kunci Terminologi (Anti-Sinonimisasi) (BLOCKER)

| Konsep | Istilah terkunci | Dilarang sebagai variasi |
|---|---|---|
| Tabel penampung kejadian | `outbox` | tabel perantara, buffer kejadian, penampung pesan |
| Kunci antiduplikasi | *idempotency key* | kunci unik pesan, penanda idempoten |
| Arsitektur 1 | Monolith Terpusat | arsitektur konvensional, sistem lama, monolitik tradisional |
| Arsitektur 2 | EDA Tanpa Proteksi | EDA dasar, event-driven sederhana |
| Arsitektur 3 | EDA dengan Proteksi | EDA lengkap, EDA termitigasi, EDA tangguh |
| Variabel terikat utama | konsistensi data | efektivitas, keandalan sistem, kualitas data |
| Kejadian gangguan | gangguan F1 sampai F6 | skenario kegagalan, insiden, kasus injeksi kesalahan |
| Jendela pemulihan | *recovery window* | masa pemulihan, periode stabilisasi |

---

### GUARD 13 : Anggaran Konektor

Maksimum 14% kalimat dibuka konektor. Daftar yang dihitung: Selain itu, Lebih lanjut, Di sisi lain, Dengan demikian, Oleh karena itu, Sementara itu, Dalam konteks, Selanjutnya, Namun demikian, Di samping itu, Sehubungan dengan.

---

### GUARD 14 : Larangan Pola Daftar Mesin

1. Dilarang setiap butir perincian dibuka frasa tebal berpola sama.
2. Dilarang seluruh butir berpanjang setara (selisih panjang antarbutir minimal 30%).
3. Dilarang perincian tiga butir apabila objek sebenarnya dua atau empat.
4. Dilarang setiap butir diakhiri klausa akibat berpola sama.

---

### GUARD 15 : Register Ilmiah Baku (BLOCKER) (baru)

Ragam ilmiah bersifat cendekia, lugas, formal, objektif, ringkas, dan konsisten. Humanisasi naskah dilakukan **di dalam** batas ini, tidak dengan menembusnya.

**15.1. Dilarang kata ragam percakapan.**
memakai, lewat, bikin, ketahuan, kelihatan, ngecek, gara-gara, kayak, seperti misalnya, banget, nggak, tapi (pada awal kalimat), terus (sebagai konektor), udah, dapetin, kepakai, dipakai (dalam arti digunakan), ngasih, taruh, naruh, bareng.

**15.2. Dilarang kata sapaan dan ajakan.**
Anda, kamu, kita lihat, mari, perhatikan bahwa, bayangkan, coba, ingat bahwa.

**15.3. Dilarang bentuk singkat dan akronim takresmi.**
yg, dgn, tsb, dll (pada badan teks), dsb, dst, & (sebagai pengganti "dan").

**15.4. Kata ganti impersonal (GUARD 32).**
Dilarang saya, aku, kami, kita, penulis merasa, menurut saya. Gunakan **peneliti**, atau susun kalimat pasif. Pilihan antara "peneliti" dan "penulis" ditetapkan sekali dan dipertahankan pada seluruh naskah.

**15.5. Nada.**
Dilarang nada promosi, nada motivasi, nada jurnalistik, tanda seru, dan majas. Ragam ilmiah bermakna denotatif.

**15.6. Uji register.**
Bacakan satu paragraf. Apabila paragraf tersebut terdengar wajar diucapkan dalam percakapan santai, register naskah terlalu rendah. Apabila terdengar seperti pidato atau iklan, register naskah terlalu tinggi dan berpuffery. Sasarannya berada di antara keduanya, yaitu laporan teknis yang tenang.

---

### GUARD 16 : Kaidah EYD Edisi V (BLOCKER pada butir 1 dan 2) (baru)

**16.1. Kata depan di, ke, dari ditulis terpisah; awalan di-, ke- ditulis serangkai.**
* ✅ *di gudang, di cabang Sooko, ke basis data pusat, dari tabel `orders`*
* ✅ *dicatat, disimpan, dikirim, ketiga, kedua*
* ❌ *digudang, dicabang, kegudang, di catat, di simpan, di kirim*
* Uji: apabila kata setelahnya menunjukkan tempat atau arah, tulis terpisah. Apabila kata setelahnya verba, tulis serangkai.

**16.2. Larangan "di mana" dan "dimana" sebagai penanda klausa relatif.**
Konstruksi ini merupakan terjemahan harfiah *where* dan bukan kaidah bahasa Indonesia. Bentuk "dimana" bahkan salah eja karena menggabungkan kata depan.
* ❌ *"sistem monolit, di mana seluruh modul berbagi satu basis data"*
* ✅ *"sistem monolit dengan seluruh modul yang berbagi satu basis data"*
* ✅ *"sistem monolit. Seluruh modulnya berbagi satu basis data."*
* Catatan: "di mana" tetap sah pada kalimat tanya dan pada bentuk "di mana-mana".

**16.3. Huruf miring untuk istilah asing.**
Istilah asing yang belum diserap dimiringkan, misalnya *event-driven*, *outbox*, *idempotency key*, *publisher confirm*, *recovery window*, *oversell*, *lost update*. Istilah yang telah diserap tidak dimiringkan, misalnya basis data, kluster, transaksi, server, sistem, data, aplikasi. Perlakuan ditetapkan sekali pada Daftar Istilah lalu dipertahankan konsisten. Kesalahan huruf miring merupakan kesalahan terbanyak pada skripsi informatika menurut kajian Lampiran E.1.

**16.4. Huruf kapital.**
Kapital hanya untuk awal kalimat, nama diri, nama lembaga, nama jabatan yang diikuti nama orang, serta judul resmi. Dilarang mengapitalkan istilah umum di tengah kalimat seperti *Sistem*, *Data*, *Arsitektur*, kecuali istilah tersebut merupakan nama resmi arsitektur yang telah dikunci (Monolith Terpusat, EDA Tanpa Proteksi, EDA dengan Proteksi).

**16.5. Tanda baca.**
Koma dipakai di belakang anak kalimat yang mendahului induk kalimat. Tidak ada spasi sebelum titik, koma, titik dua, dan titik koma. Perincian dengan penjelas menggunakan titik dua setelah klausa lengkap. Dilarang koma sebelum "dan" pada perincian dua unsur.

**16.6. Penulisan angka dan satuan.**
Desimal menggunakan koma, pemisah ribuan menggunakan titik (3.330 run; 42,5 ms). Angka di awal kalimat ditulis dengan huruf atau kalimat disusun ulang. Satuan ditulis konsisten (ms, detik, permintaan per detik).

---

### GUARD 17 : Kalimat Efektif (baru)

Enam syarat kalimat efektif dipetakan menjadi aturan yang dapat diperiksa.

**17.1. Kesepadanan struktur (BLOCKER).**
Setiap kalimat wajib bersubjek dan berpredikat jelas. Kesalahan terlazim adalah preposisi di depan subjek.
* ❌ *"Dalam penelitian ini membandingkan tiga arsitektur."* ✅ *"Penelitian ini membandingkan tiga arsitektur."*
* ❌ *"Menurut Ibu Atik menyatakan bahwa ..."* ✅ *"Ibu Atik menyatakan bahwa ..."*
* ❌ *"Berdasarkan hasil pengujian menunjukkan bahwa ..."* ✅ *"Hasil pengujian menunjukkan bahwa ..."*
* Dilarang pula konjungsi ganda: *"Karena ... sehingga ..."*, *"Meskipun ... tetapi ..."*, *"Walaupun ... namun ..."*

**17.2. Kehematan kata.** Lihat GUARD 18.

**17.3. Keparalelan bentuk.**
Unsur perincian wajib sebentuk.
* ❌ *"Tahapan penelitian meliputi perancangan arsitektur, mengimplementasikan layanan, dan pengujian gangguan."*
* ✅ *"Tahapan penelitian meliputi perancangan arsitektur, implementasi layanan, dan pengujian gangguan."*

**17.4. Ketegasan.**
Gagasan utama diletakkan di awal kalimat. Dilarang menumpuk keterangan di depan sehingga predikat terdorong ke ujung kalimat.

**17.5. Kecermatan.**
Nol ketaksaan. ❌ *"Pengujian layanan Penjualan yang baru dilakukan kemarin."* Perbaiki dengan menegaskan acuan "yang baru".

**17.6. Kelogisan.**
Pelaku dan perbuatan wajib logis. ❌ *"Tabel `outbox` bertugas menjamin keberhasilan pengiriman."* ✅ *"Pengiriman ulang pesan bersumber dari catatan pada tabel `outbox`."*

**17.7. Kepaduan.**
Rujukan pronomina jelas acuannya. Apabila dalam satu paragraf terdapat dua nomina yang mungkin dirujuk "-nya", tulis ulang nominanya.

---

### GUARD 18 : Kehematan Kata dan Antipleonasme (baru)

Pemborosan kata merupakan salah satu penyebab utama ketidakefektifan kalimat pada skripsi (Lampiran E.2 dan E.3). Daftar tertutup pada **Lampiran A.4**. Pola utama:

1. **Sinonim bertumpuk:** *adalah merupakan*, *agar supaya*, *demi untuk*, *seperti misalnya*, *disebabkan karena*, *namun tetapi*, *hanya ... saja*, *sejak dari*.
2. **Penanda jamak ganda:** *para mahasiswa-mahasiswa*, *beberapa data-data*, *banyak cabang-cabang*.
3. **Superlatif ganda:** *sangat ... sekali*, *paling ter-*, *agak sedikit*.
4. **Keterangan mubazir:** *naik ke atas*, *turun ke bawah*, *mundur ke belakang*, *saling bekerja sama satu sama lain*.
5. **Frasa panjang bernilai nol:** *dalam rangka untuk*, *guna untuk*, *dapat dikatakan bahwa*, *merupakan salah satu hal yang*, *sebagaimana telah dijelaskan sebelumnya*, *pada dasarnya*, *terlebih dahulu terlebih dulu*.
6. **Verba hampa:** *melakukan pengujian* menjadi **menguji**; *melakukan analisis* menjadi **menganalisis**; *memberikan penjelasan* menjadi **menjelaskan**; *mengadakan pengukuran* menjadi **mengukur**.

Butir 6 melayani dua tujuan sekaligus, yaitu menghemat kata dan menurunkan densitas nominalisasi (GUARD 16 pada peta, butir 7.4 pada rincian).

---

### GUARD 19 : Daftar Putih Konvensi Skripsi Indonesia (baru)

Guard ini mencegah over-koreksi. Sejumlah frasa terdengar formulaik, tetapi memang merupakan konvensi naskah skripsi Indonesia dan lazim ditulis mahasiswa. Menghapusnya justru membuat naskah tidak lagi menyerupai skripsi.

**Frasa yang TIDAK boleh ikut dibersihkan:**
* *Penelitian ini bertujuan untuk ...*
* *Rumusan masalah dalam penelitian ini adalah sebagai berikut.*
* *Berdasarkan latar belakang tersebut, penelitian ini ...*
* *Batasan masalah dalam penelitian ini meliputi ...*
* *Manfaat penelitian ini terbagi atas manfaat teoretis dan manfaat praktis.*
* *Hasil wawancara dengan Ibu Atik menunjukkan bahwa ...*
* *Tahapan penelitian ditunjukkan pada Gambar 3.1.*
* *Tabel 3.6 memuat matriks pengujian gangguan.*
* *Bab ini menguraikan ...*

**Batas pemakaian:** frasa konvensi dipakai pada posisi strukturalnya, yaitu pembuka bab, pembuka subbab, dan pengantar objek. Frasa konvensi dilarang dipakai sebagai transisi antarparagraf biasa.

**Uji pembeda cepat:** frasa konvensi menunjuk **objek naskah** (bab, tabel, rumusan masalah, gambar). Frasa slop AI menunjuk **kesan** (pentingnya, krusialnya, menariknya). Konvensi dipertahankan, kesan dibuang.

---

### GUARD 20 : Larangan Pemalsuan Kemanusiaan (BLOCKER) (baru)

1. **Dilarang menyisipkan salah ketik, kesalahan ejaan, atau kesalahan gramatikal secara sengaja** agar naskah terkesan ditulis manusia. Penguji menilai kebenaran kaidah. Kesalahan yang disengaja menghasilkan koreksi merah, bukan kepercayaan.
2. **Dilarang menurunkan register** (GUARD 15).
3. **Dilarang menambah kalimat yang tidak membawa fakta baru** hanya untuk memecah irama.
4. **Dilarang mengubah angka, nama, atau istilah** dengan alasan variasi gaya (GUARD 12 dan Kontrak Invarian).
5. **Dilarang menyalin kalimat dari sumber mana pun tanpa sitasi.** Menghindari AI slop tidak pernah menjadi alasan yang sah untuk plagiarisme.

Jalur yang sah hanya satu, yaitu menghapus ciri gaya mesin, menaikkan kekonkretan fakta, dan menjaga kaidah tetap benar.

---

### GUARD 21 : Densitas Informasi (baru di v4.0)

Prediktor terkuat kedua atas penilaian slop menurut Shaib dkk. (2025). Definisinya
sederhana: **berapa banyak yang diketahui pembaca setelah membaca satu paragraf,
dibagi berapa banyak kata yang ia lewati untuk sampai ke sana.**

**21.1. Uji hapus.** Hapus satu kalimat. Bila tidak ada informasi yang hilang, kalimat
itu memang tidak membawa informasi. Hapus permanen. Jangan diganti.

**21.2. Uji substitusi.** Ganti subjek kalimat dengan entitas lain ("PT Maju Jaya",
"sebuah perusahaan"). Bila kalimat tetap benar, kalimat itu berdensitas nol.

**21.3. Anggaran per paragraf.** Setiap paragraf wajib memuat minimal satu dari:
angka terukur, nama artefak perangkat lunak, kode gangguan, prosedur lapangan yang
spesifik, atau sitasi bernama. Paragraf tanpa kelimanya dihapus atau diisi data.

**21.4. Larangan pengganti.** Bila kalimat kosong dihapus, dilarang menggantinya dengan
kalimat kosong lain yang lebih indah. Paragraf boleh menjadi lebih pendek. Yang dilarang
berubah adalah jumlah paragraf, bukan jumlah kata.

---

### GUARD 22 : Repetisi Struktural dan Templatedness (baru di v4.0)

Model menulis formulaik pada tataran sintaksis, bukan hanya kosakata. Dua paragraf dapat
memakai kata yang sepenuhnya berbeda tetapi memakai urutan kelas kata yang identik.
Penyunting berpengalaman menangkap ini sebagai "semua kalimatnya terasa sama".

**22.1. Metrik.** `slop_audit.py` melaporkan *compression ratio* atas urutan kata dan
atas urutan kelas kata, serta *templates-per-token*, yaitu proporsi token yang tercakup
oleh n-gram kelas kata yang berulang.

**22.2. Kalibrasi wajib.** Kedua metrik naik mengikuti panjang teks, sehingga angka
mutlaknya tidak bermakna. Bandingkan hanya terhadap garis dasar tulisan lama Anda
sendiri (`slop_audit.py --calibrate`).

**22.3. Cara memperbaiki.** Jangan mengganti sinonim, karena itu tidak mengubah urutan
kelas kata dan justru melanggar GUARD 12. Ubah **susunan**: pindahkan keterangan ke
depan pada satu kalimat, jadikan klausa tujuan pada kalimat lain, pecah satu kalimat
majemuk menjadi dua kalimat tunggal.

---

### GUARD 23 : Simetri Prematur (baru di v4.0)

**23.1.** Dilarang tiga kalimat berurutan dengan pola pembuka kelas kata yang sama.
**23.2.** Dilarang perincian yang seluruh butirnya berpanjang setara dan berstruktur sama.
**23.3.** Dilarang dua paragraf berurutan dengan jumlah kalimat sama dan pola urutan sama
(pembuka umum, dua kalimat penjelas, satu kalimat penutup).
**23.4.** Simetri sah hanya bila objeknya memang simetris, misalnya perbandingan tiga
arsitektur pada tabel hasil. Di situ keparalelan justru diwajibkan (GUARD 41). Perbedaannya:
simetri pada **tabel dan perincian data** itu benar, simetri pada **prosa** itu jejak mesin.

---

### GUARD 24 : Anti-Listifikasi Paksa (baru di v4.0)

Model memecah jawaban menjadi daftar walaupun isinya paragraf. Gejala pada naskah skripsi:
subbab yang seharusnya berupa argumen mengalir berubah menjadi sepuluh butir berpeluru.

**24.1.** Perincian dipakai hanya bila objeknya memang berbutir dan berjumlah tetap,
misalnya kode gangguan F1 sampai F6, tahapan penelitian, atau batasan masalah.
**24.2.** Dilarang perincian yang setiap butirnya berupa kalimat penuh yang saling
berhubungan secara sebab akibat. Itu paragraf yang dipotong-potong.
**24.3.** Dilarang perincian bertingkat lebih dari dua lapis pada badan naskah.
**24.4.** Setelah perincian, wajib ada kalimat yang menghubungkannya kembali ke argumen.

---

### GUARD 25 : Anggaran Diksi Evaluatif dan Pemagaran (baru di v4.0)

Berdasarkan kode Bias pada taksonomi Shaib dkk. (2025) dan temuan Bharadwaj dkk. (2025)
tentang lima isyarat permukaan yang dihadiahi berlebih oleh model penghadiah.

**25.1. Diksi evaluatif (BLOCKER).** Maksimum 1,2 persen kata. Termasuk: krusial, vital,
fundamental, esensial, luar biasa, sempurna, unggul, terbaik, canggih, inovatif,
revolusioner, mutakhir, signifikan, dramatis, pesat, menarik, mengesankan, ideal, optimal.
Pada naskah rekayasa, penilaian disampaikan melalui angka, bukan melalui kata sifat.

**25.2. Pemagaran.** Maksimum 1,8 persen kata. Termasuk: mungkin, barangkali, cenderung,
tampaknya, sepertinya, diperkirakan, relatif, umumnya, biasanya, berpotensi.
Ketidakpastian yang nyata dinyatakan dengan angka dan rentang, bukan dengan kata pemagar.
*"Median 42 ms dengan IQR 8 ms"* mengandung ketidakpastian yang jujur.
*"Latensi cenderung relatif cukup baik"* tidak mengandung apa pun.

**25.3. Nada menjilat.** Dilarang kalimat yang memuji objek penelitian, pembimbing,
institusi, atau teknologi yang dipakai. Skripsi bukan tempat memuji.

---

### GUARD 26 : Prioritas Perbaikan Berbasis Probabilitas (baru di v4.0)

Guard ini bukan larangan, melainkan urutan kerja. Waktu penulis terbatas, sehingga
perbaikan harus dimulai dari kalimat yang paling berdampak.

**26.1.** Jalankan `tools/deep_audit.py NASKAH.md --topk 12`.
**26.2.** Kerjakan dua belas kalimat terdatar itu lebih dahulu, sebelum menyentuh apa pun.
**26.3.** Untuk setiap kalimat, tanyakan satu hal: *fakta apa yang saya ketahui tentang
sistem ini yang tidak akan pernah bisa ditebak siapa pun?* Masukkan fakta itu.
**26.4.** Jalankan ulang. Kalimat yang tadinya di peringkat satu seharusnya turun jauh.
Bila tidak turun, perbaikannya bersifat kosmetik, bukan substantif.
**26.5.** Berhenti membaca skornya sebagai vonis. Skor ini hanya penunjuk arah. Lihat
peringatan pada Bagian 11.

---

## 6. Sidik Jari Manusia Wajib (*Human Signature Checklist*)

Penghapusan ciri AI hanya separuh pekerjaan. Naskah tetap terasa mesin apabila tidak ada jejak orang yang benar-benar mengerjakan sistemnya. Minimal **7 dari 12** penanda berikut wajib hadir pada setiap subbab substantif. Seluruh penanda bersifat **penambahan fakta**, bukan pelonggaran bahasa.

| No | Penanda | Contoh untuk naskah Apotek Bisma |
|---|---|---|
| H-01 | Angka spesifik, bukan angka retoris | "3.330 run", "30 blok", "60 detik", bukan "ribuan pengujian" |
| H-02 | Nama artefak perangkat lunak nyata | tabel `orders`, tabel `outbox`, *exchange* RabbitMQ, kontainer layanan Penjualan |
| H-03 | Versi dan lingkungan disebut | MySQL 8.0, RabbitMQ 3.13, Docker Compose, satu host |
| H-04 | Alasan keputusan teknis, bukan sekadar keputusannya | "Pengujian dibatasi pada satu host agar seluruh layanan berbagi satu jam sistem" |
| H-05 | Keterbatasan spesifik yang diakui terbuka | "Latensi antarsimpul fisik tidak terwakili" |
| H-06 | Rujukan observasi lapangan yang bertanggal | "Berdasarkan penjajakan awal pada ... bersama Ibu Atik" |
| H-07 | Kalimat pendek baku yang menyatakan inti masalah | "Selisih tersebut baru teridentifikasi pada stok opname." |
| H-08 | Pengulangan istilah teknis tanpa variasi | `outbox` disebut sepuluh kali sebagai `outbox` |
| H-09 | Urutan operasional yang hanya diketahui pelaku lapangan | "Petugas gudang mencatat mutasi pada akhir hari, bukan pada saat barang keluar" |
| H-10 | Satuan dan ambang eksplisit | "persentil ke-95", "permintaan per detik", "milidetik" |
| H-11 | Perbedaan peran narasumber dihormati | Ibu Atik untuk keputusan dan dampak usaha; Ibu Sri Utami untuk prosedur operasional harian |
| H-12 | Rujukan silang internal yang tepat nomor | "sebagaimana definisi F4b pada Bagian E.2" |

Apabila penanda yang hadir kurang dari tujuh, jangan menambah kata sifat. Tambahkan **fakta**.

---

## 7. Protokol Tulis Ulang Per Paragraf (8 Lintasan)

Kerjakan satu paragraf sampai tuntas, baru pindah. Penulisan ulang seluruh bab sekaligus merupakan asal-muasal *splice glitch*.

**Lintasan 1 : Kunci substansi.** Catat seluruh angka, nama, istilah terkunci, dan sitasi pada paragraf tersebut. Daftar ini menjadi kontrak.

**Lintasan 2 : Bongkar pembuka.** Ganti kalimat pertama yang umum atau bernegasi paralel dengan fakta entitas riil. Jangan menambah kalimat.

**Lintasan 3 : Potong ekor mesin.** Cari ", sehingga memastikan", ", menghasilkan", ", mencerminkan", "yang mana", serta "hal ini" kedua dan seterusnya.

**Lintasan 4 : Perbaiki struktur kalimat (baru).** Periksa kesepadanan struktur, konjungsi ganda, keparalelan perincian, dan kelogisan. Pastikan setiap kalimat bersubjek.

**Lintasan 5 : Bersihkan pemborosan (baru).** Terapkan Lampiran A.4. Ubah verba hampa menjadi verba tunggal.

**Lintasan 6 : Atur irama.** Hitung panjang setiap kalimat. Apabila tiga kalimat berturut-turut berselisih di bawah 4 kata, pecah salah satunya atau gabungkan dua kalimat pendek. Pastikan terdapat minimal satu kalimat di bawah 15 kata.

**Lintasan 7 : Buang penutup rekap.** Hapus kalimat terakhir apabila hanya mengulang isi paragraf.

**Lintasan 8 : Periksa register dan ejaan (baru).** Terapkan GUARD 15 dan GUARD 16. Pastikan tidak ada kata ragam percakapan yang menyelinap masuk selama enam lintasan sebelumnya, dan periksa kata depan di, ke, dari.

**Uji akhir per paragraf:** bacakan nyaring. Apabila napas habis di tengah kalimat, pecah kalimat tersebut. Apabila terdengar seperti artikel motivasi teknologi, ganti dengan kalimat teknis berbasis arsitektur nyata Apotek Bisma. Apabila terdengar seperti percakapan santai, naikkan kembali register.

---

## 8. Kontrak Prompt untuk Asisten AI

Tempelkan kontrak berikut pada awal sesi penyuntingan berbantuan AI.

```
KONTRAK PENYUNTINGAN NASKAH SKRIPSI (WAJIB DIPATUHI)

INVARIAN (haram berubah):
- Struktur bab, subbab, urutan paragraf, jumlah paragraf. Satu paragraf masuk, satu paragraf keluar.
- Semua angka, satuan, nama entitas, nama narasumber, kode F1-F6, nama metrik, nama arsitektur.
- Semua sitasi beserta penempatannya.
- Istilah terkunci: outbox, idempotency key, Monolith Terpusat, EDA Tanpa Proteksi,
  EDA dengan Proteksi, konsistensi data, recovery window. Dilarang mencari sinonim.
- Tingkat keformalan. Naskah tetap ragam ilmiah resmi bahasa Indonesia.

REGISTER (paling sering dilanggar, periksa terakhir):
- Gunakan kata baku sesuai KBBI dan EYD Edisi V.
- DILARANG kata ragam percakapan: memakai, lewat, bikin, ketahuan, kelihatan, dipakai,
  gara-gara, kayak, banget, nggak, tapi di awal kalimat, terus sebagai konektor.
  Gunakan: menggunakan, melalui, membuat, teridentifikasi, tampak, digunakan,
  disebabkan oleh, seperti, sangat, tidak, tetapi, kemudian.
- DILARANG kata ganti saya, aku, kami, kita, Anda. Gunakan "peneliti" atau kalimat pasif.
- DILARANG menyapa pembaca, tanda seru, majas, nada promosi.
- Kalimat pasif DIPERBOLEHKAN dan lazim dalam ragam ilmiah. Yang dilarang adalah
  pasif bertumpuk dengan nominalisasi berlapis.

EJAAN (EYD Edisi V):
- Kata depan di, ke, dari ditulis TERPISAH (di gudang, ke basis data).
  Awalan di-, ke- ditulis SERANGKAI (dicatat, dikirim, ketiga).
- DILARANG "di mana" atau "dimana" sebagai penanda klausa relatif.
- Istilah asing yang belum diserap dicetak miring, konsisten sepanjang naskah.
- Desimal dengan koma, ribuan dengan titik.

DILARANG KERAS (pola mesin):
1. "bukan (lagi) X, melainkan Y" dan semua variannya, termasuk "tidak hanya ... tetapi juga".
2. Rangkaian tiga sejajar kecuali objeknya memang berjumlah tiga.
3. Ekor partisipial: ", sehingga memastikan", ", menghasilkan", ", mencerminkan", ", menegaskan".
4. "yang mana". Lebih dari satu "hal ini/tersebut" per paragraf.
5. Kalimat rekap penutup paragraf ("Dengan demikian ...", "Hal ini menunjukkan bahwa ...").
6. Sisipan editorial dan puffery: krusial, fundamental, patut digarisbawahi, menariknya,
   memegang peranan penting, era digital, lanskap, holistik, komprehensif, robust, seamless.
7. Atribusi kabur tanpa sitasi bernama dan bertahun.
8. Pertanyaan retoris. Em dash. Kutip melengkung. Boldface dekoratif. Emoji.
9. Kata "efektivitas", label "Kondisi/Artefak A/B/C", istilah DSRM, statistik inferensial.
10. Menambah kalimat baru yang tidak membawa fakta baru.
11. Menyisipkan salah ketik atau kesalahan gramatikal yang disengaja.

KALIMAT EFEKTIF:
- Setiap kalimat bersubjek. DILARANG "Dalam penelitian ini membandingkan ...",
  "Berdasarkan hasil pengujian menunjukkan ...", "Menurut Ibu Atik menyatakan ...".
- DILARANG konjungsi ganda: "Karena ... sehingga ...", "Walaupun ... namun ...".
- DILARANG pemborosan: adalah merupakan, agar supaya, demi untuk, disebabkan karena,
  sangat ... sekali, dalam rangka untuk, dapat dikatakan bahwa.
- Ubah verba hampa: melakukan pengujian -> menguji; memberikan penjelasan -> menjelaskan.
- Perincian wajib sejajar bentuknya.

JANGAN DIHAPUS (konvensi skripsi Indonesia yang sah):
"Penelitian ini bertujuan untuk", "Berdasarkan latar belakang tersebut",
"Rumusan masalah dalam penelitian ini adalah", "Batasan masalah meliputi",
"Hasil wawancara dengan Ibu Atik menunjukkan", "Tahapan penelitian ditunjukkan pada Gambar",
"Bab ini menguraikan".

WAJIB:
- Kalimat pembuka paragraf berisi fakta entitas riil (subjek, lokasi, angka).
- Variasi panjang kalimat. Minimal satu kalimat di bawah 15 kata per paragraf,
  dan kalimat pendek itu tetap baku serta berpredikat lengkap.
- Setiap tiga baris prosa teknis memuat minimal satu elemen konkret
  (nama tabel, nama layanan, kode gangguan, satuan, atau angka).

KELUARAN:
Kembalikan hanya naskah hasil suntingan. Tanpa pengantar, tanpa penutup, tanpa penjelasan,
tanpa ringkasan perubahan, tanpa tawaran bantuan lanjutan.
```

---

## 9. Protokol Verifikasi Mandiri Sebelum Maju Bimbingan

### Lapis 0 : Simpan salinan sebelum menyentuh apa pun (wajib)

```bash
make snapshot        # atau: cp REVISI_BAB_1.md .deslop/REVISI_BAB_1.before.md
```

Tanpa salinan ini, Lapis 5 tidak dapat dijalankan dan Kontrak Invarian tidak dapat
dibuktikan. Ini langkah paling murah dan paling sering dilupakan.

### Lapis 1 : Audit kuantitatif otomatis (wajib)

```bash
python tools/slop_audit.py REVISI_BAB_*.md --show 4
```

Keluaran memuat AI-Slop Index, temuan per kode guard beserta nomor baris, dan pelanggaran ambang irama. Delapan dimensi diperiksa, yaitu B (blocker), R (retoris), L (leksikal), S (sintaksis), I (irama), N (nonbaku dan register), E (ejaan), dan K (kalimat efektif). Exit code 1 berarti naskah belum boleh dikirim.

### Lapis 2 : Regex cepat via terminal

```powershell
# 1. Residu instruksi prompt dan penanda sementara
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "dijelaskan|TODO|Catatan revisi|kebutuhannya apa|semoga membantu"

# 2. Retorika kontras klise
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "bukan lagi.*melainkan|bukan sekadar.*melainkan|tidak hanya.*tetapi juga"

# 3. Label terlarang dan kata efektivitas
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "Kondisi [ABC]|Artefak [ABC]|efektivitas"

# 4. Ekor partisipial dan yang mana
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern ", sehingga mem|, menghasilkan|, mencerminkan|yang mana"

# 5. Rekap penutup paragraf
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "Dengan demikian|Hal ini menunjukkan bahwa|Secara keseluruhan"

# 6. Ragam percakapan yang menyelinap
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "\bmemakai\b|\blewat\b|\bketahuan\b|\bbikin\b|\bkayak\b|\bdipakai\b"

# 7. Kata ganti terlarang
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "\b(saya|aku|kami|kita|Anda)\b"

# 8. Kesalahan kata depan dan di mana relatif
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "\bdimana\b|, di mana|di gudang|\bdi catat\b|\bdi simpan\b|\bdigudang\b"

# 9. Bentuk takbaku yang lazim
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "analisa|praktek|resiko|sistim|obyek|hakekat|merubah|standarisasi|apotik|frekwensi|kwalitas|nomer|ijin"

# 10. Pemborosan kata
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "adalah merupakan|agar supaya|demi untuk|disebabkan karena|sangat .* sekali|dalam rangka untuk"

# 11. Kalimat tanpa subjek
Get-ChildItem -Filter "REVISI_*.md" | Select-String -Pattern "^(Dalam|Berdasarkan|Menurut|Pada|Dengan)[^.]{0,60}(menunjukkan|menjelaskan|membandingkan|menyatakan|menguraikan)"
```

### Lapis 3 : Protokol uji baca nyaring

1. Baca paragraf demi paragraf dengan bersuara.
2. Napas habis di tengah kalimat berarti kalimat terlalu panjang.
3. Terdengar seperti pidato atau artikel motivasi berarti ganti dengan kalimat teknis.
4. Terdengar seperti percakapan santai berarti register turun. Naikkan kembali dengan Lampiran A.2.
5. Setiap klaim masalah operasional memiliki narasumber sah.
6. Paragraf yang dapat dibacakan tanpa menyebut satu pun angka, nama tabel, atau kode gangguan berisiko dinilai kosong.

### Lapis 3b : Audit lapis probabilitas token (opsional, sangat dianjurkan)

```bash
pip install torch transformers
python tools/deep_audit.py --calibrate tulisan_lama/*.md    # sekali saja
python tools/deep_audit.py REVISI_BAB_1.md --topk 12
```

Keluarannya adalah dua daftar. Daftar pertama berisi kalimat paling datar secara
probabilitas, yaitu prioritas tulis ulang. Daftar kedua berisi kalimat paling tidak
terduga, yaitu kalimat yang paling terdengar seperti Anda. Pertahankan yang kedua,
kerjakan yang pertama. Jalankan `--selftest` bila ingin memverifikasi rumusnya tanpa
mengunduh model.

### Lapis 4 : Simulasi penguji

1. Angka pada kalimat ini berasal dari mana, run keberapa, dan diukur dengan cara apa?
2. Apabila kalimat ini dihapus, apa yang hilang dari argumen?
3. Istilah ini didefinisikan pada bagian mana, dan apakah definisinya mendahului tabel ini?
4. Klaim ini menjawab rumusan masalah nomor berapa?
5. Apabila "Apotek Bisma" diganti nama apotek lain, apakah kalimat ini masih benar? Bila ya, kalimat ini terlalu umum.

---

### Lapis 5 : Kontrak Invarian (WAJIB, penentu akhir)

```bash
python tools/invariant_check.py .deslop/REVISI_BAB_1.before.md REVISI_BAB_1.md \
    --terms tools/terms.json
```

Alat ini membandingkan naskah sebelum dan sesudah, lalu menolak revisi bila ada satu saja
angka, sitasi, kode gangguan, identifier, nama diri, atau istilah terkunci yang menguap
atau bertambah. Alat ini juga mendeteksi sinonimisasi istilah terkunci dan perubahan
jumlah paragraf.

**Aturan mutlak: naskah dengan ASI hijau tetapi gagal Lapis 5 adalah naskah gagal.**
Kembalikan berkas ke salinan `.before.md`, lalu ulangi penyuntingan dengan lebih
konservatif. Skor gaya tidak pernah lebih penting daripada kebenaran isi.

---

## 10. Ambang Lulus (AI-Slop Index)

| ASI | Status | Tindakan |
|---|---|---|
| Terdapat temuan BLOCKER | 🔴 MERAH | Jangan dikirim. Bersihkan blocker terlebih dahulu |
| > 25 | 🔴 MERAH | Jalankan protokol tulis ulang per paragraf (Bagian 7) |
| 13 sampai 25 | 🟡 KUNING | Layak, rapikan temuan berbobot tinggi |
| <= 12 | 🟢 HIJAU | Lanjut ke uji baca nyaring dan simulasi penguji |

Ambang ini merupakan heuristik kerja untuk prosa teknis Indonesia, bukan standar baku dari literatur. Angkanya mengarahkan revisi, bukan membuktikan kepengarangan.

---

## 11. Batas Guard Ini

1. **Daftar ciri AI adalah alat deteksi, bukan panduan menulis.** Naskah yang dikuras dari seluruh ciri AI akan steril dan kosong. Bagian 6 dan GUARD 19 berfungsi sebagai penyeimbang.
2. **Tidak ada satu ciri pun yang membuktikan apa pun secara sendirian.** Yang menjadi bukti adalah akumulasi ciri, ditambah residu teks yang mustahil diketik manusia.
3. **Detektor AI otomatis tidak sahih sebagai bukti,** terutama untuk bahasa Indonesia. Sasaran guard ini satu orang pembaca, yaitu Pak Made.
4. **Guard ini tidak menggantikan penguasaan materi.** Kalimat paling manusiawi pada naskah teknik adalah kalimat yang hanya dapat ditulis orang yang benar-benar menjalankan sistemnya. Apabila sebuah paragraf sulit dikonkretkan, persoalannya bukan gaya bahasa, melainkan datanya belum ada.
5. **Jangan melanggar Kontrak Invarian demi skor.** Naskah ber-ASI 5 yang kehilangan tiga angka hasil pengujian merupakan kegagalan total.
6. **Kebakuan mengalahkan kealamian.** Apabila sebuah perbaikan gaya berbenturan dengan kaidah EYD atau ragam ilmiah, kaidah yang menang.

---

## Lampiran A.1 : Kamus Pengganti Diksi AI

| Diksi AI | Pengganti baku untuk naskah ini |
|---|---|
| menyelami lebih dalam, mengupas tuntas | menguraikan, menelaah |
| menggarisbawahi pentingnya | menunjukkan bahwa (diikuti angka) |
| krusial, esensial, vital, fundamental | (hapus, ganti fungsi konkret) |
| holistik, komprehensif, menyeluruh | (hapus, ganti cakupan terukur) |
| robust, tangguh, andal (tanpa angka) | (ganti kondisi gagal yang ditangani: "bertahan pada F1 dan F4b") |
| seamless, mulus, tanpa hambatan | (hapus) |
| optimal | (ganti nilai terukur: "median 42 ms") |
| signifikan | (ganti selisih terukur: "selisih median 18 ms") |
| inovatif, canggih, mutakhir, terobosan | (hapus) |
| paradigma baru | pendekatan berbasis kejadian |
| menjembatani kesenjangan | menghubungkan aliran data antara unit kasir dan gudang |
| ekosistem digital, transformasi digital | (hapus, sebutkan sistem yang dimaksud) |
| harmonisasi, sinergi | sinkronisasi data antarbasis data |
| tulang punggung, jantung dari, pilar utama | (hapus, sebutkan peran teknis) |
| memegang peranan penting | menentukan (diikuti objek konkret) |
| tak dapat dipungkiri, sudah barang tentu | (hapus) |
| dalam konteks ini, sehubungan dengan hal tersebut | (hapus, mulai dari subjek) |
| berangkat dari | untuk memenuhi (diikuti kebutuhan spesifik) |
| lebih lanjut, lebih jauh lagi, di sisi lain | (hapus) |
| dengan demikian, pada akhirnya, secara keseluruhan | (hapus kalimatnya) |
| hal ini dikarenakan oleh fakta bahwa | penyebabnya adalah |
| yang mana | yang, atau pecah kalimat |
| , sehingga memastikan X | (pecah menjadi kalimat baru) |
| banyak penelitian menunjukkan | Fowler (2019) menunjukkan, Kleppmann (2017) mencatat |
| era digital, lanskap bisnis modern | (hapus, mulai dari Apotek Bisma) |
| efektivitas | konsistensi data, keandalan transaksi |
| Kondisi A / B / C | Monolith Terpusat, EDA Tanpa Proteksi, EDA dengan Proteksi |

---

## Lampiran A.2 : Register, Bukan Penurunan Formalitas

Tabel ini mencabut anjuran keliru v2.0. Kolom tengah adalah kata yang **dilarang**, kolom kanan adalah penggantinya yang baku.

| Makna | Ragam percakapan (DILARANG) | Ragam ilmiah (WAJIB) |
|---|---|---|
| menggunakan | memakai, pakai, dipakai | menggunakan, digunakan |
| melalui | lewat | melalui |
| membuat | bikin, buat | membuat, menyusun, merancang |
| menjadi diketahui | ketahuan | teridentifikasi, terdeteksi, diketahui |
| tampak | kelihatan | tampak, terlihat |
| memeriksa | ngecek, cek | memeriksa, menelaah, memverifikasi |
| karena | gara-gara | karena, disebabkan oleh |
| seperti | kayak | seperti, sebagaimana |
| sangat | banget | sangat |
| tidak | nggak, ndak | tidak |
| tetapi | tapi | tetapi, namun (di awal kalimat) |
| kemudian | terus | kemudian, selanjutnya |
| sudah | udah | sudah, telah |
| memperoleh | dapetin, dapat | memperoleh, mendapatkan |
| menempatkan | naruh, taruh | menempatkan, meletakkan |
| bersama | bareng | bersama |
| memberikan | ngasih | memberikan |
| mengubah | merubah | mengubah |
| memengaruhi | mempengaruhi | memengaruhi |

Catatan: *"dipakai"* dilarang dalam arti *digunakan*, tetapi *"terpakai"* dan *"pemakaian"* tetap sah pada konteks teknis tertentu, misalnya *"pemakaian memori"*. Pemilihan ditetapkan sekali lalu dikonsistenkan.

---

## Lampiran A.3 : Kebakuan Diksi (KBBI dan EYD Edisi V)

| Takbaku (DILARANG) | Baku (WAJIB) |
|---|---|
| analisa | analisis |
| praktek | praktik |
| resiko | risiko |
| sistim | sistem |
| obyek, subyek | objek, subjek |
| hakekat | hakikat |
| standarisasi | standardisasi |
| frekwensi | frekuensi |
| kwalitas, kwantitas | kualitas, kuantitas |
| managemen, manajement | manajemen |
| aktifitas | aktivitas |
| produktifitas | produktivitas |
| apotik | apotek |
| nomer | nomor |
| ijin | izin |
| nasehat | nasihat |
| jadual | jadwal |
| propinsi | provinsi |
| silahkan | silakan |
| antri | antre |
| merubah | mengubah |
| mempengaruhi | memengaruhi |
| difinisi | definisi |
| komplek | kompleks |
| teknis, tehnik | teknis, teknik |
| metoda | metode |
| hipotesa | hipotesis |
| sintesa | sintesis |
| kwitansi | kuitansi |
| disain | desain |
| konkrit | konkret |
| karir | karier |
| atlit | atlet |
| trotoar (benar), trotoir | trotoar |
| di samping itu (benar), disamping itu | di samping itu |
| ke depan (benar), kedepan | ke depan |
| sekedar | sekadar |
| terlanjur | telanjur |
| himbau | imbau |
| lembab | lembap |
| nampak | tampak |
| seluler, selular | seluler |
| antar cabang, antarcabang | antarcabang (serangkai) |
| non teknis, non-teknis | nonteknis (serangkai) |
| pasca panen | pascapanen (serangkai) |
| sub sistem, sub-sistem | subsistem (serangkai) |
| multi cabang | multicabang |

Bentuk terikat antar-, non-, pasca-, sub-, multi-, pra-, semi-, swa-, dan tuna- ditulis serangkai dengan kata yang mengikutinya, kecuali diikuti nama diri atau huruf kapital.

---

## Lampiran A.4 : Daftar Pemborosan Kata

| Pemborosan (DILARANG) | Bentuk hemat (WAJIB) |
|---|---|
| adalah merupakan | adalah, atau merupakan |
| agar supaya | agar, atau supaya |
| demi untuk | demi, atau untuk |
| seperti misalnya | seperti, atau misalnya |
| disebabkan karena | disebabkan oleh, atau karena |
| namun tetapi | namun, atau tetapi |
| hanya ... saja | hanya, atau saja |
| sejak dari | sejak, atau dari |
| sangat ... sekali | sangat |
| para mahasiswa-mahasiswa | para mahasiswa |
| beberapa data-data | beberapa data |
| naik ke atas, turun ke bawah | naik, turun |
| saling bekerja sama satu sama lain | bekerja sama |
| dalam rangka untuk, guna untuk | untuk |
| dapat dikatakan bahwa | (hapus) |
| merupakan salah satu hal yang | (hapus) |
| sebagaimana telah dijelaskan sebelumnya | (hapus, atau rujuk nomor bagian) |
| pada dasarnya, secara umum | (hapus) |
| melakukan pengujian | menguji |
| melakukan analisis | menganalisis |
| melakukan pengukuran | mengukur |
| memberikan penjelasan | menjelaskan |
| mengadakan perbandingan | membandingkan |
| melakukan implementasi | mengimplementasikan |
| terlebih dahulu terlebih dulu | terlebih dahulu |
| di mana, dimana (relatif) | yang, tempat, atau pecah kalimat |

---

## Lampiran B : Indeks Regex Guard

| Kode | Guard | Regex ringkas |
|---|---|---|
| B1 | Residu prompt | `dijelaskan\s+kebutuhannya\|semoga\s+membantu\|berikut\s+adalah\s+versi` |
| B2 | Penanda sementara | `\[TODO\]\|\[Nama\]\|\bTBD\b\|\bXXX\b` |
| B5 | Label terlarang | `\b(Kondisi\|Artefak\|Skenario)\s+[ABC]\b` |
| B6 | Efektivitas | `\befektivitas\b` |
| B9 | Splice glitch | `\b(\w{4,})\s+\1\b\|,\s*,` |
| B10 | Tipografi | em dash dan kutip melengkung |
| R1 | Negasi paralel | `bukan(lah)?\s+(lagi\|sekadar)?[^.;]{2,70}(melainkan\|tetapi)` |
| R2 | Trikolon | `\b[A-Za-z]{4,},\s+[A-Za-z]{4,},\s+dan\s+[A-Za-z]{4,}\b` |
| R5 | Rekap penutup | `^\s*(Dengan\s+demikian\|Singkatnya\|Hal\s+ini\s+menunjukkan)` |
| L1 | Adjektiva kosong | `holistik\|komprehensif\|krusial\|robust\|seamless\|optimal` |
| L6 | Atribusi kabur | `banyak\s+penelitian\s+menunjukkan\|para\s+ahli\s+berpendapat` |
| S1 | Ekor partisipial | `,\s+(sehingga\s+)?(memastikan\|menghasilkan\|mencerminkan)` |
| S2 | yang mana | `\byang\s+mana\b` |
| S3 | Rantai anafora | `\b(hal\s+ini\|hal\s+tersebut)\b` |
| **N1** | Ragam percakapan | `\b(memakai\|lewat\|bikin\|ketahuan\|kelihatan\|kayak\|banget\|nggak)\b` |
| **N2** | Sapaan pembaca | `\b(Anda\|kamu\|mari\|bayangkan\|perhatikan\s+bahwa)\b` |
| **N3** | Kata ganti terlarang | `\b(saya\|aku\|kami\|kita)\b` |
| **N4** | Bentuk takbaku | `\b(analisa\|praktek\|resiko\|sistim\|obyek\|merubah\|apotik\|ijin\|nomer)\b` |
| **E1** | Kata depan serangkai | `\b(digudang\|dicabang\|dirumah\|kegudang)\b\|\bdi\s+(catat\|simpan\|kirim\|uji)\b` |
| **E2** | di mana relatif | `\bdimana\b\|,\s*di\s+mana\b` |
| **E4** | Spasi tanda baca | `\s+[.,;:]` |
| **E5** | Desimal titik | `\b\d+\.\d{1,2}\s*(ms\|detik\|%)` |
| **K1** | Kalimat tanpa subjek | `^(Dalam\|Berdasarkan\|Menurut\|Pada)[^.]{0,60}(menunjukkan\|menjelaskan\|menyatakan)` |
| **K2** | Pemborosan | `adalah\s+merupakan\|agar\s+supaya\|demi\s+untuk\|disebabkan\s+karena` |
| **K3** | Konjungsi ganda | `\bKarena\b[^.]{0,80}\bsehingga\b\|\bWalaupun\b[^.]{0,80}\bnamun\b` |

Implementasi lengkap ada pada `tools/slop_audit.py`.

---

## Lampiran C : Contoh Perbaikan Nyata

### C.1. Pembuka Bab I

**Sebelum:**
> Di era perkembangan teknologi informasi yang semakin pesat, pengelolaan data pada sektor ritel farmasi memegang peranan penting. Ketika sebuah apotek berkembang dari satu menjadi banyak cabang, pertanyaan mendasar yang muncul bukan lagi apakah sistem pencatatannya sanggup menampung volume transaksi, melainkan apakah sistem tersebut masih dapat dipercaya secara holistik.

**Sesudah:**
> Apotek Bisma mengoperasikan tiga cabang aktif dan satu gudang pusat di Kabupaten Mojokerto. Setiap unit menggunakan basis data yang berdiri sendiri. Kasir mencatat penjualan ke tabel `orders` lokal, sedangkan mutasi gudang dicatat secara terpisah oleh petugas pada akhir hari. Rekonsiliasi saldo stok dikerjakan secara manual setiap pekan melalui berkas lembar sebar.

Ciri AI yang hilang: puffery pembuka, negasi paralel, adjektiva kosong, kalimat seragam. Penanda manusia yang masuk: H-01, H-02, H-07, H-09. Register: tetap baku, tanpa satu pun kata ragam percakapan.

### C.2. Kalimat mekanisme

**Sebelum:**
> Setiap layanan menulis kejadian ke basis datanya masing-masing, sehingga memastikan konsistensi data tetap terjaga secara komprehensif di seluruh cabang yang ada.

**Sesudah:**
> Layanan Penjualan menulis nota transaksi ke tabel `orders` dan pesan kejadian ke tabel `outbox` dalam satu transaksi lokal MySQL. Proses publikasi membaca tabel `outbox` secara terpisah. Urutan penulisan tersebut menjaga saldo stok tetap sama pada ketiga cabang meskipun koneksi ke RabbitMQ terputus (F1).

Ciri AI yang hilang: ekor partisipial, adjektiva kosong, kalimat tunggal panjang. Penanda manusia: H-02, H-03, H-08, H-10.

### C.3. Klaim literatur

**Sebelum:**
> Banyak penelitian menunjukkan bahwa arsitektur microservices mampu menjembatani kesenjangan antara skalabilitas dan keandalan, sehingga menghadirkan paradigma baru dalam pengembangan sistem.

**Sesudah:**
> Kleppmann (2017) mencatat bahwa pemisahan basis data pada setiap layanan memindahkan persoalan konsistensi dari transaksi tunggal ke koordinasi antarlayanan. Fowler (2019) menambahkan bahwa pemisahan tersebut menaikkan biaya penelusuran kegagalan.

### C.4. Penutup paragraf

**Sebelum:**
> ... selisih saldo tercatat pada 11 dari 30 blok pengujian. Dengan demikian, dapat disimpulkan bahwa mekanisme proteksi memiliki peran krusial dalam menjaga konsistensi data secara menyeluruh.

**Sesudah:**
> ... selisih saldo tercatat pada 11 dari 30 blok pengujian. Pada konfigurasi EDA dengan Proteksi, selisih yang sama tidak ditemukan pada seluruh 30 blok.

### C.5. Perbaikan register yang keliru (contoh v2.0 yang dicabut)

**Versi v2.0 (DILARANG, register turun):**
> Kasir memakai aplikasi kasir, datanya dikirim lewat jaringan lokal, dan selisihnya baru ketahuan waktu stok opname.

**Versi v3.0 (BENAR, tetap berirama manusia dan tetap baku):**
> Kasir menggunakan aplikasi penjualan dengan pengiriman data melalui jaringan lokal. Selisih saldo baru teridentifikasi pada saat stok opname bulanan.

Perhatikan bahwa irama tetap terjaga, yaitu satu kalimat sedang diikuti satu kalimat pendek, tanpa satu pun kata takbaku.

### C.6. Perbaikan kalimat tanpa subjek

**Sebelum:**
> Dalam penelitian ini membandingkan tiga arsitektur, di mana masing-masing diuji pada beban yang sama.

**Sesudah:**
> Penelitian ini membandingkan tiga arsitektur. Ketiganya diuji pada tingkat beban yang sama, yaitu 10, 50, dan 100 permintaan per detik.

Dua kesalahan sekaligus diperbaiki, yaitu hilangnya subjek akibat preposisi (GUARD 39) dan "di mana" relatif (GUARD 35).

---

## Lampiran D : Rujukan Stilometri dan Arsitektur Model

Seluruh entri di bawah telah diverifikasi metadata-nya. Entri yang tidak dapat
diverifikasi tidak dicantumkan. Lihat Lampiran F untuk daftar koreksi.

**D.1. Lapis probabilitas dan algoritma sampling**

1. Bao, G., Zhao, Y., Teng, Z., Yang, L., dan Zhang, Y. (2024). Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature. ICLR 2024. arXiv:2310.05130.
2. Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., dan Finn, C. (2023). DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature. ICML 2023.
3. Verma, V., Fleisig, E., Tomlin, N., dan Klein, D. (2024). Ghostbuster: Detecting Text Ghostwritten by Large Language Models. NAACL 2024. arXiv:2305.15047.
4. Holtzman, A., Buys, J., Du, L., Forbes, M., dan Choi, Y. (2020). The Curious Case of Neural Text Degeneration. ICLR 2020. arXiv:1904.09751.
5. Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., dan Goldstein, T. (2023). A Watermark for Large Language Models. ICML 2023. arXiv:2301.10226.
6. Hans, A., dkk. (2024). Spotting LLMs with Binoculars: Zero-Shot Detection of Machine-Generated Text. arXiv:2401.12070.

**D.2. Lapis sintaksis, gaya, dan kosakata**

7. Kobak, D., González-Márquez, R., Horvát, E.-Á., dan Lause, J. (2025). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. *Science Advances*, 11(27), eadt3813. Praterbit arXiv:2406.07016.
8. Reinhart, A., dkk. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *PNAS*, 122(8), e2422455122.
9. Terčon, L., dan Dobrovoljc, K. (2025). Linguistic Characteristics of AI-Generated Text: A Survey. arXiv:2510.05136. Temuan yang dipakai: teks AI kurang beragam secara leksikal, lebih kompleks secara sintaksis, dan lebih banyak memakai nominalisasi.
10. Muñoz-Ortiz, A., Gómez-Rodríguez, C., dan Vilares, D. (2024). Contrasting linguistic patterns in human and LLM-generated news text. *Artificial Intelligence Review*. Praterbit arXiv:2308.09067.
11. Shaib, C., Elazar, Y., Li, J. J., dan Wallace, B. C. (2024). Detection and Measurement of Syntactic Templates in Generated Text. EMNLP 2024. Dasar metrik *templates-per-token* pada GUARD 22.
12. Shaib, C., Barrow, J., Sun, J., Siu, A. F., Wallace, B. C., dan Nenkova, A. (2024). Standardizing the Measurement of Text Diversity. arXiv:2403.00553. Dasar metrik *compression ratio* pada GUARD 22.

**D.3. Lapis wacana dan perilaku model**

13. Shaib, C., Chakrabarty, T., Garcia-Olano, D., dan Wallace, B. C. (2025). Measuring AI "Slop" in Text. arXiv:2509.19163 (v2, Januari 2026). Taksonomi tiga tema, sebelas kode, beserta pemetaannya ke metrik otomatis. Data dan panduan anotasi: github.com/cshaib/slop.
14. Meister, C., Pimentel, T., Haller, P., Jäger, L., Cotterell, R., dan Levy, R. (2021). Revisiting the Uniform Information Density Hypothesis. EMNLP 2021. Dasar pengukuran densitas melalui surprisal.
15. Brown, C., Snodgrass, T., Kemper, S., Herman, R. E., dan Covington, M. A. (2008). Automatic measurement of propositional idea density from part-of-speech tagging. *Behavior Research Methods*, 40, 540-545. Dasar metrik densitas gagasan pada GUARD 21.
16. Sharma, M., dkk. (2023). Towards Understanding Sycophancy in Language Models. arXiv:2310.13548.
17. Bharadwaj, A., Malaviya, C., Joshi, N., dan Yatskar, M. (2025). Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models. arXiv:2506.05339. Lima isyarat permukaan yang dihadiahi berlebih: panjang, struktur, jargon, sikap menjilat, kekaburan.
18. Russell, J., Karpinska, M., dan Iyyer, M. (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. ACL 2025. Dasar empiris bahwa pembaca terlatih, seperti pembimbing, dapat mengenali teks AI tanpa alat bantu.
19. Wikipedia contributors. *Wikipedia:Signs of AI writing*. Panduan komunitas penyunting.

## Lampiran E : Rujukan Kebahasaan Indonesia

1. Kajian analisis kesalahan berbahasa Indonesia pada skripsi mahasiswa Program Studi Sistem Informasi STMIK Kharisma Makassar, yang memetakan kesalahan ejaan (huruf kapital, huruf miring, tanda baca), penulisan kata, kalimat, dan paragraf, dengan kesalahan huruf miring sebagai temuan terbanyak. *Retorika*, Universitas Negeri Makassar.
2. Kajian keefektifan kalimat pada skripsi mahasiswa Universitas Malikussaleh yang menemukan 339 kalimat tidak efektif, dengan sebab berupa kekeliruan bentukan bagian kalimat, kesalahan struktur, dan pemborosan kata. *Jurnal Kande*, 2(1), 2021.
3. Kajian fenomena pleonasme dalam bahasa Indonesia yang menempatkan ketidakhematan sebagai salah satu faktor utama ketidakefektifan kalimat. *Jurnal Review Pendidikan dan Pengajaran*.
4. Kajian analisis kesalahan berbahasa pada bagian pendahuluan skripsi, yang mencontohkan sinonim bertumpuk, superlatif ganda, dan penanda jamak ganda.
5. *EYD Edisi V* (Ejaan Bahasa Indonesia yang Disempurnakan, Edisi Kelima), Badan Pengembangan dan Pembinaan Bahasa, khususnya kaidah pemakaian huruf, penulisan kata depan di, ke, dari, penulisan unsur serapan, dan pemakaian huruf miring.
6. *Kamus Besar Bahasa Indonesia* Edisi V sebagai rujukan kebakuan diksi.
7. Rumusan ciri ragam bahasa ilmiah (cendekia, lugas dan jelas, formal, objektif, ringkas dan padat, bertolak dari gagasan, konsisten) sebagaimana lazim diajarkan dalam mata kuliah Bahasa Indonesia perguruan tinggi.
8. Kaidah kebahasaan karya ilmiah mengenai kata ganti impersonal (peneliti atau penulis, bukan saya atau kami) dan dominasi kalimat pasif demi objektivitas.

Rujukan pada dua lampiran ini merupakan dasar penyusunan guard, bukan bagian dari daftar pustaka skripsi. Jangan disalin ke Bab II kecuali memang relevan dengan kajian pustaka arsitektur perangkat lunak.

---

## Lampiran F : Verifikasi Metadata Bibliografi

Seluruh rujukan pada Lampiran D diperiksa langsung ke arXiv, Science Advances, PNAS,
dan Semantic Scholar sebelum dimasukkan. Tiga entri pada daftar kerja awal ternyata
keliru dan sudah dikoreksi. Koreksi ini dicatat di sini karena sitasi yang salah pada
naskah skripsi berakibat jauh lebih berat daripada satu paragraf berbau AI.

| Entri pada daftar awal | Masalah | Metadata yang benar |
|---|---|---|
| "Delving into ChatGPT usage in academic writing through excess vocabulary", penulis **Dmitri Porter dkk.** | Nama penulis keliru | **Kobak, D., González-Márquez, R., Horvát, E.-Á., dan Lause, J.** Terbit di *Science Advances* 11(27), eadt3813 (2025). arXiv:2406.07016 |
| "Measuring AI Slop in Text", penulis **Souradip Chakrabarty dkk.** | Nama penulis pertama keliru, urutan keliru | **Shaib, C., Chakrabarty, T., Garcia-Olano, D., dan Wallace, B. C.** arXiv:2509.19163 |
| "Towards Understanding Sycophancy & Alignment Tax in Large Language Models", **Stephen Casper dkk., arXiv:2602.16201** | Tidak ditemukan. Judul, penulis, dan nomor arXiv tidak terverifikasi | Diganti dua rujukan terverifikasi: **Sharma dkk. (2023), arXiv:2310.13548** untuk sycophancy, dan **Bharadwaj dkk. (2025), arXiv:2506.05339** untuk bias isyarat permukaan pada model penghadiah |
| "Linguistic Characteristics of AI-Generated Text: A Survey" | Penulis benar, nomor arXiv belum tercantum | **Terčon, L., dan Dobrovoljc, K. (2025), arXiv:2510.05136** |
| "Exploring linguistic fingerprints in human and AI-generated texts" (ScienceDirect) | Metadata tidak lengkap dan belum terverifikasi | Tidak dicantumkan. Klaim yang hendak didukung (keragaman leksikal AI lebih sempit) sudah tercakup oleh rujukan 9 dan 10 yang terverifikasi |

**Aturan yang berlaku seterusnya:** setiap rujukan yang masuk ke naskah atau ke guard ini
wajib diverifikasi ke sumber primer lebih dahulu. Sitasi yang tidak dapat diverifikasi
tidak dipakai, sekalipun klaimnya terdengar benar. Ini bagian dari GUARD 60.

---

## Lampiran G : Peta Rujukan ke Guard ke Alat

Tabel ini menjawab pertanyaan "aturan ini dari mana asalnya" untuk setiap guard utama.

| Rujukan | Temuan inti | Guard | Implementasi |
|---|---|---|---|
| Holtzman dkk. (2020) | Manusia menghindari jalur berprobabilitas tertinggi | G-03, G-08, G-27 | `deep_audit.py` (surprisal) |
| Bao dkk. (2024) | Teks mesin di puncak lokal kurva probabilitas bersyarat | G-56, G-58 | `deep_audit.py` (curvature d) |
| Verma dkk. (2024) | Jejak bertahan tanpa akses bobot model | Bagian 3.8.3 | dasar argumen, bukan metrik |
| Kirchenbauer dkk. (2023) | Tanda air statistik pada keluaran komersial | Bagian 3.8.4 | dasar peringatan integritas |
| Kobak dkk. (2025) | Lonjakan kosakata penanda | G-06 | `slop_audit.py` (L1-L5) |
| Reinhart dkk. (2025) | Klausa partisipial, nominalisasi, koordinasi frasal | G-16, G-17, G-20 | `slop_audit.py` (S1, S7, S8) |
| Terčon dan Dobrovoljc (2025) | Keragaman leksikal rendah, nominalisasi tinggi | G-16, G-50 | `slop_audit.py` (MATTR, D2) |
| Muñoz-Ortiz dkk. (2024) | Sebaran panjang kalimat lebih sempit | G-07, G-24 | `slop_audit.py` (I1-I6) |
| Shaib dkk. (2024, templat) | Templat sintaksis berulang | G-51 | `slop_audit.py` (D3) |
| Shaib dkk. (2024, diversity) | Compression ratio sebagai ukuran repetisi | G-50 | `slop_audit.py` (D2) |
| Shaib dkk. (2025, slop) | Taksonomi slop, Density dan Tone sebagai prediktor kuat | G-49, G-52, G-53, G-54, G-55 | `slop_audit.py` (D1, D4, D5, D6) |
| Meister dkk. (2021) | Uniform Information Density | G-57 | `deep_audit.py` (CV surprisal) |
| Brown dkk. (2008) | Propositional idea density | G-49 | `slop_audit.py` (D1) |
| Sharma dkk. (2023) | Sycophancy dari RLHF | G-13, G-25 | `slop_audit.py` (R3, R4) |
| Bharadwaj dkk. (2025) | Panjang, struktur, jargon, menjilat, kabur | G-23, G-53, G-54 | `slop_audit.py` (L7, D5, D6) |
| Russell dkk. (2025) | Pembaca terlatih mengenali teks AI tanpa alat | Bagian 11 | dasar sasaran guard: pembaca, bukan detektor |
| Kajian kesalahan berbahasa skripsi (Lampiran E) | Ejaan, huruf miring, pemborosan kata | G-33 sampai G-40 | `slop_audit.py` (N, E, K) |
| EYD Edisi V dan KBBI V | Kaidah baku | G-31 sampai G-38 | `slop_audit.py` (B11-B17) |

---

## Lampiran H : Alur Kerja Ringkas

```bash
# sekali saja
pip install -r tools/requirements.txt                      # torch opsional
python tools/invariant_check.py --init-terms tools/terms.json
python tools/slop_audit.py --calibrate tulisan_lama/*.md

# setiap kali menyunting satu berkas
make snapshot
python tools/slop_audit.py REVISI_BAB_1.md --show 6
python tools/deep_audit.py REVISI_BAB_1.md --topk 12
#   ... kerjakan delapan lintasan pada Bagian 7, paragraf demi paragraf ...
python tools/slop_audit.py REVISI_BAB_1.md --show 4
python tools/invariant_check.py .deslop/REVISI_BAB_1.before.md REVISI_BAB_1.md \
    --terms tools/terms.json        # WAJIB, penentu akhir
```

Prosedur lengkap untuk agen AI ada pada `DESLOP_AGENT.md`.
