import { writable } from "svelte/store";

const initialState = {
	messageType: "",
	message: "",
	isVisible: null,
};

const createToastStore = () => {
	const { set, subscribe, update } = writable(initialState);

	return {
		set,
		subscribe,

		showToast: (messageType, message, state) => {
			let counter = 6;

			setTimeout(() => {
				counter -= 1;
				if (counter < 0) {
					update((store) => ({
						...store,

						isVisible: false,
					}));
				}
			}, 1000);

			update((store) => ({
				...store,
				message: message,
				messageType: messageType,
				isVisible: state,
			}));
		},

		hideToast: () => {
			update((store) => ({
				...store,
				isVisible: false,
			}));
		},
	};
};

export const toastStore = createToastStore();
