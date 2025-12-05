# 🏦 Aplikasi Pengajuan Kredit PT. JKL  
Aplikasi sederhana berbasis **Flask** untuk mengelola proses pengajuan kredit mulai dari input data, verifikasi marketing, hingga approval atau reject oleh atasan.  
Seluruh data disimpan secara **in-memory** menggunakan dictionary Python, sehingga cocok untuk demonstrasi atau tugas.

---

## 🚀 Fitur Utama

### 1. Pengajuan Kredit Baru
Pengguna dapat menambahkan pengajuan baru dengan data:
- Nama Konsumen  
- NIK  
- Dealer  
- Tipe Kendaraan  
- Harga  
- Tenor Kredit  

### 2. Daftar Pengajuan
Menampilkan semua pengajuan yang telah masuk, meliputi:
- ID  
- Nama Konsumen  
- Dealer  
- Status  
- Tombol menuju halaman detail  

### 3. Detail Pengajuan
Menampilkan informasi lengkap serta aksi lanjutan:
- Verifikasi oleh Marketing  
- Approve oleh Atasan  
- Reject oleh Atasan  

### 4. Verifikasi Marketing
Marketing dapat:
- Menandai dokumen lengkap → status menjadi `MENUNGGU_APPROVAL`
- Menandai revisi → status menjadi `REVISI`
Disertai catatan opsional.

### 5. Approval & Reject
Atasan dapat memberikan keputusan akhir:
- Approve → `DISETUJUI`
- Reject → `DITOLAK`

---
