from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

applications = {}   # penyimpanan data sederhana
next_id = 1

# Template HTML dasar (langsung disisipkan ke setiap halaman)
def base(content):
    return f"""
    <!doctype html>
    <html>
    <head>
        <title>Aplikasi Kredit</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            table, th, td {{ border: 1px solid #ccc; border-collapse: collapse; padding: 6px; }}
            .btn {{ padding:6px 10px; text-decoration:none; border:1px solid #000; margin:2px; }}
            .primary {{ background:#007bff; color:white; }}
            .success {{ background:#28a745; color:white; }}
            .danger {{ background:#dc3545; color:white; }}
        </style>
    </head>
    <body>
        <h1>Aplikasi Pengajuan Kredit PT. JKL</h1>
        {content}
    </body>
    </html>
    """

@app.route("/")
def index():
    rows = ""
    for app_id, app in applications.items():
        rows += f"""
        <tr>
            <td>{app_id}</td>
            <td>{app['nama_konsumen']}</td>
            <td>{app['dealer']}</td>
            <td>{app['status']}</td>
            <td><a class='btn' href='/pengajuan/{app_id}'>Detail</a></td>
        </tr>
        """

    content = f"""
    <a class='btn primary' href='/pengajuan/baru'>+ Pengajuan Baru</a>
    <h2>Daftar Pengajuan</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Nama Konsumen</th>
            <th>Dealer</th>
            <th>Status</th>
            <th>Aksi</th>
        </tr>
        {rows if rows else "<tr><td colspan='5'>Belum ada pengajuan</td></tr>"}
    </table>
    """

    return base(content)

@app.route("/pengajuan/baru", methods=["GET", "POST"])
def new_application():
    global next_id

    if request.method == "POST":
        applications[next_id] = {
            "nama_konsumen": request.form["nama_konsumen"],
            "nik": request.form["nik"],
            "dealer": request.form["dealer"],
            "tipe_kendaraan": request.form["tipe_kendaraan"],
            "harga": request.form["harga"],
            "tenor": request.form["tenor"],
            "status": "BARU",
            "catatan": ""
        }
        next_id += 1
        return redirect("/")

    content = """
    <h2>Form Pengajuan Kredit</h2>
    <form method="post">
        <p>Nama Konsumen:<br><input name="nama_konsumen" required></p>
        <p>NIK:<br><input name="nik" required></p>
        <p>Dealer:<br><input name="dealer" required></p>
        <p>Tipe Kendaraan:<br><input name="tipe_kendaraan" required></p>
        <p>Harga:<br><input name="harga" required></p>
        <p>Tenor:<br><input name="tenor" required></p>
        <button class="btn primary">Simpan</button>
        <a class="btn" href="/">Kembali</a>
    </form>
    """
    return base(content)

@app.route("/pengajuan/<int:app_id>")
def detail_application(app_id):
    app = applications.get(app_id)
    if not app:
        return base("<h3>Data tidak ditemukan</h3>")

    content = f"""
    <h2>Detail Pengajuan #{app_id}</h2>
    <p><b>Nama Konsumen:</b> {app['nama_konsumen']}</p>
    <p><b>NIK:</b> {app['nik']}</p>
    <p><b>Dealer:</b> {app['dealer']}</p>
    <p><b>Tipe Kendaraan:</b> {app['tipe_kendaraan']}</p>
    <p><b>Harga:</b> {app['harga']}</p>
    <p><b>Tenor:</b> {app['tenor']} bulan</p>
    <p><b>Status:</b> {app['status']}</p>
    <p><b>Catatan:</b> {app['catatan']}</p>

    <h3>Aksi</h3>
    <a class='btn' href='/pengajuan/{app_id}/verifikasi'>Verifikasi (Marketing)</a>
    <a class='btn success' href='/pengajuan/{app_id}/approve'>Approve (Atasan)</a>
    <a class='btn danger' href='/pengajuan/{app_id}/reject'>Reject (Atasan)</a>

    <br><br><a class='btn' href='/'>Kembali</a>
    """
    return base(content)

@app.route("/pengajuan/<int:app_id>/verifikasi", methods=["GET", "POST"])
def verifikasi(app_id):
    app = applications.get(app_id)
    if not app:
        return base("<h3>Data tidak ditemukan</h3>")

    if request.method == "POST":
        hasil = request.form["hasil"]
        catatan = request.form.get("catatan", "")

        if hasil == "lengkap":
            app["status"] = "MENUNGGU_APPROVAL"
        else:
            app["status"] = "REVISI"

        app["catatan"] = catatan
        return redirect(f"/pengajuan/{app_id}")

    content = f"""
    <h2>Verifikasi Pengajuan #{app_id}</h2>
    <form method="post">
        <p>
            <label><input type="radio" name="hasil" value="lengkap" checked> Dokumen Lengkap</label><br>
            <label><input type="radio" name="hasil" value="revisi"> Perlu Revisi</label>
        </p>
        <p>Catatan:<br><textarea name="catatan" rows="4" cols="40"></textarea></p>
        <button class="btn primary">Simpan</button>
        <a class="btn" href="/pengajuan/{app_id}">Batal</a>
    </form>
    """
    return base(content)

@app.route("/pengajuan/<int:app_id>/approve")
def approve(app_id):
    app = applications.get(app_id)
    if app:
        app["status"] = "DISETUJUI"
    return redirect(f"/pengajuan/{app_id}")

@app.route("/pengajuan/<int:app_id>/reject")
def reject(app_id):
    app = applications.get(app_id)
    if app:
        app["status"] = "DITOLAK"
    return redirect(f"/pengajuan/{app_id}")

if __name__ == "__main__":
    app.run(debug=True)
