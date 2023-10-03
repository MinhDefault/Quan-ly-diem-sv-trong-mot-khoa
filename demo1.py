import pandas as pd
from flask import Flask, url_for, render_template, request
from markupsafe import escape
from models import *
import numpy
from psycopg2.extensions import register_adapter, AsIs
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/diem-sv"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Create the database engine
engine = create_engine('postgresql://username:password@localhost:5432/database_name')

# Create the sessionmaker and bind it to the engine
Session = sessionmaker(bind=engine)

# Create a session
session = Session()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quan-ly-sv")
def quan_ly_sv():
    sinh_vien = Thong_tin_sv.query.all()
    return render_template("quan-ly-sv.html", sinh_vien=sinh_vien)


@app.route("/them-ds-sv", methods=['GET', 'POST'])
def them_ds_sv():
    if request.method == 'POST':
        if 'excelFile' not in request.files:
            return "No file uploaded"

        file = request.files['excelFile']

        if file.filename == '':
            return "No file selected"

        if file:
            destination = 'uploads/' + file.filename
            file.save(destination)
            data_sv = pd.read_excel(destination)
            data_shape = data_sv.shape
            for dt in range(data_shape[0]):
                ho_lot = data_sv.iloc[dt, 0]
                ten = data_sv.iloc[dt, 1]
                ngay_sinh = data_sv.iloc[dt, 2]
                gioi_tinh = data_sv.iloc[dt, 3]
                faculty = data_sv.iloc[dt, 4]
                khoa = data_sv.iloc[dt, 5]
                ma_lop = data_sv.iloc[dt, 6]
                que_quan = data_sv.iloc[dt, 7]
                so_dt = data_sv.iloc[dt, 8]
                email = data_sv.iloc[dt, 9]
                thong_tin_sv = Thong_tin_sv(ho_lot=ho_lot, ten_den=ten, ngay_sinh=ngay_sinh,
                                            gioi_tinh=gioi_tinh, faculty=faculty, khoa=khoa,
                                            ma_lop=ma_lop, que_quan=que_quan, so_dt=so_dt,
                                            email=email)
                db.session.add(thong_tin_sv)
            db.session.commit()
            return "update thanh cong"


@app.route("/mon-hoc")
def mon_hoc():
    query = db.session.query(Mon_hoc.ma_gv, Mon_hoc.ma_mh, Mon_hoc.ten_mh, Mon_hoc.so_tc, Thong_tin_gv.ten_den,
                               Thong_tin_gv.ho_lot) \
        .join(Thong_tin_gv, Mon_hoc.ma_gv == Thong_tin_gv.ma_gv) \

    # Execute the query
    results = query.all()

    return render_template("mon-hoc.html", results=results)


@app.route("/them-diem-sv", methods=['GET', 'POST'])
def them_diem_sv():
    if request.method == 'POST':
        if 'excelFile' not in request.files:
            return "No file uploaded"

        file = request.files['excelFile']

        if file.filename == '':
            return "No file selected"

        if file:
            destination = 'uploads/' + file.filename
            file.save(destination)
            data_diem = pd.read_excel(destination)
            data_shape = data_diem.shape
            for dt in range(data_shape[0]):
                ma_sv = data_diem.iloc[dt, 0]
                ma_mh = data_diem.iloc[dt, 1]
                diem_A = data_diem.iloc[dt, 2]
                diem_B = data_diem.iloc[dt, 3]
                diem_C = data_diem.iloc[dt, 4]
                diem_sv = Diem_so(ma_sv=ma_sv, ma_mh=ma_mh, diem_A=diem_A, diem_B=diem_B, diem_C=diem_C)
                db.session.add(diem_sv)
            db.session.commit()
            return "update thanh cong"


@app.route("/danh-sach-diem-sv", methods=['GET', 'POST'])
def danh_sach_diem_sv():
    ma_mh = request.args.get('ma_mh')
    ten_mh = Mon_hoc.query.get(ma_mh).ten_mh
    query = db.session.query(Diem_so.ma_sv, Diem_so.diem_A, Diem_so.diem_B, Diem_so.diem_C, Thong_tin_sv.ten_den,
                               Thong_tin_sv.ho_lot, Thong_tin_sv.faculty, Thong_tin_sv.khoa) \
        .join(Thong_tin_sv, Diem_so.ma_sv == Thong_tin_sv.ma_sv) \

    # Execute the query
    results = query.all()

    return render_template("danh-sach-diem-sv.html", results=results, mon_hoc=ten_mh)


@app.route("/diem-sv", methods=['GET', 'POST'])
def diem_sv():
    ma_sv = request.args.get("ma_sv")
    ten_sv = Thong_tin_sv.query.get(ma_sv)
    ho_lot = ten_sv.ho_lot
    ten = ten_sv.ten_den
    ho_ten = ho_lot + " "+ ten
    mon_hoc = Diem_so.query.filter_by(ma_sv=ma_sv)
    # diem_so = Diem_so.query.filter_by(ma_sv=ma_sv)
    # diem_a = diem_so.diem_A
    # diem_b = diem_so.diem_A
    # diem_c = diem_so.diem_C
    
    return render_template("bang-diem-sv.html", ten_sv=ho_ten, mon_hoc=mon_hoc)


@app.route("/danh-sach-gv")
def danh_sach_giang_vien():
    giang_vien = Thong_tin_gv.query.all()
    return render_template("danh-sach-gv.html", giang_vien=giang_vien)


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
            data_gv = pd.read_excel(destination)
            data_shape = data_gv.shape
            for dt in range(data_shape[0]):
                hot_lot = data_gv.iloc[dt, 0]
                ten = data_gv.iloc[dt, 1]
                chuc_vu = data_gv.iloc[dt, 2]
                thong_tin_gv = Thong_tin_gv(ho_lot=hot_lot, ten_den=ten, chuc_vu=chuc_vu)
                db.session.add(thong_tin_gv)
            db.session.commit()
            return "update thanh cong"

    return render_template('danh-sach-gv.html')
