# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
__version__ = "2.0.1"

import subprocess
from os import path
from sys import argv
import gui
import moonphaserequester
import constants
from gui import App
from website import create_webapp


def app_run() -> None:
    print(f"App ver: {__version__}")
    print(f"GUI ver: {gui.__version__}")
    print(f"ImageGen ver: {moonphaserequester.__version__}")
    print(f"Constants ver: {constants.__version__}")

    app = App()
    app.iconbitmap("assets/icons/icon.ico")
    app.mainloop()

    if path.exists("images"):
        subprocess.run(["rm", "-rf", "images"], check=True)
        print("The image folder was deleted.")
    else:
        print("The image folder was not created.")


def server_run() -> None:
    webapp = create_webapp()
    webapp.run()


def main() -> None:
    if len(argv) == 2:
        match argv[1]:
            case "server":
                server_run()
            case _:
                print(
                    "Usage: main.py\n"
                    "    server: open the server version")
    else:
        app_run()


if __name__ == "__main__":
    main()
