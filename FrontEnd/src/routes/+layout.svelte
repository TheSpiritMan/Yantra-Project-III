<script lang="ts">
	import {
		Avatar,
		Button,
		Dropdown,
		DropdownDivider,
		DropdownHeader,
		DropdownItem,
		Input,
		Label,
		Modal,
		Sidebar,
		SidebarBrand,
		SidebarGroup,
		SidebarItem,
		SidebarWrapper,
		Spinner,
	} from "flowbite-svelte";
	import "../app.postcss";
	import "../assets/fonts.css";
	import { page } from "$app/stores";
	import { API, UserStorage, getUserToken } from "../lib/helper";
	import { goto } from "$app/navigation";
	import { token, userStore } from "$lib/store/auth";
	import ToastMessage from "$lib/components/toast-message.svelte";
	import { toastStore } from "$lib/store/toast";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";

	$: activePath = $page.url.pathname;

	let userName = null;
	let accessToken = null;
	let userInfo = null;

	$: isVisible = $toastStore.isVisible;
	$: userInfo = getUserToken();
	$: accessToken = localStorage.getItem("accessToken") ?? $token;

	// $: if (userInfo) {
	// 	console.log("userInfo", JSON.parse(userInfo));
	// 	// userName = JSON.parse(userInfo)?.userName;
	// }
	$: console.log("userINfo", userInfo);
	$: console.log("accessToken", accessToken);

	$: if (accessToken) {
		console.log("inside accesstoken");
		userStore.me();
		goto("/");
	} else {
		goto("/login");
	}

	$: console.log("userStore", $userStore);

	const signOut = async () => {
		userInfo = getUserToken();
		const refresh = JSON.parse(userInfo)?.refresh;
		const { data, status } = await API.post("/logout", {
			refresh: refresh,
		});
		const response = data;
		console.log("response", response);
		if (status === 200) {
			console.log("user logged out successfully!");
			toastStore.showToast("success", "user logged out successfully!", true);

			localStorage.clear();
			location.reload();
			goto("/login");
		}

		if (status !== 200) {
			toastStore.showToast("failure", response?.message, true);
		}
	};

	let isChangePassModalVisible = false;
	let showUserAvatarDropdown = false;

	const openModalToChangePass = () => {
		isChangePassModalVisible = true;
	};

	let newPass = "";
	let isLoading = false;

	let className =
		"flex items-center p-2 text-base font-bold text-black bg-white dark:bg-gray-700 rounded-lg dark:text-white hover:bg-white dark:hover:bg-gray-700";

	const changePass = async () => {
		console.log("changePass()");
		isLoading = true;
		const { data, status } = await API.post("/change-pass", {
			new_password: newPass,
		});
		const response = data;
		console.log("change pass response", response);
		if (response?.message && status === 200) {
			isLoading = false;
			console.log("user password changed successfully!");
			toastStore.showToast("success", response?.message, true);
			isChangePassModalVisible = false;
			// localStorage.setItem(
			// 	"userInfo",
			// 	JSON.stringify({ email: userRegistrationInputs.email })
			// );
			// goto("/verify-otp");
		}

		if (status !== 200) {
			isLoading = false;
			toastStore.showToast("failure", response?.message, true);
		}
	};
</script>

<!-- change pass modal -->

{#if isChangePassModalVisible}
	<Modal bind:open={isChangePassModalVisible} size="sm" shadow>
		<form
			class="flex flex-col gap-10"
			on:submit|preventDefault={async () => await changePass()}
		>
			<div>
				<div class="font-bold text-black text-2xl">Change Password</div>
			</div>
			<div class="flex flex-col gap-5">
				<div class="space-y-2">
					<Label for="password">New Password</Label>
					<Input
						type="password"
						id="password"
						placeholder="new password..."
						required
						bind:value={newPass}
					/>
				</div>

				<Button disabled={isLoading} type="submit" color="purple">
					Change Password
					{#if isLoading}
						<Spinner color="white" size="6" class="ml-2" />
					{/if}
				</Button>
			</div>
		</form>
	</Modal>
{/if}

{#if accessToken}
	<div class="flex w-full h-full">
		<Sidebar class="!flex !flex-col">
			<div class="flex items-center p-[1.5rem]">
				<div class="w-[3rem] h-[5rem]">
					<img
						class="w-full h-full object-cover"
						src="src/assets/images/runs.gif"
						alt=""
					/>
				</div>
				<a
					href="/upload-file"
					class="font-extrabold text-[2rem] text-[#625aff] flex justify-center"
					>Yantra</a
				>
			</div>
			<SidebarWrapper
				class="!bg-[#f2f2f2] !flex-1 !rounded-r-[20px] !p-[2rem_1.5rem]"
			>
				<!-- set ul class to set spacing between items vertically -->
				<SidebarGroup>
					<div class="relative">
						<div
							class="flex gap-3 cursor-pointer"
							on:click={() =>
								(showUserAvatarDropdown = !showUserAvatarDropdown)}
						>
							<Avatar border
								>{$userStore.me?.first_name?.[0]}{$userStore?.me
									?.last_name?.[0]}</Avatar
							>
							<div class="text-lg font-bold">
								{`${$userStore.me?.first_name} ${$userStore.me?.last_name}`}
							</div>
						</div>

						<div
							class="bg-white rounded-md p-7 mt-1 h-[10vh] shadow-md absolute right-0 left-0 {showUserAvatarDropdown
								? 'block'
								: 'hidden'}"
						>
							<div
								class="bg-slate-50 cursor-pointer"
								on:click={() => {
									openModalToChangePass();
									showUserAvatarDropdown = false;
								}}
							>
								Change Password
							</div>
						</div>
					</div>

					<div class="flex flex-col !gap-[1.4rem] !mt-[2rem]">
						<SidebarItem
							label="Home"
							href="/"
							active={activePath === "/"}
							activeClass={className}
							class="hover:bg-white"
						>
							<svelte:fragment slot="icon">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="lucide lucide-home"
									><path
										d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"
									/><polyline points="9 22 9 12 15 12 15 22" /></svg
								>
							</svelte:fragment>
						</SidebarItem>
						<div class="relative">
							<SidebarItem
								label="Dashboard"
								href="/dashboard"
								active={activePath === "/dashboard"}
								activeClass={className}
								class="hover:bg-white {$fileUploadResponseStore?.fileUploadResponse ===
								null
									? 'pointer-events-none !cursor-not-allowed'
									: ''} "
							>
								<svelte:fragment slot="icon">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-6 h-6"
										><path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z"
										/><path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z"
										/></svg
									>
								</svelte:fragment>
							</SidebarItem>

							{#if $fileUploadResponseStore?.fileUploadResponse !== null}
								<div
									class="absolute w-3 h-3 bg-green-500 rounded-full right-11 top-[14px]"
								/>
							{/if}
						</div>

						<SidebarItem
							label="Upload File"
							href="/upload-file"
							active={activePath === "/upload-file"}
							activeClass={className}
							class="hover:bg-white"
						>
							<svelte:fragment slot="icon">
								<svg
									class="svg-inline--fa fa-file-import w-6 h-6"
									aria-hidden="true"
									focusable="false"
									data-prefix="fal"
									data-icon="file-import"
									role="img"
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 512 512"
									data-fa-i2svg=""
								>
									<path
										fill="currentColor"
										d="M497.9 97.98L414.02 14.1c-9-9-21.2-14.1-33.89-14.1H175.99C149.5.1 128 21.6 128 48.09V288H8c-4.42 0-8 3.58-8 8v16c0 4.42 3.58 8 8 8h248v52.67c0 10.98 6.38 20.55 16.69 24.97 14.93 6.45 26.88-1.61 30.88-5.39l71.72-68.12c5.62-5.33 8.72-12.48 8.72-20.12s-3.09-14.8-8.69-20.11l-71.78-68.16c-8.28-7.8-20.41-9.88-30.84-5.38-10.31 4.42-16.69 13.98-16.69 24.97V288H160V48.09c0-8.8 7.2-16.09 16-16.09h176.04v104.07c0 13.3 10.7 23.93 24 23.93h103.98v304.01c0 8.8-7.2 16-16 16H175.99c-8.8 0-16-7.2-16-16V352H128v112.01c0 26.49 21.5 47.99 47.99 47.99h288.02c26.49 0 47.99-21.5 47.99-47.99V131.97c0-12.69-5.1-24.99-14.1-33.99zM288 245.12L350 304l-62 58.88V245.12zm96.03-117.05V32.59c2.8.7 5.3 2.1 7.4 4.2l83.88 83.88c2.1 2.1 3.5 4.6 4.2 7.4h-95.48z"
									/>
								</svg>
							</svelte:fragment>
						</SidebarItem>

						<SidebarItem
							label="History"
							href="/history"
							active={activePath === "/history"}
							activeClass={className}
							class="hover:bg-white"
						>
							<svelte:fragment slot="icon">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="lucide lucide-history"
									><path
										d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"
									/><path d="M3 3v5h5" /><path d="M12 7v5l4 2" /></svg
								>
							</svelte:fragment>
						</SidebarItem>
					</div>

					<div
						class="absolute bottom-2 cursor-pointer underline text-center w-[10%] flex gap-1"
						on:click={() => signOut()}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							class="lucide lucide-log-out"
							><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline
								points="16 17 21 12 16 7"
							/><line x1="21" x2="9" y1="12" y2="12" /></svg
						>
						Sign Out
					</div>
				</SidebarGroup>
			</SidebarWrapper>
		</Sidebar>

		<div class="flex-1 overflow-y-auto">
			<slot />
		</div>
	</div>
{:else if activePath === "/login" || activePath === "/register" || activePath === "/verify-otp" || activePath === "/reset-pass"}
	<slot />
{/if}

{#if isVisible}
	<ToastMessage />
{/if}
