from flask import Flask, request
from enum import Enum
import psycopg

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


def res_wrap(res):
    return {"code": res.value, "data": res.name}


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


if __name__ == "__main__":
    app.run()
