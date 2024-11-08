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
    filedialog
)
from PIL import Image, ImageFile
from moonphaserequester import MoonPhaseRequester
from constants import Constants

requester = MoonPhaseRequester()
con = Constants()

VALUES: list[str] = ["None"]


def load_image(gen_op: bool, image_base: Optional[list[str]], recent_cmb: CTkComboBox, moon_image: CTkLabel, _string: Optional[str]) -> None:
    if not gen_op:
        images: str = recent_cmb.get()

        if path.exists(con.IMAGE_PATH):
            image: ImageFile.ImageFile = Image.open(
                str(f"{getcwd()}/{con.IMAGE_PATH}/{images}.jpg"))
            moon_image.configure(image=CTkImage(
                image, image, (200, 260)))
            image.close()
    else:
        if not image_base is None:
            if path.exists(con.IMAGE_PATH):
                if not len(image_base) == 3:
                    print("the var image_base has more than 3 items")
                image: ImageFile.ImageFile = Image.open(
                    str(f"{getcwd()}/{con.IMAGE_PATH}/{image_base[0]}_{image_base[1]}_{image_base[2]}.jpg"))
                moon_image.configure(image=CTkImage(
                    image, image, (200, 260)))
                image.close()


def get_and_download_image(recent_cmb: CTkComboBox, moon_image: CTkLabel) -> None:
    con.DATE, file_data = requester.get_image_data()
    image_json: str = json.dumps(file_data)
    parsed_data: Any = json.loads(image_json)
    style, orientation = requester.get_moon_info()
    jpg_name: str = f"{con.DATE}_{style}_{orientation}"

    if isinstance(parsed_data, str):
        parsed_data = json.loads(parsed_data)
        requester.download_image(
            parsed_data["data"]["imageUrl"], f"{jpg_name}.jpg")
        print(
            f"The image {jpg_name}.jpg was downloaded!"
        )
        if "None" in VALUES:
            VALUES.pop(0)
        VALUES.append(f"{jpg_name}")
        recent_cmb.configure(values=VALUES)
        recent_cmb.set(jpg_name)
        load_image(True, [con.DATE, style, orientation],
                   recent_cmb, moon_image, None)
    else:
        print("The image data was not a dictionary")


def download_thread(cmb: CTkComboBox, moon_image: CTkLabel) -> None:
    gdit = Thread(target=get_and_download_image, args=(cmb, moon_image),
                  name="get_and_download_image")
    gdit.start()


# class DepPanel(CTkToplevel):
#     def __init__(self):
#         super().__init__()

#         # TODO


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
    height = 351
    app_title = "Moon Phase App"

    def __init__(self):
        super().__init__()

        def load_image_from_filedialog() -> None:
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
                print("No moon_image's were generated!")

        def open_infopanel() -> None:
            if self.window_dialog is None or not self.window_dialog.winfo_exists():
                self.window_dialog = InfoPanel()
            else:
                self.window_dialog.focus()

        self.window_dialog = None
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
            load_image, False, None, self.recent, self.moon_image)
        self.recent.configure(
            width=153, height=24, values=VALUES, command=partial_load_image,
            button_color="#1F6AA5"
        )
        self.recent.set("None")
        self.recent.place(x=17, y=28)

        self.info_dialog = CTkButton(
            self, text="Set Info", command=open_infopanel)
        self.info_dialog.place(x=330, y=222)  # (x=330, y=187)

        # self.load_button = CTkButton(
        #     self, text="Load Image", command=load_image_from_filedialog)
        # self.load_button.place(x=330, y=222)

        partial_download_thread = partial(
            download_thread, self.recent, self.moon_image)
        self.gen_button = CTkButton(
            self, text="Gen Image", command=partial_download_thread)
        self.gen_button.place(x=330, y=257)
