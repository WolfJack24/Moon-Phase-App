<script lang="ts">
	// Imports
	import { CreatePayload } from "../bindings/changeme/payloadservice";
	import { Payload } from "../bindings/changeme/models";

	// Local Classes and Interfaces

	// Global Variables
	let payload: Payload = new Payload();
	let currentImage: string =
		"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/330px-FullMoon2010.jpg";

	// Functions
	function createPayload(): Promise<Payload> {
		return new Promise((resolve) => {
			Promise.resolve().then(async () => {
				payload = await CreatePayload();
				if (payload) {
					console.log("Payload created successfully");
					resolve(payload);
				} else {
					throw new Error("Failed to create payload");
				}
			});
		});
	}

	async function init(): Promise<void> {
		try {
			payload = await createPayload();
		} catch (error) {
			console.error("Error during initialization:", error);
		}
	}

	init();
</script>

<div class="img-container">
	<img src={currentImage} alt="Current Selected Moon Phase" class="img" />
</div>

<style>
	.img-container {
		background-color: aqua;
	}

	.img {
		width: 160px;
		height: 260px;
	}
</style>
