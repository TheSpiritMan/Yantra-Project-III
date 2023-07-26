<script>
	import { toastStore } from "$lib/store/toast";
	import { Toast } from "flowbite-svelte";
	import { fly } from "svelte/transition";

	$: message = $toastStore.message;
	$: messageType = $toastStore.messageType;
</script>

<Toast
	bind:open={$toastStore.isVisible}
	transition={fly}
	params={{ x: 200 }}
	color={messageType == "success" ? "green" : "red"}
	position="top-right"
	class="z-[9999]"
>
	<svelte:fragment slot="icon">
		{#if messageType === "success"}
			<svg
				aria-hidden="true"
				class="w-5 h-5"
				fill="currentColor"
				viewBox="0 0 20 20"
				xmlns="http://www.w3.org/2000/svg"
				><path
					fill-rule="evenodd"
					d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
					clip-rule="evenodd"
				/></svg
			>
		{/if}

		{#if messageType === "failure"}
			<svg
				aria-hidden="true"
				class="w-5 h-5"
				fill="currentColor"
				viewBox="0 0 20 20"
				xmlns="http://www.w3.org/2000/svg"
				><path
					fill-rule="evenodd"
					d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
					clip-rule="evenodd"
				/></svg
			>
		{/if}

		<!-- <span class="sr-only">Check icon</span> -->
	</svelte:fragment>
	{message}
</Toast>
