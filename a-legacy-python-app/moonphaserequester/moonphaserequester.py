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

S = str | None
F = float | None

load_dotenv()
APP_ID: Final[S] = getenv("APP_ID")
APP_SECRET: Final[S] = getenv("APP_SECRET")

USER_PASS: str = f"{APP_ID}:{APP_SECRET}"
AUTH_STRING: str = base64.b64encode(USER_PASS.encode()).decode()

CONN: HTTPSConnection = HTTPSConnection(
    "api.astronomyapi.com")


def create_payload(**kwargs):
    return {
        "format": kwargs.get("format_type"),
        "style": {"moonStyle": kwargs.get("moon_style")},
        "backgroundStyle": kwargs.get("background_style"),
        "backgroundColor": kwargs.get("background_color"),
        "headingColor": kwargs.get("heading_color"),
        "textColor": kwargs.get("text_color"),
        "observer": {
            "latitude": kwargs.get("latitude"),
            "longitude": kwargs.get("longitude"),
            "date": kwargs.get("date")
        },
        "view": {
            "type": kwargs.get("view_type"),
            "orientation": kwargs.get("orientation")
        }
    }


class MoonPhaseRequester:
    def __init__(self) -> None:
        self.payload: Dict[str, Any] | None = None
        # Format
        self.format_type: S = None
        # Style
        self.moon_style: S = None
        self.background_style: S = None
        self.background_color: S = None
        self.heading_color: S = None
        self.text_color: S = None
        # Observer
        self.latitude: F = None
        self.longitude: F = None
        # View
        self.view_type: S = None
        self.orientation: S = None

    def get_moon_info(self) -> Tuple[str, str, str]:
        if self.format_type is None:
            self.format_type = con.DEFAULT_FORMAT
        if self.moon_style is None:
            self.moon_style = con.DEFAULT_MOONSTYLE
        if self.orientation is None:
            self.orientation = con.DEFAULT_ORIENTATION
        return self.format_type, self.moon_style, self.orientation

    # TODO: use Byte Array! Gonna be honest **kwargs confuses me :pain:
    def update_payload(self, **kwargs) -> None:
        self.format_type = (kwargs.get("format_type")
                            if kwargs.get("format_type") != "svg"
                            else "png")
        self.moon_style = kwargs.get("moon_style")
        self.background_style = kwargs.get("background_style")
        self.background_color = kwargs.get("background_color")
        self.heading_color = kwargs.get("heading_color")
        self.text_color = kwargs.get("text_color")
        self.latitude = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")
        self.view_type = kwargs.get("view_type")
        self.orientation = kwargs.get("orientation")

        self.payload = self.payload_config(
            kwargs.get("format_type"),
            kwargs.get("moon_style"),
            kwargs.get("background_style"),
            kwargs.get("background_color"),
            kwargs.get("heading_color"),
            kwargs.get("text_color"),
            kwargs.get("latitude"),
            kwargs.get("longitude"),
            kwargs.get("date"),
            kwargs.get("view_type"),
            kwargs.get("orientation")
        )

    def payload_config(
        self,
        format_type: S,
        moon_style: S,
        background_style: S,
        background_color: S,
        heading_color: S,
        text_color: S,
        latitude: F,
        longitude: F,
        date: S,
        view_type: S,
        orientation: S
    ) -> Dict[str, Any]:
        format_type = (con.DEFAULT_FORMAT
                       if format_type is None or format_type == "svg"
                       else format_type)
        moon_style = con.DEFAULT_MOONSTYLE if moon_style is None else moon_style
        background_style = (con.DEFAULT_BACKGROUND_STYLE
                            if background_style is None
                            else background_style)
        background_color = (con.DEFAULT_BACKGROUND_COLOR
                            if background_color == ""
                            else background_color)
        heading_color = con.DEFAULT_HEADING_COLOR if heading_color == "" else heading_color
        text_color = con.DEFAULT_TEXT_COLOR if text_color == "" else text_color
        latitude = con.DEFAULT_LATITUDE if latitude == "" else latitude
        longitude = con.DEFAULT_LONGITUDE if longitude == "" else longitude
        date = con.DEFAULT_DATE if date == "" else date
        view_type = con.DEFAULT_TYPE if view_type is None else view_type
        orientation = con.DEFAULT_ORIENTATION if orientation is None else orientation

        payload: dict[str, Any] = {
            "format": format_type,
            "style": {
                "moonStyle": moon_style,
                "backgroundStyle": background_style,
                "backgroundColor": background_color,
                "headingColor": heading_color,
                "textColor": text_color
            },
            "observer": {
                "latitude": latitude,
                "longitude": longitude,
                "date": date
            },
            "view": {
                "type": view_type,
                "orientation": orientation
            }
        }

        return payload

    def get_image_data(self) -> Tuple[str, str]:
        if self.payload is None:
            payload_json: str = json.dumps(self.payload_config(**con.DEFAULTS))
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
