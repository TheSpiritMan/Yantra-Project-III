<script>
	import { API } from "$lib/helper";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";
	import { toastStore } from "$lib/store/toast";
	import dayjs from "dayjs";
	import {
		Button,
		Modal,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
	} from "flowbite-svelte";
	import { onMount } from "svelte";

	let allFiles = [];

	const getAllFiles = async () => {
		console.log("getAllFiles()");
		const { data, status } = await API.get("/getAllFiles");
		const response = data;

		// [{id: "", csv_file:"", result_file: ""}]
		console.log("response", response);
		if (response && status === 200) {
			allFiles = response;
			allFiles = response?.map((eachFile) => ({
				...eachFile,
				csv_file: eachFile?.csv_file?.replace(/\/csv_files\//, ""),
				result_file: eachFile?.result_file?.replace(/\/result_files\//, ""),
				date: dayjs(eachFile?.date)?.format("YYYY MMMM DD"),
			}));
			console.log("files successfully fetched...");

			// console.log("result_file", allFiles?.[0]?.result_file);
			// getFileResponse(allFiles?.[0]?.result_file);
		}
	};

	// const getFileResponse = async (resultFilePath) => {
	// 	const fileResponse = await API.get(resultFilePath);
	// 	console.log("fileResponse", fileResponse);
	// };

	const downloadFile = async (fileId) => {
		console.log("download()", fileId);
		const { data, status } = await API.get(`/download/${fileId}`);
		const response = data;

		// [{id: "", csv_file:"", result_file: ""}]
		console.log("response", response);
		if (response && status === 200) {
			// window.open("data:text/csv;charset=utf-8," + response);
			toastStore.showToast("success", "File downloaded successfully!", true);

			const url = window.URL.createObjectURL(
				new Blob([response], { type: `text/csv` })
			);
			const link = document.createElement("a");
			link.href = url;
			// link.setAttribute("download", "file name");
			// Changed line below
			document.body.appendChild(link); // This will add your link to the DOM
			// ------------------
			link.click();
			window.URL.revokeObjectURL(url);
			link.remove();
		}

		if (status !== 200) {
			toastStore.showToast("failure", response?.message, true);
		}
	};

	const deleteFile = async (fileId) => {
		console.log("deleteFile()", fileId);
		const { data, status } = await API.get(`/delete/${fileId}`);
		const response = data;
		console.log("delete response", response);
		if (status === 200) {
			console.log("file deleted successfully");
			toastStore.showToast("success", "File deleted successfully!", true);
			if (fileId === $fileUploadResponseStore?.fileUploadResponse?.["fileId"]) {
				$fileUploadResponseStore.fileUploadResponse = null;
			}
			getAllFiles();
			console.log("call get all files");
		}

		if (status !== 200) {
			toastStore.showToast("failure", response?.message, true);
		}
	};

	onMount(async () => {
		await getAllFiles();
	});

	let openModalToDeleteFile = false;

	let idOfFileToDelete = null;

	const openModal = (fileId) => {
		openModalToDeleteFile = true;
		idOfFileToDelete = fileId;
	};
</script>

<Modal bind:open={openModalToDeleteFile} size="xs" autoclose>
	<div class="text-center">
		<svg
			aria-hidden="true"
			class="mx-auto mb-4 w-14 h-14 text-gray-400 dark:text-gray-200"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
			xmlns="http://www.w3.org/2000/svg"
			><path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
			/></svg
		>
		<h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
			Are you sure you want to delete this file?
		</h3>
		<Button
			color="red"
			class="mr-2"
			on:click={async () => await deleteFile(idOfFileToDelete)}
			>Yes, I'm sure</Button
		>
		<Button color="alternative" on:click={() => (openModalToDeleteFile = false)}
			>No, cancel</Button
		>
	</div>
</Modal>

<div class=" py-12 px-10">
	<h3 class="text-3xl font-medium border-b-[3px] border-purple-700 inline py-3">
		<span class="text-purple-700">User History</span>
	</h3>
	<div class="mt-14">
		<Table shadow striped>
			<TableHead>
				<TableHeadCell>id</TableHeadCell>
				<TableHeadCell>Date</TableHeadCell>
				<TableHeadCell>uploaded file</TableHeadCell>
				<TableHeadCell>result file</TableHeadCell>
				<TableHeadCell>ACTION</TableHeadCell>
			</TableHead>

			<TableBody class="divide-y">
				{#each allFiles as eachFile}
					<TableBodyRow>
						<TableBodyCell>{eachFile?.id}</TableBodyCell>
						<TableBodyCell>{eachFile?.date}</TableBodyCell>
						<TableBodyCell>{eachFile?.csv_file}</TableBodyCell>
						<TableBodyCell>{eachFile?.result_file}</TableBodyCell>

						<TableBodyCell
							><Button
								color="purple"
								on:click={() => downloadFile(eachFile?.id)}
								class="mr-2"
							>
								Download
							</Button>
							<Button color="red" on:click={() => openModal(eachFile?.id)}>
								Delete
							</Button></TableBodyCell
						>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	</div>
</div>
