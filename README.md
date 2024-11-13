# Moon-Phase-App

A "simple" app to request a specific moon phase by date and other parameters to show how it looks

![Demo 200x260](assets/images/demo_200x260.png "Demo_200x260")
![Demo 260x160](assets/images/demo_260x160.png "Demo_260x160")

Beware onclose of the app it deletes the folder with the images in it!

> Warning: This is not close to finished!

## Get-Started

First off get yourself a API key for free at: [Astronomy API](https://docs.astronomyapi.com/)

When you get your `APP_ID` and `APP_SECRET`, make a `.env` file that looks like this:

```properties
# add app id
APP_ID=key
# and add the app secret
APP_SECRET=key
```

```PowerShell
# Create the venv in the folder of choice
python -m venv .venv
# Install the needed librarys
python -m pip install -r requirements.txt
# run the app (by defualt)
py .\main.py
# or
# run the server app
py .\main.py server
```

Warning: web version is no where close to done

### Typescript Files

```Powershell
# Install Typescript
npm install
# Run tsc
npx tsc
# or
.\node_modules\.bin\tsc
```

### Design

The layout of this project is a Figma file:
[Moon Phase App Layout](https://www.figma.com/design/45IkxmpJ02QLcfx7dg3Ve6/Moon-Phase-App?node-id=0-1&t=NAOEOGGjnye4eSVL-1)

Deprecated Items can be accessed by presing **F1**

Versions:

- Python ver: 3.13.0
- App ver: 2.0.1
- GUI ver: 3.2.0
- Moon Phase Requester ver: 3.0.0
- Constants ver: 1.3.0
