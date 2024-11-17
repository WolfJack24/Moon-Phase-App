const genButton = document.getElementById("gen-button") as HTMLButtonElement;
const downloadButton = document.getElementById(
	"download-button"
) as HTMLButtonElement;
const updateButton = document.getElementById(
	"update-button"
) as HTMLButtonElement;

const imageFrame = document.getElementById("image-frame") as HTMLDivElement;
const moonImage = document.getElementById("moon-image") as HTMLImageElement;
const recentImages = document.getElementById("recent-cmb") as HTMLSelectElement;

const format = document.getElementById("format-input") as HTMLSelectElement;
const moonStyle = document.getElementById(
	"moon-style-input"
) as HTMLSelectElement;
const backgroundStyle = document.getElementById(
	"background-style"
) as HTMLSelectElement;
const backgroundColor = document.getElementById(
	"background-color-input"
) as HTMLInputElement;
const headingColor = document.getElementById(
	"heading-color-input"
) as HTMLInputElement;
const textColor = document.getElementById(
	"text-color-input"
) as HTMLInputElement;
const latitude = document.getElementById("latitude-input") as HTMLInputElement;
const longitude = document.getElementById(
	"longitude-input"
) as HTMLInputElement;
const date = document.getElementById("date-input") as HTMLInputElement;
const viewType = document.getElementById(
	"view-type-input"
) as HTMLSelectElement;
const moonOrientation = document.getElementById(
	"orientation-input"
) as HTMLSelectElement;

const DEFAULT_BACKGROUND_COLOR = "black";
const DEFAULT_HEADING_COLOR = "white";
const DEFAULT_TEXT_COLOR = "white";
const DEFAULT_LATITUDE = 6.56774;
const DEFAULT_LONGITUDE = 79.88956;
const DEFAULT_DATE = "2024-07-18";

const HOST = "https://api.astronomyapi.com/api/v2/studio/moon-phase";

class Data {
	format: string;
	moonStyle: string;
	backgroundStyle: string;
	backgroundColor: string;
	headingColor: string;
	textColor: string;
	latitude: number;
	longitude: number;
	date: string;
	viewType: string;
	moonOrientation: string;

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
			hexAuthString = data.authKey as string;
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

function downloadImage(fileBlob: Blob) {
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

	let expAuthString = hexAuthString.match(/.{1,2}/g) as RegExpMatchArray;
	let authString = expAuthString.reduce(
		(acc, char) => acc + String.fromCharCode(parseInt(char, 16)),
		""
	) as string;
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
