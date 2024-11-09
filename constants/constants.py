# pylint: disable=missing-module-docstring, missing-class-docstring

from typing import Tuple

type T = Tuple[str, str, str, str, str, str, float, float, str, str, str]


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

    DEFAULTS: T = (
        DEFAULT_FORMAT,
        DEFAULT_MOONSTYLE,
        DEFAULT_BACKGROUND_STYLE,
        DEFAULT_BACKGROUND_COLOR,
        DEFAULT_HEADING_COLOR,
        DEFAULT_TEXT_COLOR,
        DEFAULT_LATITUDE,
        DEFAULT_LONGITUDE,
        DEFAULT_DATE,
        DEFAULT_TYPE,
        DEFAULT_ORIENTATION
    )

    # Shared Info
    date: str | None = None
    format_type: str | None = None
    view_type: str = DEFAULT_TYPE
