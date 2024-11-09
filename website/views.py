from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def webapp() -> str:
    return render_template("index.html")
