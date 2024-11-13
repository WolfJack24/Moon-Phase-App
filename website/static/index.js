"use strict";
const genButton = document.getElementById("gen-button");
const updateButton = document.getElementById("update-button");
const imageFrame = document.getElementById("image-frame");
const moonImage = document.getElementById("moon-image");
const recentImages = document.getElementById("recent-cmb");
const format = document.getElementById("format-input");
const moonStyle = document.getElementById("moon-style-input");
const backgroundStyle = document.getElementById("background-style");
const backgroundColor = document.getElementById("background-color-input");
const headingColor = document.getElementById("heading-color-input");
const textColor = document.getElementById("text-color-input");
const latitude = document.getElementById("latitude-input");
const longitude = document.getElementById("longitude-input");
const date = document.getElementById("date-input");
const viewType = document.getElementById("view-type-input");
const moonOrientation = document.getElementById("orientation-input");
const DEFAULT_BACKGROUND_COLOR = "black";
const DEFAULT_HEADING_COLOR = "white";
const DEFAULT_TEXT_COLOR = "white";
const DEFAULT_LATITUDE = 6.56774;
const DEFAULT_LONGITUDE = 79.88956;
const DEFAULT_DATE = "2024-07-18";
const HOST = "https://api.astronomyapi.com/api/v2/studio/moon-phase";
class Data {
    constructor() {
        this.format = "";
        this.moonStyle = "";
        this.backgroundStyle = "";
        this.backgroundColor = "";
        this.backgroundColor = "";
        this.headingColor = "";
        this.textColor = "";
        this.latitude = 0.0;
        this.longitude = 0.0;
        this.date = "";
        this.viewType = "";
        this.moonOrientation = "";
    }
    print_all() {
        for (const item in this) {
            console.log(`${item}: ${this[item]}`);
        }
    }
}
let hexAuthString = "";
let data = new Data();
async function update() {
    await fetch("/update", {
        method: "POST",
    })
        .then(async (res) => {
        let data = await res.json();
        hexAuthString = data.authKey;
    })
        .catch((err) => {
        console.error("Error: ", err);
    });
    data.format = format.options[format.selectedIndex].value;
    data.moonStyle = moonStyle.options[moonStyle.selectedIndex].value;
    data.backgroundStyle =
        backgroundStyle.options[backgroundStyle.selectedIndex].value;
    data.backgroundColor =
        backgroundColor.value != ""
            ? backgroundColor.value
            : DEFAULT_BACKGROUND_COLOR;
    data.headingColor =
        headingColor.value != "" ? headingColor.value : DEFAULT_HEADING_COLOR;
    data.textColor = textColor.value != "" ? textColor.value : DEFAULT_TEXT_COLOR;
    data.latitude =
        latitude.value != "" ? Number(latitude.value) : DEFAULT_LATITUDE;
    data.longitude =
        longitude.value != "" ? Number(longitude.value) : DEFAULT_LONGITUDE;
    data.date = date.value != "" ? date.value : DEFAULT_DATE;
    data.viewType = viewType.options[viewType.selectedIndex].value;
    data.moonOrientation =
        moonOrientation.options[moonOrientation.selectedIndex].value;
}
async function genImage() {
    let payload = {
        format: data.format,
        style: {
            moonStyle: data.moonStyle,
            backgroundStyle: data.backgroundStyle,
            backgroundColor: data.backgroundColor,
            headingColor: data.headingColor,
            textColor: data.textColor,
        },
        observer: {
            latitude: data.latitude,
            longitude: data.longitude,
            date: data.date,
        },
        view: {
            type: data.viewType,
            orientation: data.moonOrientation,
        },
    };
    let expAuthString = hexAuthString.match(/.{1,2}/g);
    let authString = expAuthString.reduce((acc, char) => acc + String.fromCharCode(parseInt(char, 16)), "");
    let headers = { Authorization: `Basic ${authString}` };
    await fetch(HOST, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(payload),
    })
        .then(async (res) => {
        let data = await res.json();
        moonImage.src = data.data.imageUrl;
    })
        .catch((err) => {
        console.error("Error: ", err);
    });
}
updateButton.onclick = update;
genButton.onclick = genImage;
update();
