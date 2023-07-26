<script>
	import { PolarArea } from "svelte-chartjs";

	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		ArcElement,
		RadialLinearScale,
	} from "chart.js";
	import { fileUploadResponseStore } from "$lib/store/ai-processed-data";

	ChartJS.register(Title, Tooltip, Legend, ArcElement, RadialLinearScale);

	$: data = {
		datasets: [
			{
				data: [
					$fileUploadResponseStore?.fileUploadResponse?.fraudCount,
					$fileUploadResponseStore?.fileUploadResponse?.genuineCount,
				],
				backgroundColor: ["rgba(247, 70, 74, 0.5)", "rgba(70, 191, 189, 0.5)"],
				label: "Fraud detection result", // for legend
			},
		],
		labels: ["Fraud", "Genuine"],
	};
</script>

<PolarArea {data} options={{ responsive: true }} />
