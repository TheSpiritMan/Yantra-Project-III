import { writable } from "svelte/store";

const initialState = {
	// fileUploadResponse: {
	// 	fraudCount: null,
	// 	genuineCount: null,
	// 	fileId: null,
	// 	message: null,
	// },
	fileUploadResponse: null,
};

const createAiProcessedDataStore = () => {
	const { update, set, subscribe } = writable(initialState);
	return {
		set,
		subscribe,
	};

	// setFileUploadResponse: () => {

	// }
};

export const fileUploadResponseStore = createAiProcessedDataStore();
