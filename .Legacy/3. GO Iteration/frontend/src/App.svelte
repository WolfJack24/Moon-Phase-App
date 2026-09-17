<script lang="ts">
	// Imports
	import { Payload, Colour } from "../bindings/changeme/models";
	import { CreatePayload } from "../bindings/changeme/payloadservice";
	import { GetColour } from "../bindings/changeme/colourservice";

	// Local Classes and Interfaces

	// Functions
	async function createPayload(): Promise<Payload> {
		return await CreatePayload();
	}

	async function getColour(colour: Colour): Promise<string> {
		return await GetColour(colour);
	}

	// Global Variables
	let payload: Payload = new Payload();
	let currentImage: string = "";
	let Colours: Array<string> = [];

	// Elements
	let imgContainer: HTMLDivElement;
	let img: HTMLImageElement;
	let recentImagesContainer: HTMLDivElement;
	let recentImagesSelect: HTMLSelectElement;
	let setInfoBtn: HTMLInputElement;
	let saveImageBtn: HTMLInputElement;
	let genImageBtn: HTMLInputElement;

	(async () => {
		payload = await createPayload();
		for (let i = 0; i < Colour.ColourCount; i++) {
			Colours[i] = await getColour(i);
		}

		// Set Colours
		if (document.getElementById("img-container") !== null) {
			imgContainer = document.getElementById("img-container") as HTMLDivElement;
			img = document.getElementById("img") as HTMLImageElement;
			recentImagesContainer = document.getElementById(
				"recent-images-container"
			) as HTMLDivElement;
			recentImagesSelect = document.getElementById(
				"images-select"
			) as HTMLSelectElement;
			setInfoBtn = document.getElementById("set-info-btn") as HTMLInputElement;
			saveImageBtn = document.getElementById(
				"save-image-btn"
			) as HTMLInputElement;
			genImageBtn = document.getElementById(
				"gen-image-btn"
			) as HTMLInputElement;

			imgContainer.style.backgroundColor =
				Colours[Colour.FrameBackgroundColour];
			recentImagesContainer.style.backgroundColor =
				Colours[Colour.FrameBackgroundColour];
			setInfoBtn.style.backgroundColor = Colours[Colour.ButtonBackgroundColour];
			saveImageBtn.style.backgroundColor =
				Colours[Colour.ButtonBackgroundColour];
			genImageBtn.style.backgroundColor =
				Colours[Colour.ButtonBackgroundColour];
		}

		let colour = Colours[Colour.FrameBackgroundColour];
		colour = Colours[Colour.ButtonBackgroundColour];
		colour = Colours[Colour.ButtonHoverColour];
		colour = Colours[Colour.ButtonTextColour];
	})();
</script>

<div class="img-container" id="img-container">
	<img
		src={currentImage}
		alt="Current Selected Moon Phase"
		class="img"
		id="img"
	/>
</div>

<div class="recent-images-container" id="recent-images-container">
	<p>Recent Images</p>
	<select id="images-select"></select>
</div>

<input
	class="btn set-info-btn"
	id="btn set-info-btn"
	type="button"
	value="Set Info"
/>
<input
	class="btn save-image-btn"
	id="btn save-image-btn"
	type="button"
	value="Save Image"
/>
<input
	class="btn gen-image-btn"
	id="btn gen-image-btn"
	type="button"
	value="Gen Image"
/>

<style>
	.img-container {
		position: absolute;
		width: 221px;
		height: 277px;
		left: 29px;
		top: 37px;
		border-radius: 5px;
	}

	.img {
		position: rel;
		width: 160px;
		height: 260px;
		left: 10px;
		top: 8px;
	}

	.recent-images-container {
		position: absolute;
		width: 187px;
		height: 66px;
		left: 295px;
		top: 37px;
	}

	.recent-images-container p {
		position: absolute;
		width: 84px;
		height: 16px;
		left: 17px;
		top: 5px;
	}

	.recent-images-container select {
		position: absolute;
		width: 153px;
		height: 28px;
		left: 17px;
		top: 28px;
	}

	.btn {
		cursor: pointer;
		position: absolute;
		width: 140px;
		height: 28px;
		left: 342px;
		/* ? No Top? */
		border-width: 0.5px;
		border-radius: 5px;
		transition: background-color 0.5s ease;
	}

	.btn:hover {
		background-color: pink;
	}

	.btn.set-info-btn {
		top: 216px;
	}

	.btn.save-image-btn {
		top: 251px;
	}

	.btn.gen-image-btn {
		top: 286px;
	}
</style>
