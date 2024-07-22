# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
import subprocess
from os import path
from gui import App


def main():
    app = App(size="500x400", title="Moon Phase App")
    app.mainloop()

    if path.exists("images"):
        subprocess.run(["rm", "-rf", "images"], check=True)
        print("Images was was deleted.")
    else:
        print("Images was not created.")


if __name__ == "__main__":
    main()
