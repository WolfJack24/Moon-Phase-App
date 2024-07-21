# pylint: disable=missing-module-docstring, missing-function-docstring, global-statement
from http.client import HTTPSConnection, HTTPResponse
import json
from typing import Final, Tuple, Dict, Any
from os import getenv, path, mkdir
import base64
from requests import get as requestsget, Response, ConnectionError as RequestsConnectionError
from dotenv import load_dotenv

load_dotenv()
APP_ID: Final[str | None] = getenv("APP_ID")
APP_SECRET: Final[str | None] = getenv("APP_SECRET")

USER_PASS: str = f"{APP_ID}:{APP_SECRET}"
AUTH_STRING: str = base64.b64encode(USER_PASS.encode()).decode()

CONN: HTTPSConnection = HTTPSConnection(
    "api.astronomyapi.com")

payload: Dict[str, Any] | None = None


def payload_config(
    date: str | None,
    moon_style: str | None,
    orientation: str | None
) -> Dict[str, Any]:
    if date is None:
        date = "2024-07-18"

    if moon_style is None:
        moon_style = "default"

    if orientation is None:
        orientation = "south-up"

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


def update_payload(date: str, style: str, orientation: str) -> None:
    global payload
    payload = payload_config(date, style, orientation)


def get_image() -> Tuple[str, str]:
    if payload is None:
        payload_json = json.dumps(payload_config(
            "2024-07-18", "default", "south-up"))
    else:
        payload_json = json.dumps(payload)

    parsed_data = json.loads(payload_json)
    encoded_payload = payload_json.encode()

    headers: Dict[str, str] = {'Authorization': f"Basic {AUTH_STRING}"}

    CONN.request(method="POST", url="/api/v2/studio/moon-phase",
                 body=encoded_payload, headers=headers)

    response: HTTPResponse = CONN.getresponse()
    data: str = response.read().decode("utf-8")
    date_request: str = parsed_data["observer"]["date"]

    return date_request, data


def download_image(url: str, filename: str) -> None:
    img_dir: str = "images"

    try:
        response: Response = requestsget(url, timeout=10)
        print("Connection Successful!")
    except RequestsConnectionError:
        print("User is NOT connected to the internet!")

    if not path.exists(img_dir):
        mkdir(img_dir)

    with open(f"{img_dir}/{filename}", "wb") as picture:
        picture.write(response.content)
