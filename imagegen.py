# pylint: disable=missing-module-docstring, missing-function-docstring
from http.client import HTTPSConnection, HTTPResponse
import json
from typing import Final
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

# info\payload.json


def get_image() -> str:
    try:
        with open("info/payload.json", "r", encoding="utf-8") as json_file:
            json_data: str = json.load(json_file)
    except FileNotFoundError:
        print("payload.json doe's not exist")
    except json.JSONDecodeError:
        print("Could not decode file: payload.json")

    payload_json = json.dumps(json_data)
    parsed_data = json.loads(payload_json)
    encoded_payload = payload_json.encode()

    headers: dict = {'Authorization': f"Basic {AUTH_STRING}"}

    CONN.request(method="POST", url="/api/v2/studio/moon-phase",
                 body=encoded_payload, headers=headers)

    response: HTTPResponse = CONN.getresponse()
    data: str = response.read().decode("utf-8")
    date_request: str = parsed_data["observer"]["date"]

    with open("info/data.json", "w", encoding="utf-8") as file:
        file.write(data)

    return date_request


def download_image(url: str, filename: str) -> None:
    img_dir: str = "images"
    response: Response = requestsget(url, timeout=3)
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    with open(f"{img_dir}/{filename}", "wb") as file:
        file.write(response.content)
