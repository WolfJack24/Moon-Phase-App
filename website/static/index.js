"use strict";
const genButton = document.getElementById("gen-button");
const downloadButton = document.getElementById("download-button");
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
let imageUrl = "";
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
    let view = viewType.options[viewType.selectedIndex].value;
    switch (view) {
        case "portrait-simple":
            imageFrame.style.position = "absolute";
            imageFrame.style.left = "52px";
            imageFrame.style.top = "36px";
            imageFrame.style.width = "221px";
            imageFrame.style.height = "277px";
            moonImage.style.position = "relative";
            moonImage.style.left = "10px";
            moonImage.style.top = "8px";
            moonImage.style.height = "260px";
            break;
        case "landscape-simple":
            imageFrame.style.position = "absolute";
            imageFrame.style.left = "14px";
            imageFrame.style.top = "81px";
            imageFrame.style.width = "287px";
            imageFrame.style.height = "182px";
            moonImage.style.position = "relative";
            moonImage.style.left = "13px";
            moonImage.style.top = "11px";
            moonImage.style.height = "160px";
            break;
    }
    moonImage.src = "";
    imageUrl = "";
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
    data.viewType = view;
    data.moonOrientation =
        moonOrientation.options[moonOrientation.selectedIndex].value;
}
function downloadImage(fileBlob) {
    // file download credits:
    // https://openjavascript.info/2022/10/18/image-url-to-blob-in-javascript/
    // https://www.youtube.com/watch?v=cP5E0b21f_Y
    const url = URL.createObjectURL(fileBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `image.${data.format}`;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
function download() {
    if (imageUrl !== "") {
        fetch(imageUrl)
            .then((res) => res.blob())
            .then((blob) => downloadImage(blob))
            .catch((err) => console.error(`Error: ${err}`));
    }
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
        imageUrl = data.data.imageUrl;
        moonImage.src = imageUrl;
    })
        .catch((err) => {
        console.error("Error: ", err);
    });
}
updateButton.onclick = async () => {
    await update();
};
downloadButton.onclick = () => {
    download();
};
genButton.onclick = async () => {
    await genImage();
};
update();
