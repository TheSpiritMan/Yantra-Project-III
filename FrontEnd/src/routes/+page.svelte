<script lang="ts">
	import { goto } from "$app/navigation";
	import { Alert, Timeline, TimelineItem } from "flowbite-svelte";
	import { onMount } from "svelte";

	// onMount(() => goto("/register"));
</script>

<!-- <div class="" /> -->

<div class=" py-12 px-10">
	<h3 class="text-3xl font-medium border-b-[3px] border-purple-700 inline py-3">
		Welcome to Yantra <span class="text-purple-700"
			>(Credit Card Fraud detector)</span
		>
	</h3>

	<div class="w-fit mt-11">
		<Alert color="blue">
			<svg
				slot="icon"
				aria-hidden="true"
				class="w-5 h-5"
				fill="currentColor"
				viewBox="0 0 20 20"
				xmlns="http://www.w3.org/2000/svg"
				><path
					fill-rule="evenodd"
					d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
					clip-rule="evenodd"
				/></svg
			>
			<span class="font-semibold text-lg">How fraud detection works?</span>
		</Alert>
	</div>

	<div class="flex">
		<div class="mt-11 flex-1">
			<Timeline order="vertical">
				<TimelineItem
					title="Upload CSV file which contains transactions data"
					svgClass="!hidden"
				>
					<!-- <p class="text-base font-normal text-gray-500 dark:text-gray-400">
					Get started with dozens of web components and interactive elements.
				</p> -->
				</TimelineItem>
				<TimelineItem
					title="Process CSV file data through AI model"
					svgClass="!hidden"
				>
					<!-- <p class="text-base font-normal text-gray-500 dark:text-gray-400">
					Get started with dozens of web components and interactive elements.
				</p> -->
				</TimelineItem>
				<TimelineItem
					title="Provide fraud and genuine transaction count"
					svgClass="!hidden"
				>
					<!-- <p class="text-base font-normal text-gray-500 dark:text-gray-400">
					Get started with dozens of web components and interactive elements.
				</p> -->
				</TimelineItem>

				<TimelineItem
					title="Provide updated csv file with fraud and genuine transaction count to download"
					svgClass="!hidden"
				>
					<!-- <p class="text-base font-normal text-gray-500 dark:text-gray-400">
					Get started with dozens of web components and interactive elements.
				</p> -->
				</TimelineItem>
			</Timeline>
		</div>

		<div class="flex-1 flex justify-end">
			<img
				class="w-[600px] rounded-[3%]"
				src="src/assets/images/5f8da531af3cda1546bae979_HERO_IMAGE_2020.gif"
				alt=""
			/>
		</div>
	</div>
</div>

<style>
	:global(ol li) {
		margin-bottom: 4.5rem !important;
	}
</style>
