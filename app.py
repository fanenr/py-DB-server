from flask import Flask, request
from enum import Enum
import psycopg
from psycopg.rows import dict_row

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


def res_wrap(res, data=None):
    return {"code": res.value, "data": data if data else res.name}


app = Flask(__name__)
conn = psycopg.connect(**conn_info)


def data_check(data, *fields):
    for f in fields:
        if not data.get(f):
            return False
    return True


@app.route("/teacher/reg", methods=["POST"])
def teacher_reg():
    data = request.form
    if not data_check(data, "name", "username", "password"):
        return res_wrap(Res.INCOMPLETE)

    try:
        sql = "INSERT INTO teacher (name, username, password) VALUES (%s, %s, %s)"
        value = (data["name"], data["username"], data["password"])
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(sql, value)
    except psycopg.IntegrityError:
        return res_wrap(Res.DUPLICATE)
    except Exception:
        return res_wrap(Res.INTERNAL)

    return res_wrap(Res.OK)


@app.route("/student/reg", methods=["POST"])
def student_reg():
    data = request.form
    if not data_check(data, "name", "start", "username", "password"):
        return res_wrap(Res.INCOMPLETE)

    try:
        sql = "INSERT INTO student (name, start, username, password) VALUES (%s, %s, %s, %s)"
        value = (data["name"], data["start"], data["username"], data["password"])
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(sql, value)
    except psycopg.IntegrityError:
        return res_wrap(Res.DUPLICATE)
    except Exception:
        return res_wrap(Res.INTERNAL)

    return res_wrap(Res.OK)


@app.route("/teacher/log", methods=["POST"])
def teacher_log():
    data = request.form
    if not data_check(data, "username", "password"):
        return res_wrap(Res.INCOMPLETE)

    try:
        sql = "SELECT * FROM teacher WHERE username = %s"
        value = (data["username"],)
        with conn.transaction():
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, value)
                if not (user := cur.fetchone()):
                    return res_wrap(Res.NOUSER)
                if data["password"] != user["password"]:
                    return res_wrap(Res.WRONGPASSWD)
                del user["username"]
                del user["password"]
    except Exception as e:
        return res_wrap(Res.INTERNAL)

    return res_wrap(Res.OK, user)


@app.route("/student/log", methods=["POST"])
def student_log():
    data = request.form
    if not data_check(data, "username", "password"):
        return res_wrap(Res.INCOMPLETE)

    try:
        sql = "SELECT * FROM student WHERE username = %s"
        value = (data["username"],)
        with conn.transaction():
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, value)
                if not (user := cur.fetchone()):
                    return res_wrap(Res.NOUSER)
                if data["password"] != user["password"]:
                    return res_wrap(Res.WRONGPASSWD)
                del user["username"]
                del user["password"]
    except Exception:
        return res_wrap(Res.INTERNAL)

    return res_wrap(Res.OK, user)


if __name__ == "__main__":
    app.run()
