# pylint: disable=missing-module-docstring, missing-function-docstring, global-statement, missing-class-docstring
from http.client import HTTPSConnection, HTTPResponse
import json
from typing import Final, Tuple, Dict, Any
from os import getenv, path, mkdir
import base64
from requests import get as requestsget, Response, ConnectionError as RequestsConnectionError
from dotenv import load_dotenv
from constants import Constants

con = Constants()

load_dotenv()
APP_ID: Final[str | None] = getenv("APP_ID")
APP_SECRET: Final[str | None] = getenv("APP_SECRET")

USER_PASS: str = f"{APP_ID}:{APP_SECRET}"
AUTH_STRING: str = base64.b64encode(USER_PASS.encode()).decode()

CONN: HTTPSConnection = HTTPSConnection(
    "api.astronomyapi.com")


class MoonPhaseRequester:
    def __init__(self) -> None:
        self.payload: Dict[str, Any] | None = None
        self.style: str | None = None
        self.orientation: str | None = None

    def get_moon(self) -> Tuple[str, str]:
        if self.style is None:
            self.style = con.DEFAULT_STYLE
        if self.orientation is None:
            self.orientation = con.DEFAULT_ORIENTATION
        return self.style, self.orientation

    def update_payload(self, date: str, style: str, orientation: str) -> None:
        self.style = style
        self.orientation = orientation
        self.payload = self.payload_config(date, style, orientation)

    def payload_config(
        self,
        date: str | None,
        moon_style: str | None,
        orientation: str | None
    ) -> Dict[str, Any]:
        if date is None:
            date = con.DEFAULT_DATE

        if moon_style is None:
            moon_style = con.DEFAULT_STYLE

        if orientation is None:
            orientation = con.DEFAULT_ORIENTATION

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

    def get_image(self) -> Tuple[str, str]:
        if self.payload is None:
            payload_json: str = json.dumps(self.payload_config(
                "2024-07-18", "default", "south-up"))
        else:
            payload_json: str = json.dumps(self.payload)

        parsed_data: Any = json.loads(payload_json)
        encoded_payload: bytes = payload_json.encode()

        headers: Dict[str, str] = {'Authorization': f"Basic {AUTH_STRING}"}

        CONN.request(method="POST", url="/api/v2/studio/moon-phase",
                     body=encoded_payload, headers=headers)

        response: HTTPResponse = CONN.getresponse()
        data: str = response.read().decode("utf-8")
        date_request: str = parsed_data["observer"]["date"]

        return date_request, data

    def download_image(self, url: str, filename: str) -> None:
        try:
            response: Response = requestsget(url, timeout=10)
            print("Connection Successful!")
        except RequestsConnectionError:
            print("User is NOT connected to the internet!")

        if not path.exists(con.IMAGE_PATH):
            mkdir(con.IMAGE_PATH)

        with open(f"{con.IMAGE_PATH}/{filename}", "wb") as picture:
            picture.write(response.content)
