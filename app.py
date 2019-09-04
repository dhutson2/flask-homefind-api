from flask import Flask, g
from flask_login import LoginManager
from flask_cors import CORS
import models
from api.user import user

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = "lcxzerwkj24@lk24nb234l2!n342lk3bn4234!kn"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userId):
    try:
        return models.User.get(models.user.id == userId)
    except models.DoesNotExist:
        return None


# CORS(user, origins=["http://localhost:3000"], supports_credentials=True)


@app.register_blueprint(user)
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/")
def index():
    return "hi you are on 8000"


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
