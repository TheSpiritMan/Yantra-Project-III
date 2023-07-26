<script lang="ts">
	import { goto } from "$app/navigation";
	import { API } from "$lib/helper";
	import { userInputStore } from "$lib/store/auth";
	import { toastStore } from "$lib/store/toast";
	import { Button, Input, Label, Modal, Spinner, Toast } from "flowbite-svelte";
	import { onMount } from "svelte";

	const userRegistrationInputs = {
		username: "",
		email: "",
		password: "",
		first_name: "",
		last_name: "",
	};

	let isLoading = false;

	const register = async () => {
		console.log("register()");
		isLoading = true;
		const { data, status } = await API.post(
			"/register",
			userRegistrationInputs
		);
		const response = data;
		console.log("response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("user registration done successfully!");
			toastStore.showToast(
				"success",
				"User registration done successfully!",
				true
			);
			$userInputStore.email = userRegistrationInputs.email;

			// localStorage.setItem(
			// 	"userInfo",
			// 	JSON.stringify({ email: userRegistrationInputs.email })
			// );
			goto("/verify-otp");
		}

		if (status !== 200) {
			isLoading = false;
			toastStore.showToast("failure", response?.message, true);
		}
	};

	// onMount(() => register());

	// onMount(() => {
	// 	localStorage.setItem(
	// 		"userInfo",
	// 		JSON.stringify({ email: "grishmink@gmail.com" })
	// 	);
	// });

	$: console.log("userRegistrationInputs", userRegistrationInputs);
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
				on:submit|preventDefault={async () => {
					await register();
					// console.log("register");
				}}
			>
				<div>
					<div class="font-bold text-black text-2xl">Get started</div>
					<div class="">Create your account now</div>
				</div>
				<div class="flex flex-col gap-5">
					<div class="space-y-2">
						<Label for="user-name">Username</Label>
						<Input
							type="text"
							id="user-name"
							placeholder="username"
							bind:value={userRegistrationInputs.username}
							required
						/>
					</div>
					<div class="space-y-2">
						<Label for="first-name">Firstname</Label>
						<Input
							type="text"
							id="first-name"
							placeholder="firstname..."
							bind:value={userRegistrationInputs.first_name}
							required
						/>
					</div>
					<div class="space-y-2">
						<Label for="last-name">Lastname</Label>
						<Input
							type="text"
							id="last-name"
							placeholder="lastname..."
							bind:value={userRegistrationInputs.last_name}
							required
						/>
					</div>
					<div class="space-y-2">
						<Label for="email">Email</Label>
						<Input
							type="email"
							id="email"
							placeholder="email"
							required
							bind:value={userRegistrationInputs.email}
						/>
					</div>
					<div class="space-y-2">
						<Label for="password">Password</Label>
						<Input
							type="password"
							id="password"
							placeholder="password"
							required
							bind:value={userRegistrationInputs.password}
						/>
					</div>

					<Button disabled={isLoading} type="submit" color="purple">
						Register
						{#if isLoading}
							<Spinner color="white" size="6" class="ml-2" />
						{/if}
					</Button>
				</div>
			</form>

			<div class="flex items-center justify-center gap-1">
				<div>Have an account?</div>
				<div
					class="text-purple-700 font-semibold cursor-pointer"
					on:click={() => goto("/login")}
				>
					Login
				</div>
			</div>
		</div>
	</div>
</Modal>
