import { WebChannelHandler } from "./webchannel";
import Chart from "chart.js/auto";

export class ChartHandler {
    private chart: Chart | null = null;
    private readonly ctx: CanvasRenderingContext2D | null = null;

    constructor(canvasId: string) {
        const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
        if (!canvas) {
            console.error("Chart canvas not found!");
            return;
        }
        this.ctx = canvas.getContext("2d");
        if (!this.ctx) {
            console.error("Failed to get canvas context!");
        }
    }

    /**
     * Initializes or updates the chart with new data.
     * @param {string[]} labels - The labels for the X-axis.
     * @param {number[]} values - The data values for the Y-axis.
     * @param {string} type - The type of chart (e.g., "bar", "line", "pie").
     */
    updateChart(labels: string[], values: number[], type: "bar" | "line" | "pie" = "bar") {
        if (!this.ctx) return;

        if (this.chart) {
            this.chart.destroy(); // Prevent multiple instances
        }

        this.chart = new Chart(this.ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: "Chart Data",
                    data: values,
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}

const webChannel = WebChannelHandler.getInstance();
const chartHandler = new ChartHandler("chartCanvas");

async function setupChart() {
    await webChannel.registerCallback("preview", (msg) => {
        console.log("Received Data from Python (preview):", msg);
        const data = JSON.parse(msg);
        chartHandler.updateChart(data.labels, data.values, "bar");
    });

    // Request data from Python when the page loads
    await webChannel.sendMessage("preview", "request-data");
}

setupChart();