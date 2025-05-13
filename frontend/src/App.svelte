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
	class="img-container"
	style="background-color: {Colours[Colour.FrameBackgroundColour]}"
>
	<img src={currentImage} alt="Current Selected Moon Phase" class="img" />
</div>

<style>
	/* .img-container {
	} */

	.img {
		width: 160px;
		height: 260px;
	}
</style>
