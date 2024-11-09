# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, global-statement
from os import path, getcwd
import json
from typing import Any, Optional
from threading import Thread
from functools import partial
from customtkinter import (
    CTk,
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkImage,
    CTkToplevel,
    CTkEntry,
    CTkComboBox,
    CTkSwitch,
    StringVar,
    filedialog
)
from PIL import Image, ImageFile
from moonphaserequester import MoonPhaseRequester
from constants import Constants

requester = MoonPhaseRequester()
con = Constants()

VALUES: list[str] = ["None"]


def load_image(
    gen_op: bool,
    image_base: Optional[list[str]],
    format: str | None,
    recent_cmb: CTkComboBox,
    moon_image: CTkLabel,
    _string: Optional[str]
) -> None:

    # New size 260x160
    if format is not None:
        if not gen_op:
            images: str = recent_cmb.get()

            if path.exists(con.IMAGE_PATH):
                image: ImageFile.ImageFile = Image.open(
                    str(f"{getcwd()}/{con.IMAGE_PATH}/{images}.{format}"))
                moon_image.configure(image=CTkImage(
                    image, image, (200, 260)))
                image.close()
        else:
            if not image_base is None:
                if path.exists(con.IMAGE_PATH):
                    if not len(image_base) == 3:
                        print("the var image_base has more than 3 items")
                    image: ImageFile.ImageFile = Image.open(
                        str(f"{getcwd()}/{con.IMAGE_PATH}/{image_base[0]}_{image_base[1]}_{image_base[2]}.{format}"))
                    moon_image.configure(image=CTkImage(
                        image, image, (200, 260)))
                    image.close()


def get_and_download_image(recent_cmb: CTkComboBox, moon_image: CTkLabel) -> None:
    con.date, file_data = requester.get_image_data()
    image_json: str = json.dumps(file_data)
    parsed_data: Any = json.loads(image_json)
    con.format, style, orientation = requester.get_moon_info()
    image_name: str = f"{con.date}_{style}_{orientation}"

    if isinstance(parsed_data, str):
        parsed_data = json.loads(parsed_data)
        if "statusCode" in parsed_data:
            print(json.dumps(parsed_data, indent=4))
        elif "data" in parsed_data:
            requester.download_image(
                parsed_data["data"]["imageUrl"], f"{image_name}.{con.format}")
            print(
                f"The image {image_name}.{con.format} was downloaded!"
            )
        else:
            print("There was neither a error or data when downloading the image")

        if "None" in VALUES:
            VALUES.pop(0)
        if not image_name in VALUES:
            VALUES.append(f"{image_name}")
        recent_cmb.configure(values=VALUES)
        recent_cmb.set(image_name)
        load_image(True, [con.date, style, orientation],
                   con.format, recent_cmb, moon_image, None)
    else:
        print("The image data was not a dictionary")


def download_thread(cmb: CTkComboBox, moon_image: CTkLabel) -> None:
    gdit = Thread(target=get_and_download_image, args=(cmb, moon_image),
                  name="get_and_download_image")
    gdit.start()


class DepPanel(CTkToplevel):
    def __init__(self, dep_items: dict[str, Any], moving_items: dict[str, Any]):
        super().__init__()

        self.load_filedialog_var = StringVar(value="off")
        self._dep_items = dep_items
        self._moving_items = moving_items

        self.geometry("200x125")
        self.title("Dep Items")
        self.resizable(False, False)

        def load_dep_item(item: str, dep_item: str, item_to_be_moved: Optional[str]) -> None:
            deprecated_item = self._dep_items[dep_item]
            moving_item = self._moving_items[item_to_be_moved if item_to_be_moved is not None else "None"]

            match item:
                case "Load_Button":
                    if self.load_filedialog_var.get() == "on":
                        deprecated_item.configure(state="normal")
                        moving_item.place(x=330, y=216)
                    else:
                        deprecated_item.configure(state="hidden")
                        moving_item.place(x=330, y=251)

        partial_load_dep_item = partial(
            load_dep_item, "Load_Button", "load_button", "info_dialog")
        self.load_filedialog = CTkSwitch(
            self, width=22, height=12, text="Load from filedialog",
            onvalue="on", offvalue="off", variable=self.load_filedialog_var, command=partial_load_dep_item
        )
        self.load_filedialog.place(x=11, y=16)


class InfoPanel(CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("340x311")
        self.title("Info Dialog")
        self.resizable(False, False)

        self.format_label = CTkLabel(self, width=46, height=12, text="Format:")
        self.format_label.place(x=22, y=21)

        self.format = CTkComboBox(self, corner_radius=5, values=["PNG", "SVG"])
        self.format.set("PNG")
        self.format.place(x=22, y=38)

        self.style_label = CTkLabel(self, width=34, height=12, text="Style:")
        self.style_label.place(x=22, y=71)

        self.style = CTkComboBox(
            self, corner_radius=5,
            values=["Default", "Sketch", "Shaded"])
        self.style.set("Default")
        self.style.place(x=22, y=88)

        self.background_style = CTkComboBox(
            self, corner_radius=5, values=["Stars", "Solid"])
        self.background_style.set("Stars")
        self.background_style.place(x=22, y=121)

        self.background_color = CTkEntry(
            self, corner_radius=5, placeholder_text="Background Color")
        self.background_color.place(x=22, y=154)

        self.heading_color = CTkEntry(
            self, corner_radius=5, placeholder_text="Heading Color")
        self.heading_color.place(x=22, y=187)

        self.text_color = CTkEntry(
            self, corner_radius=5, placeholder_text="Text Color")
        self.text_color.place(x=22, y=220)

        self.observer_label = CTkLabel(
            self, width=60, height=12, text="Observer:")
        self.observer_label.place(x=179, y=21)

        self.latitude = CTkEntry(
            self, corner_radius=5, placeholder_text="Latitude")
        self.latitude.place(x=179, y=38)

        self.longitude = CTkEntry(
            self, corner_radius=5, placeholder_text="Longitude")
        self.longitude.place(x=179, y=71)

        self.date = CTkEntry(
            self, placeholder_text="Date: YYYY-MM-DD")
        self.date.place(x=179, y=104)

        self.view_label = CTkLabel(self, width=37, height=12, text="View:")
        self.view_label.place(x=179, y=137)

        self.view_type = CTkComboBox(
            self, corner_radius=5,
            values=["Portrait Simple", "Landscape Simple"])
        self.view_type.set("Portrait Simple")
        self.view_type.place(x=179, y=154)

        self.orientation = CTkComboBox(
            self, corner_radius=5, values=["North Up", "South Up"])
        self.orientation.set("South Up")
        self.orientation.place(x=179, y=187)

        self.update_button = CTkButton(
            self, text="Update", command=self.update)
        self.update_button.place(x=100, y=262)

    def check_date(self, date: str) -> str:
        if date == "":
            date = con.DEFAULT_DATE

        if "-" not in date:
            date = date.replace(" ", "-")

        return date

    def update(self) -> None:
        format: str = self.format.get().lower()
        style: str = self.style.get().lower()
        background_style: str = self.background_style.get().lower()
        background_color: str = self.background_color.get().lower()
        heading_color: str = self.heading_color.get().lower()
        text_color: str = self.text_color.get().lower()
        latitude: float = float(
            self.latitude.get()) if self.latitude.get() != "" else con.DEFAULT_LATITUDE
        longitude: float = float(
            self.longitude.get()) if self.longitude.get() != "" else con.DEFAULT_LONGITUDE
        date: str = self.check_date(self.date.get())
        view_type: str = self.view_type.get().lower().replace(" ", "-")
        orientation: str = self.orientation.get().lower().replace(" ", "-")

        requester.update_payload(
            format,
            style,
            background_style,
            background_color,
            heading_color,
            text_color,
            latitude,
            longitude,
            date,
            view_type,
            orientation
        )


class App(CTk):
    width = 500
    height = 351
    app_title = "Moon Phase App"

    def __init__(self):
        super().__init__()

        requester.update_payload(*con.DEFAULTS)

        def load_image_from_filedialog() -> None:
            # ! Deprecated
            if path.exists(con.IMAGE_PATH):
                filename = filedialog.askopenfile(
                    defaultextension="jpg",
                    initialdir=f"{getcwd()}/{con.IMAGE_PATH}"
                )
                image: ImageFile.ImageFile = Image.open(
                    str(filename.name))  # type: ignore
                self.moon_image.configure(image=CTkImage(
                    image, image, (200, 260)))
                image.close()
            else:
                print("No image's were generated!")

        def open_infopanel() -> None:
            if self.info_panel is None or not self.info_panel.winfo_exists():
                self.info_panel = InfoPanel()
            else:
                self.info_panel.focus()

        def open_deppanel() -> None:
            if self.dep_panel is None or not self.dep_panel.winfo_exists():
                self.dep_panel = DepPanel(dep_items, moving_items)
            else:
                self.dep_panel.focus()

        self.info_panel = None
        self.dep_panel = None
        self.geometry(f"{self.width}x{self.height}")
        self.title(self.app_title)
        self.resizable(False, False)

        self.moon_image_frame = CTkFrame(
            self, width=221, height=277, corner_radius=5, fg_color="#303030")
        self.moon_image_frame.place(x=29, y=37)

        self.moon_image = CTkLabel(
            self.moon_image_frame, width=200, height=260, text="")
        self.moon_image.place(x=10, y=8)

        self.images_frame = CTkFrame(
            self, width=187, height=66, fg_color="#303030")
        self.images_frame.place(x=283, y=37)

        self.recent_label = CTkLabel(
            self.images_frame, width=95, height=16, text="Recent Images")
        self.recent_label.place(x=4, y=5)

        # Please ignore this complicated mess of code, thanks in regard 👍
        self.recent = CTkComboBox(self.images_frame)
        partial_load_image = partial(
            load_image, False, None, con.format, self.recent, self.moon_image)
        self.recent.configure(
            width=153, height=24, values=VALUES, command=partial_load_image,
            button_color="#1F6AA5"
        )
        self.recent.set("None")
        self.recent.place(x=17, y=28)

        # ! Deprecated
        self.load_button = CTkButton(
            self, text="Load Image", command=load_image_from_filedialog, state="hidden")
        self.load_button.place(x=330, y=251)

        self.info_dialog = CTkButton(
            self, text="Set Info", command=open_infopanel)
        self.info_dialog.place(x=330, y=251)  # origanel (x=330, y=216)

        partial_download_thread = partial(
            download_thread, self.recent, self.moon_image)
        self.gen_button = CTkButton(
            self, text="Gen Image", command=partial_download_thread)
        self.gen_button.place(x=330, y=286)

        dep_items: dict[str, Any] = {
            "load_button": self.load_button
        }
        moving_items: dict[str, Any] = {
            "None": None,
            "info_dialog": self.info_dialog
        }
        self.bind_all("<F1>", lambda event: open_deppanel())
