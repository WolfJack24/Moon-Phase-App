<script lang="ts">
	// Imports
	import { Payload, Colours } from "../bindings/changeme/models";
	import { CreatePayload } from "../bindings/changeme/payloadservice";
	import { GetColour } from "../bindings/changeme/colourservice";

	// Local Classes and Interfaces

	// Global Variables
	let payload: Payload = createPayload();
	let currentImage: string =
		"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/330px-FullMoon2010.jpg";

	// Functions
	function createPayload(): Payload {
		let localpayload: Payload = new Payload();
		Promise.all([CreatePayload()])
			.then((results) => {
				localpayload = results[0];
			})
			.catch((error) => {
				console.error("Error creating payload:", error);
			});
		return localpayload;
	}

	function getColour(colour: Colours): string {
		let colourstring: string = "";
		Promise.all([GetColour(colour)])
			.then((results) => {
				colourstring = results[0];
			})
			.catch((error) => {
				console.error("Error getting colour:", error);
			});
		return colourstring;
	}
</script>

<div
	class="img-container"
	style="background-color: {getColour(Colours.ButtonBackgroundColour)}"
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
