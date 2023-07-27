<script>
	import { Doughnut } from "svelte-chartjs";
	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		ArcElement,
		CategoryScale,
	} from "chart.js";
	import BarChart from "./charts/bar-chart.svelte";
	import LineChart from "./charts/line-chart.svelte";
	import PolarAreaChart from "./charts/polar-area-chart.svelte";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";
	import {
		Button,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
	} from "flowbite-svelte";
	import { API } from "$lib/helper";
	import { toastStore } from "$lib/store/toast";
	ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

	$: console.log("fileuploadresponsestore", $fileUploadResponseStore);

	$: doughtnutData = {
		labels: ["Fraud", "Genuine"],
		datasets: [
			{
				data: [
					$fileUploadResponseStore?.fileUploadResponse?.fraudCount,
					$fileUploadResponseStore?.fileUploadResponse?.genuineCount,
				],
				backgroundColor: ["#F7464A", "#46BFBD"],
				hoverBackgroundColor: ["#FF5A5E", "#5AD3D1"],
			},
		],
	};

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
	};
</script>

<div class=" py-12 px-10">
	<h3 class="text-3xl font-medium border-b-[3px] border-purple-700 inline py-3">
		<span class="text-purple-700">Dashboard</span>
	</h3>

	<div class="mt-14">
		<Table shadow striped>
			<TableHead>
				<TableHeadCell>File Id</TableHeadCell>
				<TableHeadCell>Date</TableHeadCell>
				<TableHeadCell>Fraud Count</TableHeadCell>
				<TableHeadCell>Genuine Count</TableHeadCell>
				<TableHeadCell>ACTION</TableHeadCell>
			</TableHead>

			<TableBody class="divide-y">
				<TableBodyRow>
					<TableBodyCell
						>{$fileUploadResponseStore?.fileUploadResponse
							?.fileId}</TableBodyCell
					>
					<TableBodyCell
						>{$fileUploadResponseStore?.fileUploadResponse?.date}</TableBodyCell
					>
					<TableBodyCell
						>{$fileUploadResponseStore?.fileUploadResponse
							?.fraudCount}</TableBodyCell
					>
					<TableBodyCell
						>{$fileUploadResponseStore?.fileUploadResponse
							?.genuineCount}</TableBodyCell
					>
					<TableBodyCell
						><Button
							color="purple"
							on:click={() =>
								downloadFile(
									$fileUploadResponseStore?.fileUploadResponse?.fileId
								)}
							class="mr-2"
						>
							Download
						</Button>
					</TableBodyCell>
				</TableBodyRow>
			</TableBody>
		</Table>
	</div>

	<div class="grid grid-cols-2 gap-x-3 mt-11 gap-y-10 items-center">
		<div class="w-[65%] border-[2px] border-gray-200 rounded-2xl p-8">
			<Doughnut data={doughtnutData} options={{ responsive: true }} />
		</div>

		<div class="w-[65%] border-[2px] border-gray-200 rounded-2xl p-8">
			<BarChart />
		</div>

		<!-- <div class="w-[65%] border-[2px] border-gray-200 rounded-2xl p-8">
			<LineChart />
		</div> -->

		<div class="w-[65%] border-[2px] border-gray-200 rounded-2xl p-8">
			<PolarAreaChart />
		</div>
	</div>
</div>
