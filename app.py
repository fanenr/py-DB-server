import psycopg as pg

from enum import Enum
from datetime import timedelta

from flask import Flask
from flask import request
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from psycopg.rows import dict_row
from passlib.context import CryptContext


conn_info = {
    "user": "arthur",
    "password": "12345",
    "dbname": "postgres",
    "host": "localhost",
    "port": 5432,
}


class Res(Enum):
    OK = 0
    INTERNAL = 1
    DUPLICATE = 2
    INCOMPLETE = 3

    NOUSER = 4
    WRONGPASSWD = 5

    @staticmethod
    def wrap(res, data=None):
        if not data:
            data = {"data": res.name}
        return {"code": res.value, **data}


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "arthur"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)


CORS(app)
jwt = JWTManager(app)
conn = pg.connect(**conn_info)
pwd = CryptContext(schemes=["bcrypt"])


def data_check(data, *fields):
    for f in fields:
        if not data.get(f):
            return False
    return True


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    token = create_access_token(get_jwt_identity())
    return {"access_token": token}


@app.route("/teacher/reg", methods=["POST"])
def teacher_reg():
    data = request.form
    if not data_check(data, "name", "username", "password"):
        return Res.wrap(Res.INCOMPLETE)

    try:
        sql = "INSERT INTO teacher (name, username, password) VALUES (%s, %s, %s)"
        value = (data["name"], data["username"], pwd.hash(data["password"]))
        with conn.transaction():
            cur = conn.cursor()
            cur.execute(sql, value)
    except pg.IntegrityError:
        return Res.wrap(Res.DUPLICATE)
    except Exception:
        return Res.wrap(Res.INTERNAL)

    cur.close()
    return Res.wrap(Res.OK)


@app.route("/student/reg", methods=["POST"])
def student_reg():
    data = request.form
    if not data_check(data, "name", "start", "username", "password"):
        return Res.wrap(Res.INCOMPLETE)

    try:
        sql = "INSERT INTO student (name, start, username, password) VALUES (%s, %s, %s, %s)"
        value = (
            data["name"],
            data["start"],
            data["username"],
            pwd.hash(data["password"]),
        )
        with conn.transaction():
            cur = conn.cursor()
            cur.execute(sql, value)
    except pg.IntegrityError:
        return Res.wrap(Res.DUPLICATE)
    except Exception:
        return Res.wrap(Res.INTERNAL)

    cur.close()
    return Res.wrap(Res.OK)


@app.route("/teacher/log", methods=["POST"])
def teacher_log():
    data = request.form
    if not data_check(data, "username", "password"):
        return Res.wrap(Res.INCOMPLETE)

    try:
        sql = "SELECT * FROM teacher WHERE username = %s"
        value = (data["username"],)
        with conn.transaction():
            cur = conn.cursor(row_factory=dict_row)
            cur.execute(sql, value)
    except Exception:
        return Res.wrap(Res.INTERNAL)

    if not (info := cur.fetchone()):
        return Res.wrap(Res.NOUSER)
    if not pwd.verify(data["password"], info["password"]):
        return Res.wrap(Res.WRONGPASSWD)

    del info["username"]
    del info["password"]

    access_token = create_access_token(identity=info["id"])
    refresh_token = create_refresh_token(identity=info["id"])

    info["access_token"] = access_token
    info["refresh_token"] = refresh_token

    cur.close()
    return Res.wrap(Res.OK, info)


@app.route("/student/log", methods=["POST"])
def student_log():
    data = request.form
    if not data_check(data, "username", "password"):
        return Res.wrap(Res.INCOMPLETE)

    try:
        sql = "SELECT * FROM student WHERE username = %s"
        value = (data["username"],)
        with conn.transaction():
            cur = conn.cursor(row_factory=dict_row)
            cur.execute(sql, value)
    except Exception:
        return Res.wrap(Res.INTERNAL)

    if not (info := cur.fetchone()):
        return Res.wrap(Res.NOUSER)
    if not pwd.verify(data["password"], info["password"]):
        return Res.wrap(Res.WRONGPASSWD)

    del info["username"]
    del info["password"]

    access_token = create_access_token(identity=info["id"])
    refresh_token = create_refresh_token(identity=info["id"])

    info["access_token"] = access_token
    info["refresh_token"] = refresh_token

    cur.close()
    return Res.wrap(Res.OK, info)


if __name__ == "__main__":
    app.run()
