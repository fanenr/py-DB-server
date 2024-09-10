import util, psycopg

from ext import pwd, conn
from flask import request
from flask import Blueprint

from psycopg.rows import dict_row
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token


bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/reg", methods=["POST"])
def student_reg():
    data = request.form
    if not util.check(data, "name", "start", "username", "password"):
        return util.badreq("The parameters are incomplete")

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
    except psycopg.IntegrityError:
        return util.conflict("The user already exists")
    except Exception:
        return util.internal("Internal error")

    cur.close()
    return "ok"


@bp.route("/log", methods=["POST"])
def student_log():
    data = request.form
    if not util.check(data, "username", "password"):
        return util.badreq("The parameters are incomplete")

    try:
        sql = "SELECT * FROM student WHERE username = %s"
        value = (data["username"],)
        with conn.transaction():
            cur = conn.cursor(row_factory=dict_row)
            cur.execute(sql, value)
    except Exception:
        return util.internal("Internal error")

    if not (info := cur.fetchone()):
        return util.unauth("The user does not exist")
    if not pwd.verify(data["password"], info["password"]):
        return util.unauth("Wrong username or password")

    del info["username"]
    del info["password"]

    access_token = create_access_token(info["id"])
    info["access_token"] = access_token

    cur.close()
    return info


@bp.route("/test")
@jwt_required()
def test():
    id = get_jwt_identity()
    return {"id": id}
