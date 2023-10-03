from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Diem_so_1(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ma_sv = Column(Integer, nullable=False)
    ma_mh = Column(Integer, nullable=False)
    diem_A = Column(Integer, nullable=False)
    diem_B = Column(Integer, nullable=False)
    diem_C = Column(Integer, nullable=False)

