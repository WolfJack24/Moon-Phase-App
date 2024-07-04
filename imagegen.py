# pylint: disable=missing-module-docstring, missing-function-docstring
from http.client import HTTPSConnection, HTTPResponse
import json
from typing import Final, Tuple, Dict, Any
import os
import base64
from requests import get as requestsget, Response
from dotenv import load_dotenv

load_dotenv()
APP_ID: Final[str] = os.getenv("APP_ID")
APP_SECRET: Final[str] = os.getenv("APP_SECRET")

USER_PASS: str = f"{APP_ID}:{APP_SECRET}"
AUTH_STRING: str = base64.b64encode(USER_PASS.encode()).decode()

CONN: HTTPSConnection = HTTPSConnection(
    "api.astronomyapi.com")


def payload_config(
    date: str,
    moon_style: str = "default",
    orientation: str = "south-up"
) -> Dict[str, Any]:
    return {
        "format": "png",
        "style": {
            "moonStyle": moon_style,
            "backgroundStyle": "stars",
            "backgroundColor": "black",
            "headingColor": "white",
            "textColor": "white"
        },
        "observer": {
            "latitude": 6.56774,
            "longitude": 79.88956,
            "date": date
        },
        "view": {
            "type": "portrait-simple",
            "orientation": orientation
        }
    }


def get_image() -> Tuple[Any]:
    payload = payload_config("2024-07-18", "default", "south-up")

    payload_json = json.dumps(payload)
    parsed_data = json.loads(payload_json)
    encoded_payload = payload_json.encode()

    headers: dict = {'Authorization': f"Basic {AUTH_STRING}"}

    CONN.request(method="POST", url="/api/v2/studio/moon-phase",
                 body=encoded_payload, headers=headers)

    response: HTTPResponse = CONN.getresponse()
    data: str = response.read().decode("utf-8")
    date_request: str = parsed_data["observer"]["date"]

    return date_request, data


def download_image(url: str, filename: str) -> None:
    img_dir: str = "images"
    response: Response = requestsget(url, timeout=3)
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    with open(f"{img_dir}/{filename}", "wb") as file:
        file.write(response.content)
