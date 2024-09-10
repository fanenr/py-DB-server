from ext import jwt
from flask import Flask
from flask_cors import CORS
from datetime import timedelta


def app_init():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "arthur"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

    CORS(app)
    jwt.init_app(app)

    from teacher import bp as teacher
    from student import bp as student

    app.register_blueprint(teacher)
    app.register_blueprint(student)

    return app


if __name__ == "__main__":
    app = app_init()
    app.run()
