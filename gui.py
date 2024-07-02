# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os
import json
import customtkinter as ctk
from PIL import Image
from imagegen import get_image, download_image


DATE = get_image()


def get_and_download_image() -> None:
    try:
        if os.path.exists("info/data.json"):
            with open("info/data.json", "r", encoding="utf-8") as json_file:
                image_data: str = json.load(json_file)
    except FileNotFoundError:
        print("payload.json doe's not exist")
    except json.JSONDecodeError:
        print("Could not decode file: payload.json")

    image_json = json.dumps(image_data)
    parsed_data = json.loads(image_json)
    download_image(parsed_data["data"]["imageUrl"], f"{DATE}.jpg")


class InfoPanel(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("200x400")
        self.title("Info Dialog")
        self.resizable(False, False)

        self.date_input = ctk.CTkEntry(
            self, placeholder_text="Date: YYYY-MM-DD")
        self.date_input.pack(padx=20, pady=10)


class App(ctk.CTk):
    def __init__(self, size: str, title: str):
        super().__init__()

        def load_image():
            image_path = f"images/{DATE}.jpg"
            if os.path.exists(image_path):
                self.image_label.configure(image=ctk.CTkImage(
                    Image.open(image_path), Image.open(image_path), (200, 260)))

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
        self.grid = [0, 1, 2, 3, 4, 5]
        for i in self.grid:
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.image_label = ctk.CTkLabel(
            self, width=200, height=260, text="AHHHHHHHH")
        self.image_label.grid(column=3, row=0, columnspan=3, rowspan=4)

        self.info_dialog = ctk.CTkButton(
            self, text="Set Info", command=open_toplevel)
        self.info_dialog.grid(column=0, row=3, padx=5, pady=5)

        self.load_button = ctk.CTkButton(
            self, text="Load Image", command=load_image)
        self.load_button.grid(column=0, row=4, padx=5, pady=5)

        self.gen_button = ctk.CTkButton(
            self, text="Gen Image", command=get_and_download_image)
        self.gen_button.grid(column=0, row=5, padx=5, pady=5)
