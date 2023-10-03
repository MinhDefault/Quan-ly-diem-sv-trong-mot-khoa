import pandas as pd
from flask import Flask, url_for, render_template, request
from markupsafe import escape
from models import *

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/diem-sv"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    lop = Lop(ten_lop="DCCTCLC66A1", ma_gv= 2)
    db.session.add(lop)
    lop = Lop(ten_lop="DCCTCLC66A2", ma_gv= 1)
    db.session.add(lop)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()