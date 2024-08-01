# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, global-statement
from os import path, getcwd
import json
from functools import partial
from typing import Any
from customtkinter import (
    CTk,
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkImage,
    CTkToplevel,
    CTkEntry,
    CTkComboBox,
    filedialog
)
from PIL import Image, ImageFile
from imagegen import MoonPhaseRequester
from constants import Constants

requester = MoonPhaseRequester()
con = Constants()


def get_and_download_image() -> None:
    con.DATE, file_data = requester.get_image()
    image_json: str = json.dumps(file_data)
    parsed_data: Any = json.loads(image_json)
    (style, orientation) = requester.get_moon()

    if isinstance(parsed_data, str):
        parsed_data = json.loads(parsed_data)
        requester.download_image(
            parsed_data["data"]["imageUrl"], f"{con.DATE}_{style}_{orientation}.jpg")
        print(
            f"The image {con.DATE}_{style}_{orientation}.jpg was downloaded!"
        )
    else:
        print("The image data was not a dictionary")


class InfoPanel(CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("200x180")
        self.title("Info Dialog")
        self.resizable(False, False)

        self.date = CTkEntry(
            self, placeholder_text="Date: YYYY-MM-DD")
        self.date.place(x=30, y=22)

        self.style = CTkComboBox(
            self, corner_radius=5,
            values=["Default", "Sketch", "Shaded"])
        self.style.set("Default")
        self.style.place(x=30, y=58)

        self.orientation = CTkComboBox(
            self, corner_radius=5, values=["North Up", "South Up"])
        self.orientation.set("South Up")
        self.orientation.place(x=30, y=94)

        self.update_button = CTkButton(
            self, text="Update", command=self.update)
        self.update_button.place(x=30, y=130)

    def update(self) -> None:
        date: str = self.date.get()
        style: str = self.style.get()
        orientation: str = self.orientation.get()

        if date == "":
            date = "2024-07-18"

        if "-" not in date:
            date = date.replace(" ", "-")

        style = style.lower()
        orientation = orientation.lower().replace(" ", "-")

        requester.update_payload(date, style, orientation)


class App(CTk):
    width = 500
    height = 400
    app_title = "Moon Phase App"

    def __init__(self):
        super().__init__()

        def load_image() -> None:
            if path.exists(con.IMAGE_PATH):
                filename = filedialog.askopenfile(
                    defaultextension="jpg",
                    initialdir=f"{getcwd()}/{con.IMAGE_PATH}"
                )
                image: ImageFile.ImageFile = Image.open(
                    str(filename.name))  # type: ignore
                self.image.configure(image=CTkImage(
                    image, image, (200, 260)))
                image.close()
            else:
                print("No Image's were generated!")

        def open_infopanel() -> None:
            if self.window_dialog is None or not self.window_dialog.winfo_exists():
                self.window_dialog = InfoPanel()
            else:
                self.window_dialog.focus()

        self.window_dialog = None
        self.geometry(f"{self.width}x{self.height}")
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        self.title(self.app_title)
        self.resizable(False, False)

        self.notif_frame = CTkFrame(
            self, width=221, height=29, corner_radius=3, fg_color="#303030")
        self.notif_frame.place(x=29, y=29)

        self.notif_text = CTkLabel(
            self.notif_frame, width=72, height=12, text="Notifications Not Working... Yet!")
        self.notif_text.place(x=10, y=7)

        self.image_frame = CTkFrame(
            self, width=221, height=277, corner_radius=5, fg_color="#303030")
        self.image_frame.place(x=29, y=85)

        self.image = CTkLabel(
            self.image_frame, width=200, height=260, text="")
        self.image.place(x=10, y=8)

        self.info_dialog = CTkButton(
            self, text="Set Info", command=open_infopanel)
        self.info_dialog.place(x=330, y=230)

        self.load_button = CTkButton(
            self, text="Load Image", command=load_image)
        self.load_button.place(x=330, y=265)

        self.gen_button = CTkButton(
            self, text="Gen Image", command=get_and_download_image)
        self.gen_button.place(x=330, y=300)
