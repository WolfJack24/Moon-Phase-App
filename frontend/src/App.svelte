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

	(async () => {
		payload = await createPayload();
		for (let i = 0; i < Colour.ColourCount; i++) {
			Colours[i] = await getColour(i);
		}
	})();
</script>

<div
	style="
		--frame-bg: {Colours[Colour.FrameBackgroundColour]}
		--btn-bg: {Colours[Colour.ButtonBackgroundColour]}
		--btn-hover: {Colours[Colour.ButtonHoverColour]}
		--btn-text: {Colours[Colour.ButtonTextColour]}
	"
></div>

<div class="img-container">
	<img src={currentImage} alt="Current Selected Moon Phase" class="img" />
</div>

<div class="recent-images-container">
	<p>Recent Images</p>
	<select></select>
</div>

<input class="btn set-info-btn" type="button" value="Set Info" />
<input class="btn save-image-btn" type="button" value="Save Image" />
<input class="btn gen-image-btn" type="button" value="Gen Image" />

<style>
	.img-container {
		position: absolute;
		width: 221px;
		height: 277px;
		left: 29px;
		top: 37px;
		background-color: var(--frame-bg);
	}

	.img {
		position: absolute;
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
		background-color: var(--frame-bg);
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
		position: absolute;
		width: 140px;
		height: 28px;
		left: 342px;
		/* ? No Top? */
		background-color: var(--btn-bg);
		color: var(--btn-text);
	}

	.btn:hover {
		background-color: var(--btn-hover);
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
