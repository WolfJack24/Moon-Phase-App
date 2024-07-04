# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os
import json
import customtkinter as ctk
from PIL import Image
from imagegen import get_image, download_image


DATE, FILE_DATA = get_image()


def get_and_download_image() -> None:
    image_json = json.dumps(FILE_DATA)
    parsed_data = json.loads(image_json)

    if isinstance(parsed_data, str):
        parsed_data = json.loads(parsed_data)
        download_image(parsed_data["data"]["imageUrl"], f"{DATE}.jpg")
    else:
        print("the data was not a dict")


class InfoPanel(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("200x180")
        self.title("Info Dialog")
        self.resizable(False, False)

        self.date = ctk.CTkEntry(
            self, placeholder_text="Date: YYYY-MM-DD")
        self.date.place(x=30, y=22)

        self.style = ctk.CTkComboBox(
            self, corner_radius=5,
            values=["Default", "Sketch", "Shaded"])
        self.style.set("Default")
        self.style.place(x=30, y=58)

        self.orientation = ctk.CTkComboBox(
            self, corner_radius=5, values=["North Up", "South Up"])
        self.orientation.set("South Up")
        self.orientation.place(x=30, y=94)

        self.update = ctk.CTkButton(self, text="Update")
        self.update.place(x=30, y=130)


class App(ctk.CTk):
    def __init__(self, size: str, title: str):
        super().__init__()

        def load_image():
            image_path = f"images/{DATE}.jpg"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                self.image.configure(image=ctk.CTkImage(
                    image, image, (200, 260)))
                image.close()

        def open_toplevel():
            if self.window_dialog is None or not self.window_dialog.winfo_exists():
                self.window_dialog = InfoPanel()
            else:
                self.window_dialog.focus()

        self.window_dialog = None
        self.geometry(size)
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        self.title(title)
        self.resizable(False, False)

        self.image_frame = ctk.CTkFrame(
            self, width=221, height=277, corner_radius=5, fg_color="#303030")
        self.image_frame.place(x=30, y=60)

        self.image = ctk.CTkLabel(
            self.image_frame, width=200, height=260, text="")
        self.image.place(x=10, y=8)

        self.info_dialog = ctk.CTkButton(
            self, text="Set Info", command=open_toplevel)
        self.info_dialog.place(x=330, y=230)

        self.load_button = ctk.CTkButton(
            self, text="Load Image", command=load_image)
        self.load_button.place(x=330, y=265)

        self.gen_button = ctk.CTkButton(
            self, text="Gen Image", command=get_and_download_image)
        self.gen_button.place(x=330, y=300)
