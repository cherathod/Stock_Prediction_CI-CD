// Utility function for element selection
const $ = (id) => document.getElementById(id);

// Show loading state
function showLoading(isLoading) {
    const btn = $("fetch-btn");
    if (btn) {
        btn.disabled = isLoading;
        btn.innerHTML = isLoading ? '<span class="loader"></span> Fetching...' : 'Get Prediction';
    }
}

// Fetch Stock Prediction
async function fetchPrediction() {
    const ticker = $("ticker").value.trim();
    const algorithm = $("algorithm").value;

    if (!ticker) {
        alert("⚠️ Please enter a valid stock ticker.");
        return;
    }

    const endpoint = "/stock_prediction";
    const requestData = { ticker, model: algorithm };

    console.log("🔄 Sending Request:", JSON.stringify(requestData));

    try {
        showLoading(true);

        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        });

        if (!response.ok) {
            throw new Error(`❌ Failed to fetch prediction: ${await response.text()}`);
        }

        const result = await response.json();
        console.log("✅ Received Response:", result);

        if (result.error) {
            alert(`⚠️ Error: ${result.error}`);
            return;
        }

        // Update Plots Dynamically
        updateChart("line-chart", result.line_plot);
        updateChart("three-d-chart", result.three_d_plot);
        updateChart("scatter-chart", result.scatter_plot);
        updateChart("histogram-chart", result.histogram);

        // Update Candlestick Chart (Opens in a new tab)
        if (result.candlestick_chart) {
            $("candlestick-link").href = `/static/${result.candlestick_chart}`;
            $("candlestick-container").style.display = "block";
        }
    } catch (error) {
        console.error("🚨 Error fetching prediction:", error);
        alert("⚠️ An unexpected error occurred while fetching the prediction.");
    } finally {
        showLoading(false);
    }
}

// Utility function to update charts
function updateChart(elementId, chartPath) {
    const chartElement = $(elementId);
    const container = $(elementId + "-container");

    if (chartElement && chartPath) {
        chartElement.src = `/static/${chartPath}`;
        container.style.display = "block";
    } else {
        console.warn(`⚠️ Chart data missing for: ${elementId}`);
    }
}

// Fetch default stock prediction (AAPL)
async function fetchDefaultStockPrediction() {
    try {
        console.log("🔄 Fetching default stock prediction...");

        const response = await fetch("/stock_prediction", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticker: "AAPL", model: "LSTM" }),
        });

        if (!response.ok) throw new Error(`❌ Default prediction failed: ${await response.text()}`);

        const data = await response.json();
        console.log("✅ Default Prediction Response:", data);

        updateChart("line-chart", data.line_plot);
        updateChart("three-d-chart", data.three_d_plot);
        updateChart("scatter-chart", data.scatter_plot);
        updateChart("histogram-chart", data.histogram);

        if (data.candlestick_chart) {
            $("candlestick-link").href = `/static/${data.candlestick_chart}`;
            $("candlestick-container").style.display = "block";
        }
    } catch (error) {
        console.error("🚨 Error fetching default stock prediction:", error);
    }
}

// Run the default stock prediction when the page loads
document.addEventListener("DOMContentLoaded", fetchDefaultStockPrediction);
