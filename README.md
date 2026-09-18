# ANTI AI SLOP OPUS 5 — Toolkit Global (Acuan Utama)

Toolkit anti-AI-slop v4.0 untuk naskah akademik Indonesia. Repo ini adalah **acuan utama yang read-only**:
aturan dan skrip di sini **tidak diubah** — yang bekerja adalah command global OpenCode yang
memanggil toolkit ini dari repo mana pun secara adaptif.

## Isi toolkit (jangan diubah)

| Berkas | Peran |
|---|---|
| `ANTI_AI_SLOP_GUARD.md` | Aturan mengikat G-01–G-60 + Kontrak Invarian |
| `DESLOP_AGENT.md` | Prosedur agen 5 gerbang + 8 lintasan |
| `slop_audit.py` | Auditor permukaan (L/R/S/I/N/E/K/B/D), stdlib only |
| `invariant_check.py` | Penjaga substansi 100% (Gerbang 4), stdlib only |
| `deep_audit.py` | Audit lapis token (G-56–G-58), opsional, perlu `torch` |
| `terms.json` | Contoh istilah terkunci kasus Apotek Bisma |
| `Makefile` | Pintasan Unix (referensi; di Windows pakai perintah di bawah) |
| `requirements.txt` | Kosong untuk 2 skrip wajib; `torch+transformers` hanya untuk `deep_audit.py` |

## Command global (dipakai dari repo mana pun)

| Command | Fungsi |
|---|---|
| `/deslop-audit <berkas...>` | Gerbang 1+3: audit G-01–G-60 + ASI (lolos ≤ 25, ideal ≤ 12) |
| `/deslop-deep <berkas...>` | Lapis token: peringkat kalimat terdatar (`--topk 12`) |
| `/deslop-check <sebelum> <sesudah>` | Gerbang 4: tolak bila satu angka/sitasi menguap |
| `/deslop <berkas>` | End-to-end 5 gerbang, satu berkas + satu subbab per iterasi |
| `/deslop-calibrate <tulisan_lama...>` | Garis dasar gaya pribadi → `.slop_baseline.json` di repo aktif |

Shortcut lama `/humanize` (folder `command\`, menunjuk ke `Downloads\humanize...-v1`)
sudah dihapus. Satu-satunya yang aktif adalah `/deslop-*` di atas.

## Mekanisme kerja

1. **Acuan vs kerja.** Guard + skrip dibaca dari `B:\app\ANTI AI SLOP OPUS 5\`
   via path absolut. Snapshot (`.deslop\*.before.md`), baseline
   (`.slop_baseline.json`), dan laporan (`.deslop\*.report.md`) selalu ditulis
   di **repo aktif**, tidak pernah di folder toolkit.
2. **Adaptif konteks.** `terms.json` hanyalah contoh (outbox, Ibu Atik, F1–F6).
   Untuk dokumen lain, istilah terkunci dikunci otomatis dari dokumen itu:
   angka + satuan, sitasi, nama diri, kode identifier, span `` `kode` ``, heading.
   Istilah baru → agen berhenti dan bertanya, tidak menebak.
3. **Alur 5 gerbang** (per `DESLOP_AGENT.md`): 1 audit awal → 2 tulis ulang
   8 lintasan per paragraf → 3 audit ulang (maks 3 putaran) → 4 invarian
   (gagal = kembalikan berkas, ulangi konservatif) → 5 laporan.
4. **Windows-native.** Semua perintah memakai PowerShell (`Copy-Item`,
   `New-Item`), bukan sintaks Unix di `Makefile`.

## Contoh cepat (dari repo dokumen mana pun, PowerShell)

```powershell
# 1. Kalibrasi sekali dari tulisan lama sendiri (opsional tapi dianjurkan)
/deslop-calibrate tulisan_lama\*.md

# 2. Audit
/deslop-audit Bab1.md --show 6

# 3. De-slop end-to-end
/deslop Bab1.md

# Manual setara (tanpa command):
python "B:\app\ANTI AI SLOP OPUS 5\slop_audit.py" Bab1.md --show 6
python "B:\app\ANTI AI SLOP OPUS 5\invariant_check.py" .deslop\Bab1.before.md Bab1.md --terms "B:\app\ANTI AI SLOP OPUS 5\terms.json"
```

## Batasan jujur

Ambang ASI dan heuristik adalah alat bantu revisi, bukan bukti kepengarangan.
Skor `deep_audit.py` bersifat relatif internal (model penilai kecil) — hanya untuk
memeringkat kalimat yang perlu dikonkretkan di naskah Anda sendiri.
