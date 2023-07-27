<script lang="ts">
	import { goto } from "$app/navigation";
	import { API } from "$lib/helper";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";
	import { toastStore } from "$lib/store/toast";
	import { Button, Dropzone, Heading } from "flowbite-svelte";
	import dayjs from "dayjs";

	let isDragged = false;
	let file: File | null = null;
	let isLoading = false;
	let fileInput: HTMLElement;

	const addDragClass = (e: Event) => {
		e.preventDefault();
		isDragged = true;
	};

	const removeDragClass = (e: Event) => {
		e.preventDefault();
		isDragged = false;
	};

	const onDrop = (e: DragEvent) => {
		e.preventDefault();
		console.log("dropHandle()", e.dataTransfer);
		file = e.dataTransfer?.files?.[0]!;
		removeDragClass(e);
	};

	interface FileTarget extends EventTarget {
		files: FileList;
		// Add other properties if needed
	}

	const onChooseFile = (e: Event) => {
		console.log("handleChooseFile", e.target);
		const target = e.target as FileTarget;
		file = target.files?.[0];
		console.log("file", file);
	};

	const upload = async () => {
		console.log("upload()");
		const formData = new FormData();
		formData.append("csv_file", file!);
		const { data, status } = await API.post("/upload-file", formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		});
		const response = data;
		// {"message":"File Uploaded Successfully","File ID":"e10dff87-f59b-48d7-9dd9-e3c5c1c0595e",
		// "counts":{"0":369,"1":337}}
		console.log("response", response);
		if (response && status === 200) {
			console.log("file uploaded successfully!");
			toastStore.showToast("success", "File uploaded successfully!", true);

			// localStorage.setItem(
			// 	"userInfo",
			// 	JSON.stringify({ email: userRegistrationInputs.email })
			// );
			// goto("/verify-otp");
			$fileUploadResponseStore.fileUploadResponse = {
				fraudCount: response?.counts?.["0"],
				genuineCount: response?.counts?.["1"],
				fileId: response?.["File ID"],
				message: response?.message,
				date: dayjs(response?.date)?.format("YYYY MMMM DD"),
			};
			goto("/dashboard");
		}

		if (status !== 200) {
			toastStore.showToast("failure", "Only CSV files are allowed.", true);
		}
	};
</script>

<div class="p-12 inline-flex">
	<Heading tag="h1" class="!text-[#1a1844] !text-4xl">Upload csv file</Heading>
</div>

<div
	class="uploadBox"
	class:isDragged
	on:drag|preventDefault|stopPropagation={() => {
		return false;
	}}
	on:dragstart|preventDefault|stopPropagation={() => {
		return false;
	}}
	on:dragend|preventDefault|stopPropagation={removeDragClass}
	on:dragover|preventDefault|stopPropagation={addDragClass}
	on:dragenter|preventDefault|stopPropagation={addDragClass}
	on:dragleave|preventDefault|stopPropagation={removeDragClass}
	on:drop|preventDefault|stopPropagation={onDrop}
>
	<svg
		class="svg-inline--fa fa-file-import file-icon"
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

	{#if !isLoading && !file}
		<div class="fileUploadWrapper">
			<label class="fileUploadLabel">
				<span class="chooseFile">
					<svg
						class="svg-inline--fa fa-folder-open fa-w-18"
						aria-hidden="true"
						focusable="false"
						data-prefix="far"
						data-icon="folder-open"
						role="img"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 576 512"
						data-fa-i2svg=""
					>
						<path
							fill="currentColor"
							d="M527.9 224H480v-48c0-26.5-21.5-48-48-48H272l-64-64H48C21.5 64 0 85.5 0 112v288c0 26.5 21.5 48 48 48h400c16.5 0 31.9-8.5 40.7-22.6l79.9-128c20-31.9-3-73.4-40.7-73.4zM48 118c0-3.3 2.7-6 6-6h134.1l64 64H426c3.3 0 6 2.7 6 6v42H152c-16.8 0-32.4 8.8-41.1 23.2L48 351.4zm400 282H72l77.2-128H528z"
						/>
					</svg>
					<span> Choose file</span>
				</span>
				<input
					type="file"
					on:change={(e) => onChooseFile(e)}
					bind:this={fileInput}
					accept=".csv"
				/>
			</label>
			<span>or drag them here.</span>
		</div>
	{/if}

	{#if file}
		<div class="chosenFileContainer">
			<p>{file?.name || "readme.md"}</p>

			<!-- action button wrapper -->
			<div class="chosenFileActionContainer">
				<label class="fileUploadLabel">
					<span class="chooseFile">
						<svg
							class="svg-inline--fa fa-folder-open fa-w-18"
							aria-hidden="true"
							focusable="false"
							data-prefix="far"
							data-icon="folder-open"
							role="img"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 576 512"
							data-fa-i2svg=""
						>
							<path
								fill="currentColor"
								d="M527.9 224H480v-48c0-26.5-21.5-48-48-48H272l-64-64H48C21.5 64 0 85.5 0 112v288c0 26.5 21.5 48 48 48h400c16.5 0 31.9-8.5 40.7-22.6l79.9-128c20-31.9-3-73.4-40.7-73.4zM48 118c0-3.3 2.7-6 6-6h134.1l64 64H426c3.3 0 6 2.7 6 6v42H152c-16.8 0-32.4 8.8-41.1 23.2L48 351.4zm400 282H72l77.2-128H528z"
							/>
						</svg>
						<span> Change</span>
					</span>
					<input
						type="file"
						on:change={(e) => onChooseFile(e)}
						bind:this={fileInput}
						accept=".csv"
					/>
				</label>

				<!-- remove icon -->
				<div class="removeIcon" on:click={() => (file = null)}>
					<svg
						class="svg-inline--fa fa-minus fa-w-11"
						aria-hidden="true"
						focusable="false"
						data-prefix="fal"
						data-icon="minus"
						role="img"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 384 512"
						data-fa-i2svg=""
						><path
							fill="currentColor"
							d="M376 232H8c-4.42 0-8 3.58-8 8v32c0 4.42 3.58 8 8 8h368c4.42 0 8-3.58 8-8v-32c0-4.42-3.58-8-8-8z"
						/></svg
					>
				</div>
			</div>
		</div>
	{/if}

	{#if file}
		<div class="submitButtons mt-11 space-x-4">
			<Button
				on:click={() => (file = null)}
				class="!border-2 !border-solid !border-[#1a1844] !text-[#1a1844] hover:!text-[#413cab] hover:!border-[#413cab] hover:!bg-transparent !transition-all !ease-in-out !duration-150 !py-2 !px-6 !font-semibold !text-base !rounded-lg"
				outline
			>
				Cancel
			</Button>
			<Button
				on:click={async () => await upload()}
				class="!bg-[#1a1844] !text-[#fff]  hover:!bg-[#413cab] !transition-all !ease-in-out !duration-150 !py-2 !px-6 !font-semibold !text-base !rounded-lg"
				>Upload</Button
			>
		</div>
	{/if}
</div>

<style>
	.uploadBox {
		background: #fff;
		border-radius: 16px;
		margin: 0 auto;
		padding: 82px 58px 50px;
		min-height: 332px;
		/* min-width: 642px; */
		width: 60%;
		display: flex;
		flex-direction: column;
		align-items: center;
		position: relative;
	}

	.uploadBox.isDragged {
		background: rgba(98, 90, 255, 0.1);
	}

	.uploadBox:after {
		content: "";
		position: absolute;
		top: 16px;
		bottom: 16px;
		left: 16px;
		right: 16px;
		border: 2px dashed #625aff;
		border-radius: 16px;
		pointer-events: none;
	}

	.uploadBox .file-icon {
		width: 5rem;
		color: #625aff;
		margin-bottom: 40px;
		pointer-events: none;
	}

	.fileUploadWrapper {
		display: flex;
		height: 28px;
		align-items: center;

		/* 
		.isDragged & {
			pointer-events: none;
		} */
	}

	.fileUploadWrapper > span {
		margin-left: 8px;
	}

	.chooseFile {
		display: flex;
		align-items: center;
		color: #1a1844;
		border-bottom: 2px solid #1a1844;
		cursor: pointer;
		transition: all ease-in-out 0.2s;
	}

	.chooseFile:hover {
		color: #413cab;
		border-bottom: 2px solid #413cab;
	}

	.chooseFile svg {
		width: 1.2rem;
	}

	.chooseFile span {
		padding-left: 4px;
		font-weight: 800;
	}

	input[type="file"] {
		display: none;
	}

	.chosenFileContainer {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid rgba(26, 24, 68, 0.25);
		padding: 10px 0;
	}

	.chosenFileActionContainer {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.removeIcon {
		background: rgba(0, 0, 0, 0.25);
		border-radius: 100%;
		padding: -1px;
		width: 1rem;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 3px 6px;
		width: 1.8rem;
		height: 1.8rem;
		transition: all ease-in-out 0.2s;
		cursor: pointer;
	}

	.removeIcon:hover {
		background: rgba(0, 0, 0, 0.1);
	}
</style>
