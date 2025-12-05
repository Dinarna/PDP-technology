from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Penyimpanan data sederhana (in-memory)
applications = {}   # key: id (int), value: dict data pengajuan
next_id = 1         # auto-increment id

# Template HTML sangat sederhana (pakai render_template_string)
BASE_HTML = """
<!doctype html>
<html>
<head>
    <title>Aplikasi Pengajuan Kredit</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .btn {{ padding: 6px 10px; text-decoration: none; border: 1px solid #333; margin-right: 4px; }}
        .btn-primary {{ background: #007bff; color: white; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-danger {{ background: #dc3545; color: white; }}
        table, th, td {{ border: 1px solid #ccc; border-collapse: collapse; padding: 6px; }}
    </style>
</head>
<body>
    <h1>Aplikasi Pengajuan Kredit PT. JKL</h1>
    <p><a class="btn btn-primary" href="{{ url_for('new_application') }}">+ Pengajuan Baru</a></p>
    {% block content %}{% endblock %}
</body>
</html>
"""

@app.route("/")
def index():
    # Dashboard: daftar semua pengajuan
    html = """
    {% extends "base" %}
    {% block content %}
    <h2>Daftar Pengajuan</h2>
    {% if apps %}
    <table>
        <tr>
            <th>ID</th>
            <th>Nama Konsumen</th>
            <th>Nama Dealer</th>
            <th>Status</th>
            <th>Aksi</th>
        </tr>
        {% for app_id, app in apps.items() %}
        <tr>
            <td>{{ app_id }}</td>
            <td>{{ app['nama_konsumen'] }}</td>
            <td>{{ app['dealer'] }}</td>
            <td>{{ app['status'] }}</td>
            <td>
                <a class="btn" href="{{ url_for('detail_application', app_id=app_id) }}">Detail</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>Belum ada pengajuan.</p>
    {% endif %}
    {% endblock %}
    """
    return render_template_string(html, apps=applications, **{"base": BASE_HTML})

@app.route("/pengajuan/baru", methods=["GET", "POST"])
def new_application():
    global next_id

    if request.method == "POST":
        # Ambil data dari form
        nama_konsumen = request.form.get("nama_konsumen")
        nik = request.form.get("nik")
        dealer = request.form.get("dealer")
        tipe_kendaraan = request.form.get("tipe_kendaraan")
        harga = request.form.get("harga")
        tenor = request.form.get("tenor")

        # Simpan ke "database" sederhana
        applications[next_id] = {
            "nama_konsumen": nama_konsumen,
            "nik": nik,
            "dealer": dealer,
            "tipe_kendaraan": tipe_kendaraan,
            "harga": harga,
            "tenor": tenor,
            "status": "BARU",
            "catatan": ""
        }
        next_id += 1

        return redirect(url_for("index"))

    # Jika GET, tampilkan form input pengajuan
    html = """
    {% extends "base" %}
    {% block content %}
    <h2>Form Pengajuan Kredit (Sales Dealer)</h2>
    <form method="post">
        <p>
            Nama Konsumen:<br>
            <input type="text" name="nama_konsumen" required>
        </p>
        <p>
            NIK:<br>
            <input type="text" name="nik" required>
        </p>
        <p>
            Dealer / Sales:<br>
            <input type="text" name="dealer" required>
        </p>
        <p>
            Tipe Kendaraan:<br>
            <input type="text" name="tipe_kendaraan" required>
        </p>
        <p>
            Harga Kendaraan:<br>
            <input type="number" name="harga" required>
        </p>
        <p>
            Tenor (bulan):<br>
            <input type="number" name="tenor" required>
        </p>
        <p>
            <button class="btn btn-primary" type="submit">Simpan Pengajuan</button>
            <a class="btn" href="{{ url_for('index') }}">Kembali</a>
        </p>
    </form>
    {% endblock %}
    """
    return render_template_string(html, **{"base": BASE_HTML})

@app.route("/pengajuan/<int:app_id>")
def detail_application(app_id):
    app_data = applications.get(app_id)
    if not app_data:
        return "Pengajuan tidak ditemukan", 404

    html = """
    {% extends "base" %}
    {% block content %}
    <h2>Detail Pengajuan #{{ app_id }}</h2>
    <p><b>Nama Konsumen:</b> {{ app['nama_konsumen'] }}</p>
    <p><b>NIK:</b> {{ app['nik'] }}</p>
    <p><b>Dealer:</b> {{ app['dealer'] }}</p>
    <p><b>Tipe Kendaraan:</b> {{ app['tipe_kendaraan'] }}</p>
    <p><b>Harga:</b> {{ app['harga'] }}</p>
    <p><b>Tenor:</b> {{ app['tenor'] }} bulan</p>
    <p><b>Status:</b> {{ app['status'] }}</p>
    <p><b>Catatan:</b> {{ app['catatan'] }}</p>

    <h3>Aksi</h3>
    <p>
        <!-- Marketing: verifikasi -->
        <a class="btn" href="{{ url_for('verify_application', app_id=app_id) }}">Verifikasi (Marketing)</a>
        <!-- Atasan: approve / reject -->
        <a class="btn btn-success" href="{{ url_for('approve_application', app_id=app_id) }}">Approve (Atasan)</a>
        <a class="btn btn-danger" href="{{ url_for('reject_application', app_id=app_id) }}">Reject (Atasan)</a>
    </p>

    <p><a class="btn" href="{{ url_for('index') }}">Kembali ke Daftar</a></p>
    {% endblock %}
    """
    return render_template_string(html, app=app_data, app_id=app_id, **{"base": BASE_HTML})

@app.route("/pengajuan/<int:app_id>/verifikasi", methods=["GET", "POST"])
def verify_application(app_id):
    app_data = applications.get(app_id)
    if not app_data:
        return "Pengajuan tidak ditemukan", 404

    if request.method == "POST":
        hasil = request.form.get("hasil")
        catatan = request.form.get("catatan", "")

        if hasil == "lengkap":
            app_data["status"] = "MENUNGGU_APPROVAL"
        else:
            app_data["status"] = "REVISI"
        app_data["catatan"] = catatan

        return redirect(url_for("detail_application", app_id=app_id))

    html = """
    {% extends "base" %}
    {% block content %}
    <h2>Verifikasi Pengajuan #{{ app_id }} (Marketing)</h2>
    <form method="post">
        <p>
            Hasil Verifikasi:<br>
            <label><input type="radio" name="hasil" value="lengkap" checked> Dokumen Lengkap</label><br>
            <label><input type="radio" name="hasil" value="revisi"> Perlu Revisi</label>
        </p>
        <p>
            Catatan:<br>
            <textarea name="catatan" rows="4" cols="40"></textarea>
        </p>
        <p>
            <button class="btn btn-primary" type="submit">Simpan Verifikasi</button>
            <a class="btn" href="{{ url_for('detail_application', app_id=app_id) }}">Batal</a>
        </p>
    </form>
    {% endblock %}
    """
    return render_template_string(html, app_id=app_id, **{"base": BASE_HTML})

@app.route("/pengajuan/<int:app_id>/approve")
def approve_application(app_id):
    app_data = applications.get(app_id)
    if not app_data:
        return "Pengajuan tidak ditemukan", 404

    # Atasan menyetujui pengajuan
    app_data["status"] = "DISETUJUI"
    return redirect(url_for("detail_application", app_id=app_id))

@app.route("/pengajuan/<int:app_id>/reject")
def reject_application(app_id):
    app_data = applications.get(app_id)
    if not app_data:
        return "Pengajuan tidak ditemukan", 404

    # Atasan menolak pengajuan
    app_data["status"] = "DITOLAK"
    return redirect(url_for("detail_application", app_id=app_id))

# Agar BASE_HTML bisa dipakai sebagai "template base"
@app.context_processor
def inject_base_template():
    return {"base": BASE_HTML}

if __name__ == "__main__":
    # Jalankan web server lokal
    app.run(debug=True)
