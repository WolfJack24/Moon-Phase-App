# pylint: disable=missing-module-docstring, missing-class-docstring

from typing import Any, Dict, Tuple


class Constants():
    # Image related vars
    IMAGE_PATH: str = "images"
    IMAGE_SIZES: list[Tuple[int, int]] = [(200, 260), (260, 160)]

    # Format
    DEFAULT_FORMAT: str = "png"

    # Style
    DEFAULT_MOONSTYLE: str = "default"
    DEFAULT_BACKGROUND_STYLE: str = "stars"
    DEFAULT_BACKGROUND_COLOR: str = "black"
    DEFAULT_HEADING_COLOR: str = "white"
    DEFAULT_TEXT_COLOR: str = "white"

    # Observer
    DEFAULT_LATITUDE: float = 6.56774
    DEFAULT_LONGITUDE: float = 79.88956
    DEFAULT_DATE: str = "2024-07-18"

    # View
    DEFAULT_TYPE: str = "portrait-simple"
    DEFAULT_ORIENTATION: str = "south-up"

    DEFAULTS: Dict[str, Any] = {
        "format_type": DEFAULT_FORMAT,
        "moon_style": DEFAULT_MOONSTYLE,
        "background_style": DEFAULT_BACKGROUND_STYLE,
        "background_color": DEFAULT_BACKGROUND_COLOR,
        "heading_color": DEFAULT_HEADING_COLOR,
        "text_color": DEFAULT_TEXT_COLOR,
        "latitude": DEFAULT_LATITUDE,
        "longitude": DEFAULT_LONGITUDE,
        "date": DEFAULT_DATE,
        "view_type": DEFAULT_TYPE,
        "orientation": DEFAULT_ORIENTATION
    }

    # Shared Info
    date: str | None = None
    format_type: str | None = None
    view_type: str = DEFAULT_TYPE


class Info():
    format_type: str
    moon_style: str
    background_style: str
    background_color: str
    heading_color: str
    text_color: str
    latitude: float
    longitude: float
    date: str
    view_type: str
    orientation: str
