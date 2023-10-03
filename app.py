from flask import Flask, url_for, render_template, request
from markupsafe import escape
import pandas

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quan-ly-sv")
def quan_ly_sv():
    return render_template("quan-ly-sv.html")


@app.route("/mon-hoc")
def mon_hoc():
    return render_template("mon-hoc.html")


@app.route("/danh-sach-gv")
def danh_sach_giang_vien():
    return render_template("danh-sach-gv.html")


@app.route("/them-ds-gv", methods=['GET', 'POST'])
def them_ds_gv():
    if request.method == 'POST':
        if 'excelFile' not in request.files:
            return "No file uploaded"

        file = request.files['excelFile']

        if file.filename == '':
            return "No file selected"

        if file:
            destination = 'uploads/' + file.filename
            file.save(destination)
            return "File uploaded successfully!"

    return render_template('danh-sach-gv.html')
