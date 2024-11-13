
from typing import Tuple
from flask import Blueprint, Response, make_response, render_template, jsonify
from moonphaserequester.moonphaserequester import AUTH_STRING

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def webapp() -> str:
    return render_template("index.html")


@views.route("/update", methods=["POST"])
def update() -> Tuple[Response, int]:
    auth = AUTH_STRING.encode().hex()
    resp = make_response(jsonify({"authKey": auth}))
    resp.headers["Request"] = "Value"
    return resp, 200
