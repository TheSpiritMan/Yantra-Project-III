import axios from "axios";
import type { InternalAxiosRequestConfig, AxiosResponse } from "axios";
import { getUserToken } from "./storage";
import { goto } from "$app/navigation";

const axiosInstance = axios.create({
	baseURL: "https://yantra-api.sandabgc.com.np",
});

axiosInstance.interceptors.request.use(
	(config: InternalAxiosRequestConfig) => {
		const token = localStorage.getItem("accessToken");
		// const { access } = JSON.parse(getUserToken() ?? "");
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
			console.log("access", token);
		}
		console.log("config", config);

		return config;
	},
	(error) => {
		console.log("error", error);
		return Promise.reject(error);
	}
);

axiosInstance.interceptors.response.use(
	(response: AxiosResponse) => response,
	(error) => {
		if (error.response && error.response?.status === 401) {
			// Token is invalid or expired
			// Handle token invalidation,
			console.log("token expired");
			localStorage.clear();
			location.reload();
			goto("/login");
		}
		return Promise.reject(error);
	}
);

export const API = axiosInstance;
