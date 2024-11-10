from typing import Tuple
from flask import Blueprint, render_template, request, jsonify, Response, flash
import json
from constants import Info

views = Blueprint("views", __name__)

info = Info()


@views.route("/", methods=["GET", "POST"])
def webapp() -> str:
    return render_template("index.html")


@views.route("/update", methods=["POST"])
def update() -> Tuple[Response, int]:
    request_data = json.loads(request.data)
    if request_data:
        info.format_type = request_data["format"]
        info.moon_style = request_data["moonStyle"]
        info.background_style = request_data["backgroundStyle"]
        info.background_color = request_data["backgroundColor"]
        info.heading_color = request_data["headingColor"]
        info.text_color = request_data["textColor"]
        info.latitude = request_data["latitude"]
        info.longitude = request_data["longitude"]
        info.date = request_data["date"]
        info.view_type = request_data["viewType"]
        info.orientation = request_data["orientation"]
        flash("Info Updated", "info")
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404
