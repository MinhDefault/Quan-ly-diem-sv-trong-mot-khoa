from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lop(db.Model):
    ma_lop = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String, nullable=False)
    ma_gv = Column(Integer, ForeignKey("thong_tin_gv.ma_gv"), nullable=False)


class Thong_tin_sv(db.Model):
    ma_sv = Column(Integer, primary_key=True, autoincrement=True)
    ho_lot = Column(String, nullable=False)
    ten_den = Column(String, nullable=False)
    ngay_sinh = Column(String, nullable=False)
    gioi_tinh = Column(String, nullable=False)
    faculty = Column(String, nullable=False)
    khoa = Column(Integer, nullable=False)
    ma_lop = Column(Integer, ForeignKey("lop.ma_lop"), nullable=False)
    que_quan = Column(String, nullable=False)
    so_dt = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Thong_tin_gv(db.Model):
    ma_gv = Column(Integer, primary_key=True, autoincrement=True)
    ho_lot = Column(String, nullable=False)
    ten_den = Column(String, nullable=False)
    chuc_vu = Column(String, nullable=False)


class Mon_hoc(db.Model):
    ma_mh = Column(Integer, primary_key=True, nullable=False)
    ten_mh = Column(String, nullable=False, unique=True)
    so_tc = Column(Integer, nullable=False)
    ma_gv = Column(Integer, ForeignKey("thong_tin_gv.ma_gv"), nullable=False)


class Diem_so(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ma_sv = Column(Integer, ForeignKey("thong_tin_sv.ma_sv"), nullable=False)
    ma_mh = Column(Integer, ForeignKey("mon_hoc.ma_mh"), nullable=False)
    diem_A = Column(Integer, nullable=False)
    diem_B = Column(Integer, nullable=False)
    diem_C = Column(Integer, nullable=False)

