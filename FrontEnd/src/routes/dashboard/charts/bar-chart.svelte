<script>
	import { Bar } from "svelte-chartjs";

	import {
		Chart,
		Title,
		Tooltip,
		Legend,
		BarElement,
		CategoryScale,
		LinearScale,
	} from "chart.js";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";

	Chart.register(
		Title,
		Tooltip,
		Legend,
		BarElement,
		CategoryScale,
		LinearScale
	);

	$: data = {
		labels: ["Fraud", "Genuine"],
		datasets: [
			{
				label: "count",
				data: [
					$fileUploadResponseStore?.fileUploadResponse?.fraudCount,
					$fileUploadResponseStore?.fileUploadResponse?.genuineCount,
				],
				backgroundColor: ["rgba(255, 134,159,0.4)", "rgba(113, 205, 205,0.4)"],
				borderWidth: 2,
				borderColor: ["rgba(255, 134, 159, 1)", "rgba(113, 205, 205, 1)"],
			},
		],
	};
</script>

<Bar {data} options={{ responsive: true }} />
