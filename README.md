# SIMONA — UID Banten (Maturity Level Gudang Distribusi)

Versi ini pakai **data & formula resmi** dari dokumen "Kriteria Penilaian
Maturity Level Gudang Distribusi Tahun 2026" — bukan lagi data contoh generik.

## Yang Sudah Sesuai Dokumen Asli

- **6 Aspek** dengan bobot resmi: Sumber Daya Manusia (10), Anggaran dan
  Pengelolaan Keuangan (10), Tata Kelola (30), Infrastruktur (10),
  Peralatan Penunjang Operasional (10), Kinerja (30)
- **29 indikator** dengan rubrik kriteria Level 1-5 asli dari dokumen
- **Formula resmi**:
  ```
  Nilai Indikator = (Level / 5) x (Bobot Aspek / Jumlah Indikator dalam Aspek)
  Nilai Total     = Σ Nilai Indikator            (maksimum 100)
  Maturity Level  = Nilai Total / 20              (skala 1 - 5)
  ```
  Sudah diverifikasi cocok 100% dengan contoh perhitungan di dokumen
  (misal: semua level 5 → total 100 → Matlev 5).
- **Unit**: PLN UID Banten + 7 unit gudang (Serpong, Cikokol, Teluk Naga,
  Cikupa, Banten Utara, Banten Selatan, UP2D)
- **Data Juni 2026 sudah diisi dengan data real** dari dokumen (status
  APPROVED, periode LOCKED) — jadi begitu dibuka, dashboard sudah menampilkan
  hasil real: Serpong 98,50 (Matlev 4,92), Cikokol 92,50, dst.
- **Periode Juli 2026 dibuka (OPEN)** untuk simulasi isi assessment baru.

## Cara Jalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cara Coba

1. Masuk sebagai **UID** (PLN UID Banten) → buka **Dashboard** → pilih
   periode **06/2026 (LOCKED)** → lihat ranking 7 unit dengan skor real,
   radar chart per aspek, dan tabel monitoring lengkap.
2. Klik expander **"Contoh perhitungan"** di bagian bawah Dashboard untuk
   lihat rincian kontribusi nilai per aspek suatu unit — cocokkan dengan
   tabel di dokumen aslinya.
3. Ganti Role → masuk sebagai **UP3** (misal Serpong) → buka **Dashboard**
   → lihat skor & rata-rata level per aspek unit itu sendiri untuk periode
   Juni.
4. Ganti periode ke **07/2026 (OPEN)** → buka **Assessment** → coba isi
   level pakai slider, baca kriteria di bawahnya, simpan draft, upload
   evidence, submit.
5. Ganti Role ke **UID** → buka **Review** → approve atau kembalikan untuk
   revisi assessment Juli yang baru di-submit tadi.
6. Coba juga **Master Data** (khusus UID) → tab **Bobot Aspek** → lihat
   bobot resmi (10/10/30/10/10/30), coba ubah, lihat efeknya ke skor.

## Perbedaan dari Versi Demo Generik Sebelumnya

| | Demo generik sebelumnya | Versi UID Banten ini |
|---|---|---|
| Bobot | per indikator, manual isi rata | per **aspek**, sesuai dokumen resmi |
| Level | skor 40-100 per level (buatan) | Level 1-5 langsung sesuai dokumen |
| Formula skor | rata-rata tertimbang biasa | formula resmi PLN (nilai/20 = Matlev) |
| Data | kosong / contoh acak | **Juni 2026 diisi data real** dari dokumen |
| Unit | 1 UID + 2 UP3 + 4 ULP fiktif | UID Banten + 7 unit gudang real |

## Struktur File

```
simona_uid_banten/
├── app.py                  # entry point tunggal — navigasi role-aware (st.navigation)
├── data.py                 # seluruh data & formula perhitungan
├── ui.py                   # topbar, hero, styling bersama
├── assets/
│   ├── logo_pln.png
│   └── logo_danantara.png
└── views/
    ├── home.py              # beranda: hero+login (belum masuk) / ringkasan (sudah masuk)
    ├── dashboard.py
    ├── assessment.py        # hanya muncul di sidebar untuk role UP3/ULP
    ├── review.py             # hanya muncul di sidebar untuk role UID
    ├── master_data.py       # hanya muncul di sidebar untuk role UID
    └── notifikasi.py
```

Navigasi sidebar sekarang otomatis menyembunyikan halaman yang tidak relevan
dengan role yang sedang login (misalnya UID tidak akan melihat menu
"Assessment" sama sekali, bukan cuma diblokir saat diklik).

## Catatan Desain

- Ikon navigasi memakai Material Symbols bawaan Streamlit (`:material/...:`),
  bukan emoji — supaya terlihat konsisten dengan produk enterprise.
- Hero section di halaman Beranda memakai gradient biru + logo, bukan foto asli
  dari materi presentasi (karena file foto tersebut belum tersedia sebagai
  aset gambar terpisah). Kalau ingin memakai foto asli dari slide presentasi,
  export slide tersebut sebagai PNG/JPG dan kirimkan filenya — bisa dipasang
  sebagai background hero.

