# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
import subprocess
from gui import App


def main():
    app = App(size="500x400", title="Moon Phase App")
    app.mainloop()

    subprocess.run(["rm", "-rf", "images"], check=True)


if __name__ == "__main__":
    main()
