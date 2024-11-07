# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
__version__ = "2.0.1"

import subprocess
from os import path
from sys import argv
import gui
import moonphaserequester
import constants
from gui import App


def app_run() -> None:
    print(f"App ver: {__version__}")
    print(f"GUI ver: {gui.__version__}")
    print(f"ImageGen ver: {moonphaserequester.__version__}")
    print(f"Constants ver: {constants.__version__}")

    app = App()
    app.mainloop()

    if path.exists("images"):
        subprocess.run(["rm", "-rf", "images"], check=True)
        print("Images was was deleted.")
    else:
        print("Images was not created.")


def server_run() -> None:
    print("Not implemented yet, WIP!")


def main():
    if len(argv) == 2:
        match argv[1]:
            case "server":
                server_run()
            case _:
                print(
                    "Usage: main.py\n\t"
                    "server: open the server version")
    else:
        app_run()


if __name__ == "__main__":
    main()
