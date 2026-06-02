# Panduan Refactoring: Single Responsibility Principle (SRP)

Dokumen ini berisi panduan teknis langkah demi langkah jika Anda ingin me-refactor (merombak) kode aplikasi `pol-lapor` agar sepenuhnya mematuhi **Single Responsibility Principle (SRP)**. Prinsip SRP menyatakan bahwa *setiap kelas, fungsi, atau file hanya boleh memiliki satu alasan untuk berubah (satu tanggung jawab spesifik).*

---

## 1. Refactoring pada `PenangananProvider`
File `lib/logic/providers/penanganan_provider.dart` saat ini memiliki tanggung jawab lintas domain (State, Tracking, Notifikasi, Auth).

### Apa yang harus diubah?
- **Pindahkan Logika Notifikasi:** 
  Cabut fungsi `_kirimNotifikasiPelapor()` dari file ini. Buat file baru bernama `lib/logic/services/notifikasi_service.dart`. `PenangananProvider` cukup memanggil `NotifikasiService.kirimNotifUpdate(...)`.
- **Pindahkan Logika Tracking:** 
  Cabut fungsi `_insertTrackingLog()`. Pindahkan logika ini murni ke dalam `TrackingProvider` atau buat `TrackingService`.
- **Pindahkan Logika Update Status User:**
  Di dalam `updateProgresLaporan`, ada kode untuk meng-update `is_busy` pengguna menjadi `false`. Logika modifikasi profil pengguna harusnya ada di `UserProvider` atau `AuthService`.
- **(Opsional) Gunakan UseCase:** 
  Jika ingin lebih ketat, `PenangananProvider` seharusnya tidak mengeksekusi logika penyimpanan secara langsung. Buat folder `lib/domain/usecases/` lalu buat `UpdatePenangananUseCase.dart`. Provider hanya meneruskan perintah dari UI ke UseCase tersebut.

---

## 2. Refactoring pada `DetailLaporanScreen`
File `lib/presentation/screens/pelapor/detail_laporan_screen.dart` memiliki panjang hingga 600+ baris karena menampung semua logika *layouting* UI secara mandiri.

### Apa yang harus diubah?
Pecah file tunggal ini menjadi beberapa komponen (widget) mandiri. Buat folder baru: `lib/presentation/widgets/pelapor/` dan pisahkan kode berikut:

#### A. Buat `InfoLaporanCard.dart`
- **Isi:** Pindahkan fungsi `_buildInfoCard` (menampilkan judul kerusakan, status, lokasi, dll) ke file ini.
- **Tanggung Jawab:** Hanya untuk merender kartu informasi utama laporan.

#### B. Buat `FotoKerusakanCard.dart`
- **Isi:** Pindahkan fungsi `_buildPhotoCard`.
- **Tanggung Jawab:** Hanya fokus mengatur logika apakah foto berasal dari *network* atau *lokal*, lalu merendernya.

#### C. Buat `TrackingTimelineCard.dart`
- **Isi:** Pindahkan fungsi `_buildTrackingCard` beserta perhitungan `stepsData`, penentuan indikator aktif, dan ekstensi waktu.
- **Tanggung Jawab:** Hanya untuk menampilkan timeline 5-langkah (dari Menunggu hingga Selesai).

#### D. Buat `FotoProgresCard.dart` & `BuktiSelesaiCard.dart`
- **Isi:** Pindahkan `_buildFotoProgresCard` dan `_buildHasilPerbaikanCard` ke widget masing-masing.

**Hasil Akhir di `DetailLaporanScreen`:**
File layar utama Anda (DetailLaporanScreen) nantinya hanya berisi sekitar 50 baris kode yang memanggil widget-widget tersebut:
```dart
body: ListView(
  children: [
    InfoLaporanCard(laporan: laporan, penanganan: penanganan),
    FotoKerusakanCard(laporan: laporan),
    TrackingTimelineCard(),
    if (adaProgres) FotoProgresCard(penanganan: penanganan),
    if (isSelesai) BuktiSelesaiCard(penanganan: penanganan),
  ]
)
```

---

## 3. Evaluasi Model dan Data Layer
- **Pisahkan Entity dan Model (Strict Clean Architecture)**:
  Saat ini `LaporanLokal` bertugas ganda sebagai *Entity* (bisnis) dan *Data Model* (penyimpanan lokal Hive). Dalam SRP murni, entitas bisnis murni tidak boleh bergantung pada *library* pihak ketiga (seperti `@HiveType`). 
  > *Catatan: Untuk Flutter, pemisahan tingkat ini sering dianggap *over-engineering* kecuali untuk aplikasi tingkat *Enterprise* (sangat besar).*

## Kapan Harus Melakukan Ini?
Jangan terburu-buru melakukan semuanya sekaligus. Lakukan refactoring secara perlahan-lahan. Memecah `DetailLaporanScreen` ke banyak *widget* kecil adalah langkah terbaik pertama yang bisa Anda lakukan karena dampaknya sangat signifikan dalam mempermudah tim (atau Anda sendiri) membaca UI kedepannya.
