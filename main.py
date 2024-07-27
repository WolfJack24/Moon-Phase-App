# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
import subprocess
from os import path
from sys import argv
from gui.gui import App


def app_run() -> None:
    app = App(size="500x400", title="Moon Phase App")
    app.mainloop()

    if path.exists("images"):
        subprocess.run(["rm", "-rf", "images"], check=True)
        print("Images was was deleted.")
    else:
        print("Images was not created.")


def server_run() -> None:
    print("WIP!")


def main():
    if len(argv) >= 2:
        match argv[1]:
            case "app":
                app_run()
            case "server":
                server_run()
            case _:
                print(
                    "Usage: main.py\n\t"
                    "app: open the app verison\n\t"
                    "server: open the server version")
    else:
        print(
            "Usage: main.py\n"
            "    app: open the app verison\n"
            "    server: open the server version")


if __name__ == "__main__":
    main()
