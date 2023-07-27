<script lang="ts">
	import { goto } from "$app/navigation";
	import { API } from "$lib/helper";
	import { userInputStore } from "$lib/store/auth";
	import { toastStore } from "$lib/store/toast";
	import { Button, Input, Label, Modal, Spinner } from "flowbite-svelte";
	import { onMount } from "svelte";

	const otpVeificationInputs = {
		email: "",
		otp: "",
	};

	let isLoading = false;

	const verifyOtp = async () => {
		// try {
		// 	isLoading = true;
		// 	const { data, status } = await API.post(
		// 		"/verify-otp",
		// 		otpVeificationInputs
		// 	);
		// 	const response = data;
		// 	// {"message":"OTP verification successful"}
		// 	console.log("response", response);
		// 	if (response?.message && status === 200) {
		// 		isLoading = false;
		// 		console.log("user otp verified successfully!");
		// 		toastStore.showToast("success", "OTP verified successfully!", true);
		// 		goto("/login");
		// 	}
		// } catch (error) {
		// 	isLoading = false;
		// 	toastStore.showToast("failure", "invalid otp", true);
		// }

		isLoading = true;
		const { data, status } = await API.post(
			"/verify-otp",
			otpVeificationInputs
		);
		const response = data;
		// {"message":"OTP verification successful"}
		console.log("response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("user otp verified successfully!");
			toastStore.showToast("success", response?.message, true);
			goto("/login");
		}

		if (status !== 200) {
			isLoading = false;
			toastStore.showToast(
				"failure",
				typeof response?.message === "object" ? "invalid otp" : "otp expired",
				true
			);
		}
	};

	const resendOtp = async () => {
		isLoading = true;
		const { data, status } = await API.post("/resend-otp", {
			email: otpVeificationInputs.email,
		});
		const response = data;
		// {"message":"OTP verification successful"}
		console.log("response", response);
		isLoading = false;
		if (response?.message && status === 200) {
			console.log("otp sent successfully!");
			toastStore.showToast("success", "OTP sent successfully!", true);

			// goto("/login");
		}

		if (status !== 200) {
			toastStore.showToast("failure", response?.message, true);
		}
	};

	onMount(() => {
		// const userInfo = localStorage.getItem("userInfo") ?? "";
		// if (userInfo) {
		// 	otpVeificationInputs.email = JSON.parse(userInfo)?.email ?? "";
		// }
		otpVeificationInputs.email = $userInputStore.email;
	});
</script>

<Modal open size="lg" permanent shadow>
	<div class="flex p-8 items-center">
		<div class="basis-full p-4 h-[30rem]">
			<img
				class="h-full"
				src="src/assets/images/undraw_two_factor_authentication_namy.svg"
				alt=""
			/>
		</div>

		<div class="basis-full flex flex-col gap-7">
			<form
				class="flex flex-col gap-10"
				on:submit|preventDefault={async () => await verifyOtp()}
			>
				<div>
					<div class="font-bold text-black text-2xl">Verify OTP</div>
				</div>
				<div class="flex flex-col gap-5">
					<div class="space-y-2">
						<Label for="email">Email</Label>
						<Input
							type="email"
							id="email"
							placeholder="email"
							required
							bind:value={otpVeificationInputs.email}
							disabled
						/>
					</div>
					<div class="space-y-2">
						<Label for="OTP">OTP</Label>
						<Input
							type="text"
							id="OTP"
							placeholder="OTP"
							required
							bind:value={otpVeificationInputs.otp}
						/>
					</div>

					<div class="flex items-center gap-1 text-sm">
						<div>Didn't receive an OTP?</div>
						<div
							class="text-purple-700 font-semibold cursor-pointer"
							on:click={() => resendOtp()}
						>
							Resend

							{#if isLoading}
								<Spinner color="white" size="6" class="ml-2" />
							{/if}
						</div>
					</div>
					<Button disabled={isLoading} type="submit" color="purple">
						Verify
						{#if isLoading}
							<Spinner color="white" size="6" class="ml-2" />
						{/if}
					</Button>
				</div>
			</form>

			<div>
				<div class="flex items-center justify-center gap-1">
					<div>Have an account?</div>
					<div
						class="text-purple-700 font-semibold cursor-pointer"
						on:click={() => goto("/login")}
					>
						Login
					</div>
				</div>

				<div class="flex items-center justify-center gap-1">
					<div>Don't have an account?</div>
					<div
						class="text-purple-700 font-semibold cursor-pointer"
						on:click={() => goto("/register")}
					>
						Register
					</div>
				</div>
			</div>
		</div>
	</div>
</Modal>
