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


class Code(Enum):
    OK = 0
    INTERNAL = 1
    DUPLICATE = 2
    FIELD_INCOMPLETE = 3


app = Flask(__name__)
conn = psycopg.connect(**conn_info)


def data_check(data, *fields):
    for f in fields:
        if not data.get(f):
            return False
    return True


def res_wrap(code):
    return {"code": code.value, "data": code.name}


@app.route("/teacher/reg", methods=["POST"])
def teacher_reg():
    data = request.form
    if not data_check(data, "name", "username", "password"):
        return res_wrap(Code.FIELD_INCOMPLETE)

    try:
        with conn.execute(
            "INSERT INTO teacher (name, username, password) VALUES (%s, %s, %s)",
            (data["name"], data["username"], data["password"]),
        ):
            conn.commit()
    except psycopg.IntegrityError:
        conn.rollback()
        return res_wrap(Code.DUPLICATE)
    except psycopg.Error:
        conn.rollback()
        return res_wrap(Code.INTERNAL)
    except Exception:
        return res_wrap(Code.INTERNAL)

    return res_wrap(Code.OK)


@app.route("/student/reg", methods=["POST"])
def student_reg():
    data = request.form
    if not data_check(data, "name", "username", "password", "semester"):
        return res_wrap(Code.FIELD_INCOMPLETE)

    try:
        with conn.execute(
            "INSERT INTO student (name, username, password, semester) VALUES (%s, %s, %s, %s)",
            (data["name"], data["username"], data["password"], int(data["semester"])),
        ):
            conn.commit()
    except psycopg.IntegrityError:
        conn.rollback()
        return res_wrap(Code.DUPLICATE)
    except psycopg.Error:
        conn.rollback()
        return res_wrap(Code.INTERNAL)
    except Exception:
        return res_wrap(Code.INTERNAL)

    return res_wrap(Code.OK)


if __name__ == "__main__":
    app.run()
