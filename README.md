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
pip install requirements.txt # Install the needed librarys
py .\main.py # run the app
```
