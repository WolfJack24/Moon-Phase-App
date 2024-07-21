# Moon-Phase-App

A "simple" app to request a specific moon phase by date and other parameters to show how it looks

> Warning: This is not close to finished!

## Get-Started

First off get yourself a API key for free at: [Astronomy API](https://docs.astronomyapi.com/)

When you get your `APP_ID` and `APP_SECRET`, make a `.env` file that looks like this:

```properties
APP_ID=key # add app id
APP_SECRET=key # and add the app secret
```

```PowerShell
python -m venv .venv # Create the venv in the folder of choice
python -m pip install -r requirements.txt # Install the needed librarys
py .\main.py # run the app
```

### Design

The layout of this project is a Figma file:
[Moon Phase App Layout](https://www.figma.com/design/45IkxmpJ02QLcfx7dg3Ve6/Moon-Phase-App?node-id=0-1&t=NAOEOGGjnye4eSVL-1)

## TODO

- [ ] Make some functions Asynchronous to stop the app from freezing when the `Gen Button` is clicked
- [ ] Add fully working notifications
