# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
from gui import App


def main():
    app = App(size="600x400", title="Moon Phase")
    app.mainloop()


if __name__ == "__main__":
    main()
