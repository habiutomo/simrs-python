# SIMRS (Sistem Informasi Manajemen Rumah Sakit)

SIMRS adalah aplikasi berbasis web untuk mengelola berbagai aspek operasional rumah sakit, termasuk pendaftaran pasien, jadwal janji temu, rekam medis, laporan, dan lainnya.

## Fitur Utama

- **Manajemen Pasien**: Tambah, lihat, dan kelola data pasien.
- **Jadwal Janji Temu**: Atur jadwal janji temu pasien dengan dokter.
- **Rekam Medis**: Simpan dan kelola rekam medis pasien.
- **Laporan dan Analitik**: Buat laporan dalam berbagai format, termasuk grafik dan PDF.
- **Dashboard Interaktif**: Tampilkan statistik rumah sakit dan aktivitas terbaru.

## Struktur Proyek

```
__pycache__/          # Cache Python
app.py                # File utama untuk inisialisasi aplikasi Flask
attached_assets/      # Folder untuk menyimpan aset gambar
instance/             # Folder untuk file database SQLite
models/               # Model database untuk berbagai entitas
routes/               # Rute aplikasi Flask
static/               # File statis (CSS, JS, gambar)
templates/            # Template HTML untuk Flask
utils/                # Utilitas untuk laporan dan fungsi lainnya
```

## Instalasi

1. **Clone repository ini**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Buat virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi database**:
   - File database SQLite (`simrs.db`) sudah tersedia di folder instance.

5. **Jalankan aplikasi**:
   ```bash
   flask run
   ```

6. **Akses aplikasi**:
   Buka browser dan akses `http://127.0.0.1:5000`.

## Konfigurasi

- **Variabel kunganLing**:
  - `SESSION_SECRET`: Kunci rahasia untuk sesi Flask (default: `simrs-development-key`).

- **Database**:
  - Aplikasi menggunakan SQLite sebagai database default. Anda dapat mengubah URI database di file app.py pada konfigurasi `SQLALCHEMY_DATABASE_URI`.

## Penggunaan

### Menambahkan Pasien
1. Akses halaman pasien melalui menu navigasi.
2. Klik tombol "Tambah Pasien".
3. Isi formulir dan simpan.

### Membuat Laporan
1. Akses halaman laporan melalui menu navigasi.
2. Pilih jenis laporan dan periode waktu.
3. Klik "Generate" untuk membuat laporan.

## Pengembangan

### Struktur Kode
- **`app.py`**: Inisialisasi aplikasi Flask dan konfigurasi utama.
- **models**: Model database menggunakan SQLAlchemy.
- **routes**: Blueprint untuk rute aplikasi.
- **utils**: Fungsi utilitas untuk laporan dan analitik.
- **js**: File JavaScript untuk interaktivitas frontend.

### Menambahkan Rute Baru
1. Tambahkan fungsi rute di file yang sesuai di folder routes.
2. Daftarkan rute baru di app.py jika diperlukan.

### Membuat Grafik
Gunakan fungsi `generate_chart` di reports.py untuk membuat grafik berbasis data.

## Kontribusi

1. Fork repository ini.
2. Buat branch baru untuk fitur atau perbaikan Anda.
3. Kirim pull request ke branch `main`.

## Lisensi

Proyek ini dilisensikan di bawah MIT License. habizinnia@gmail.com
