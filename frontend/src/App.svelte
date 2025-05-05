<script lang="ts">
	// Imports
	import { Payload, Colours } from "../bindings/changeme/models";
	import { CreatePayload } from "../bindings/changeme/payloadservice";
	import { GetColour } from "../bindings/changeme/colourservice";

	// Local Classes and Interfaces

	// Functions
	async function createPayload(): Promise<Payload> {
		return await CreatePayload();
	}

	async function getColour(colour: Colours): Promise<string> {
		return await GetColour(colour);
	}

	// Global Variables
	let payload: Payload = new Payload();
	let currentImage: string = "";
	let ButtonBack: string = "";

	(async () => {
		payload = await createPayload();
		currentImage =
			"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/330px-FullMoon2010.jpg";
		ButtonBack = await getColour(Colours.ButtonBackgroundColour);
	})();
</script>

<div class="img-container" style="background-color: {ButtonBack}">
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
