import models

import os
import sys
import secrets


from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint("users", "user", url_prefix="/user")

# register route
@user.route("/register", methods=["POST"])
def register_user():
    print(request, '<--request')

    payload = request.get_json()
    print(payload, '<--payload')
    payload["email"].lower()
    try:
        models.User.get(models.User.email == payload["email"])

        return jsonify(
            data={},
            status={"code": 401, "message": "A user with that email already exists!"}
        )
    except models.DoesNotExist:

        payload["password"] = generate_password_hash(payload["password"])
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)
        del user_dict["password"]
        return jsonify(data=user_dict, status={"code": 200, "message": "Success"})


@user.route("/login", methods=["GET", "POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.username == payload["username"])
        user_dict = model_to_dict(user)
        if check_password_hash(user_dict["password"], payload["password"]):
            del user_dict["password"]
            login_user(user)
            print(user_dict["username"], '<-- current user here')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect!"},)
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={"code": 401, "message": "Username or password is incorrect!"}
        )


@user.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify(
        data={},
        status={"code": 200, "message": "Success logging out"}
    )
