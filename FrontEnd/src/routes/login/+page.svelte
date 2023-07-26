<script lang="ts">
	import { goto } from "$app/navigation";
	import { API, setUserToken } from "$lib/helper";
	import { token, userStore } from "$lib/store/auth";
	import { toastStore } from "$lib/store/toast";

	import { Button, Input, Label, Modal, Spinner } from "flowbite-svelte";

	const userLoginInputs = {
		username: "",
		password: "",
	};

	let isLoading = false;

	const login = async () => {
		isLoading = true;
		const { data, status } = await API.post("/login", userLoginInputs);
		const response = data;
		// {"message":"Login successful",
		// "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTE1ODYzNCwiaWF0IjoxNjg4NTY2NjM0LCJqdGkiOiI0NTI4NmY2OTU4YWI0ZDA2YjczOTMwZDg1ODNhMTIzOCIsInVzZXJfaWQiOiJjMDQyMjY5MS1hNjZhLTQzNDEtOGM5Mi05ZmRkMjIxYTRiZGIifQ.fClwG9YOyC_odqx8CQ0OoT2cfLML2Edjqgd0BRmk8io",
		// "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg4NTY3NTM0LCJpYXQiOjE2ODg1NjY2MzQsImp0aSI6ImE0Yjk1MDU4NmYzNjQxODlhNjc5MGNhOTYwZTIzNmNmIiwidXNlcl9pZCI6ImMwNDIyNjkxLWE2NmEtNDM0MS04YzkyLTlmZGQyMjFhNGJkYiJ9.vEQxmPISfGIQFiDkVkKEh_HS31lvVJGOHZtQo5AGv30"}
		console.log("response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("user logged in successfully!");
			toastStore.showToast("success", "User logged In successfully!", true);

			const userToken = {
				...response,
			};
			const accessToken = response?.access;
			$token = accessToken;
			localStorage.setItem("accessToken", accessToken);
			// setUserToken(accessToken);
			setUserToken(JSON.stringify(userToken));
			// userStore.me();
			// goto("/");
		}
		if (status !== 200) {
			isLoading = false;
			toastStore.showToast("failure", response?.message, true);
		}

		// if (status !== 200) {
		// 	toastStore.showToast("success", response?.message, true);
		// }
	};

	// const { access } = JSON.parse(getUserToken() ?? "");
</script>

<Modal open size="lg" permanent shadow>
	<div class="flex p-8 items-center">
		<div class="basis-full p-4 h-[30rem]">
			<img
				class="h-full"
				src="src/assets/images/undraw_astronaut_re_8c33.svg"
				alt=""
			/>
		</div>

		<div class="basis-full flex flex-col gap-7">
			<form
				class="flex flex-col gap-10"
				on:submit|preventDefault={async () => await login()}
			>
				<div>
					<div class="font-bold text-black text-2xl">Hi there!</div>
					<div class="">Welcome Back</div>
				</div>
				<div class="flex flex-col gap-5">
					<div class="space-y-2">
						<Label for="user-name">Username</Label>
						<Input
							type="text"
							id="user-name"
							placeholder="username"
							required
							bind:value={userLoginInputs.username}
						/>
					</div>

					<div class="space-y-2">
						<Label for="password">Password</Label>
						<Input
							type="password"
							id="password"
							placeholder="password"
							required
							bind:value={userLoginInputs.password}
						/>
					</div>

					<div class="flex items-center gap-1 text-sm">
						<div>Forgot Password?</div>
						<div
							class="text-purple-700 font-semibold cursor-pointer"
							on:click={() => goto("/reset-pass")}
						>
							Reset
						</div>
					</div>

					<Button disabled={isLoading} type="submit" color="purple"
						>Log In

						{#if isLoading}
							<Spinner color="white" size="6" class="ml-2" />
						{/if}
					</Button>
				</div>
			</form>

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
</Modal>
