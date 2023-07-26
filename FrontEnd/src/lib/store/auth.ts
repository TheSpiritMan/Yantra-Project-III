import { API } from "$lib/helper";
import { writable } from "svelte/store";

export let token = writable("");

export let userInputStore = writable({ email: "", userName: "" });

const initialState = {
	me: null,
	isLoading: false,
};

const createUserStore = () => {
	const { set, subscribe, update } = writable(initialState);

	return {
		set,
		subscribe,

		me: async () => {
			update((store) => ({
				...store,
				isLoading: true,
			}));
			const { data, status } = await API.get("/me");
			const response = data;
			console.log("me response", response);
			update((store) => ({
				...store,
				isLoading: false,
				me: response,
			}));
		},
	};
};

export const userStore = createUserStore();
