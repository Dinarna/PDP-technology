# 🏦 Aplikasi Pengajuan Kredit – Flask Mini System

Aplikasi ini merupakan **sistem pengajuan kredit sederhana** berbasis **Flask** dengan workflow:  
**Sales → Marketing (Verifikasi) → Atasan (Approval)**.  
Data disimpan menggunakan **in-memory dictionary** sehingga aplikasi cocok untuk demo, tugas kampus, atau prototipe.

---

## 🚀 Fitur Utama

### ✔️ 1. Dashboard Pengajuan
- Menampilkan seluruh pengajuan kredit dalam bentuk tabel.
- Informasi ditampilkan: ID, Nama Konsumen, Dealer, Status.
- Tombol menuju halaman detail pengajuan.

### ✔️ 2. Pengajuan Baru (Sales)
Form untuk membuat pengajuan kredit baru, mencakup:
- Nama Konsumen
- NIK
- Dealer / Sales
- Tipe Kendaraan
- Harga Kendaraan
- Tenor (bulan)

Status awal setiap pengajuan adalah **"BARU"**.

### ✔️ 3. Detail Pengajuan
Halaman detail menampilkan:
- Data konsumen
- Data kendaraan
- Catatan verifikasi
- Status proses
- Aksi Marketing & Atasan

### ✔️ 4. Verifikasi Marketing
Marketing dapat memberikan hasil verifikasi:
- Dokumen lengkap → status menjadi **MENUNGGU_APPROVAL**
- Perlu revisi → status menjadi **REVISI**
- Menambahkan catatan

### ✔️ 5. Approval Atasan
Atasan dapat memilih:
- **Approve** → status **DISETUJUI**
- **Reject** → status **DITOLAK**

---

## 🧩 Endpoint & Workflow

| Endpoint | Method | Deskripsi |
|----------|--------|------------|
| `/` | GET | Dashboard daftar pengajuan |
| `/pengajuan/baru` | GET/POST | Form membuat pengajuan baru |
| `/pengajuan/<id>` | GET | Detail pengajuan |
| `/pengajuan/<id>/verifikasi` | GET/POST | Verifikasi marketing |
| `/pengajuan/<id>/approve` | GET | Persetujuan oleh atasan |
| `/pengajuan/<id>/reject` | GET | Penolakan oleh atasan |

---

## 🗂 Struktur Program

Aplikasi ini tidak menggunakan folder templates; semua HTML dibuat dengan `render_template_string`.

Struktur utama:
