const imageFrame = document.getElementById("image-frame");
const moonImage = document.getElementById("moon-image");
const recentImages = document.getElementById("recent-cmb");
const genButton = document.getElementsByClassName("gen-button");
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
const updateButton = document.getElementById("update-button");

const DEFAULT_BACKGROUND_COLOR = "black";
const DEFAULT_HEADING_COLOR = "white";
const DEFAULT_TEXT_COLOR = "white";
const DEFAULT_LATITUDE = 6.56774;
const DEFAULT_LONGITUDE = 79.88956;
const DEFAULT_DATE = "2024-07-18";

function update() {
	fetch("/update", {
		method: "POST",
		body: JSON.stringify({
			format: format.value,
			moonStyle: moonStyle.value,
			backgroundStyle: backgroundStyle.value,
			backgroundColor:
				backgroundColor.value != ""
					? backgroundColor.value
					: DEFAULT_BACKGROUND_COLOR,
			headingColor:
				headingColor.value != "" ? headingColor.value : DEFAULT_HEADING_COLOR,
			textColor: textColor.value != "" ? textColor.value : DEFAULT_TEXT_COLOR,
			latitude:
				latitude.value != "" ? parseFloat(latitude.value) : DEFAULT_LATITUDE,
			longitude:
				longitude.value != "" ? parseFloat(longitude.value) : DEFAULT_LONGITUDE,
			date: date.value != "" ? date.value : DEFAULT_DATE,
			viewType: viewType.value,
			orientation: moonOrientation.value,
		}),
	})
		.then((_res) => {
			console.log("Info Updated!");
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}

updateButton.onclick = update;
