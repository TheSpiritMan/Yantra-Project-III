<script lang="ts">
	import { goto } from "$app/navigation";
	import { API, setUserToken } from "$lib/helper";
	import { token } from "$lib/store/auth";
	import { toastStore } from "$lib/store/toast";

	import { Button, Input, Label, Modal, Spinner } from "flowbite-svelte";

	const resetPassInputs = {
		email: "",
		otp: "",
		new_password: "",
	};

	let step = 0;
	let isLoading = false;

	const forgotPass = async () => {
		isLoading = true;
		const { data, status } = await API.post("/forgot-pass", {
			email: resetPassInputs?.email,
		});
		const response = data;
		// {"message":"Login successful",
		// "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTE1ODYzNCwiaWF0IjoxNjg4NTY2NjM0LCJqdGkiOiI0NTI4NmY2OTU4YWI0ZDA2YjczOTMwZDg1ODNhMTIzOCIsInVzZXJfaWQiOiJjMDQyMjY5MS1hNjZhLTQzNDEtOGM5Mi05ZmRkMjIxYTRiZGIifQ.fClwG9YOyC_odqx8CQ0OoT2cfLML2Edjqgd0BRmk8io",
		// "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg4NTY3NTM0LCJpYXQiOjE2ODg1NjY2MzQsImp0aSI6ImE0Yjk1MDU4NmYzNjQxODlhNjc5MGNhOTYwZTIzNmNmIiwidXNlcl9pZCI6ImMwNDIyNjkxLWE2NmEtNDM0MS04YzkyLTlmZGQyMjFhNGJkYiJ9.vEQxmPISfGIQFiDkVkKEh_HS31lvVJGOHZtQo5AGv30"}
		console.log("response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("forgot pass otp sent successfully!");
			toastStore.showToast("success", "OTP sent successfully!", true);

			step = 1;
		}

		if (status !== 200) {
			isLoading = false;
			toastStore.showToast("failure", response?.message, true);
		}
	};

	const resetPass = async () => {
		isLoading = true;
		const { data, status } = await API.post("/reset-pass", resetPassInputs);
		const response = data;
		// {"message":"Login successful",
		// "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTE1ODYzNCwiaWF0IjoxNjg4NTY2NjM0LCJqdGkiOiI0NTI4NmY2OTU4YWI0ZDA2YjczOTMwZDg1ODNhMTIzOCIsInVzZXJfaWQiOiJjMDQyMjY5MS1hNjZhLTQzNDEtOGM5Mi05ZmRkMjIxYTRiZGIifQ.fClwG9YOyC_odqx8CQ0OoT2cfLML2Edjqgd0BRmk8io",
		// "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg4NTY3NTM0LCJpYXQiOjE2ODg1NjY2MzQsImp0aSI6ImE0Yjk1MDU4NmYzNjQxODlhNjc5MGNhOTYwZTIzNmNmIiwidXNlcl9pZCI6ImMwNDIyNjkxLWE2NmEtNDM0MS04YzkyLTlmZGQyMjFhNGJkYiJ9.vEQxmPISfGIQFiDkVkKEh_HS31lvVJGOHZtQo5AGv30"}
		console.log("response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("password reset successfull!");
			toastStore.showToast("success", "Password changed successfully!", true);

			goto("/login");
		}

		if (status !== 200) {
			isLoading = false;
			toastStore.showToast("failure", response?.message, true);
		}
	};

	// const { access } = JSON.parse(getUserToken() ?? "");
</script>

<Modal open size="lg" permanent shadow>
	<div class="flex p-8 items-center">
		<div class="basis-full p-4 h-[30rem]">
			<img
				class="h-full"
				src="src/assets/images/undraw_forgot_password_re_hxwm.svg"
				alt=""
			/>
		</div>

		<div class="basis-full flex flex-col gap-7">
			{#if step === 0}
				<form
					class="flex flex-col gap-10"
					on:submit|preventDefault={async () => await forgotPass()}
				>
					<div>
						<div class="font-bold text-black text-2xl">Forgot Password?</div>
						<div class="">Reset</div>
					</div>
					<div class="flex flex-col gap-5">
						<div class="space-y-2">
							<Label for="email">Email</Label>
							<Input
								type="email"
								id="email"
								placeholder="email"
								required
								bind:value={resetPassInputs.email}
							/>
						</div>

						<!-- <div class="space-y-2">
						<Label for="password">Password</Label>
						<Input
							type="password"
							id="password"
							placeholder="password"
							required
							bind:value={userLoginInputs.password}
						/>
					</div> -->

						<Button disabled={isLoading} type="submit" color="purple">
							Submit
							{#if isLoading}
								<Spinner color="white" size="6" class="ml-2" />
							{/if}
						</Button>
					</div>
				</form>
			{/if}

			{#if step === 1}
				<form
					class="flex flex-col gap-10"
					on:submit|preventDefault={async () => await resetPass()}
				>
					<div>
						<div class="font-bold text-black text-2xl">Forgot Password?</div>
						<div class="">Reset</div>
					</div>
					<div class="flex flex-col gap-5">
						<div class="space-y-2">
							<Label for="email">Email</Label>
							<Input
								type="email"
								disabled
								id="email"
								placeholder="email"
								required
								bind:value={resetPassInputs.email}
							/>
						</div>

						<div class="space-y-2">
							<Label for="otp">OTP</Label>
							<Input
								type="text"
								id="otp"
								placeholder="otp..."
								required
								bind:value={resetPassInputs.otp}
							/>
						</div>

						<div class="space-y-2">
							<Label for="password">New Password</Label>
							<Input
								type="password"
								id="password"
								placeholder="password"
								required
								bind:value={resetPassInputs.new_password}
							/>
						</div>

						<Button disabled={isLoading} type="submit" color="purple">
							Reset
							{#if isLoading}
								<Spinner color="white" size="6" class="ml-2" />
							{/if}
						</Button>
					</div>
				</form>
			{/if}

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
