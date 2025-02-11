// Utility function for element selection
const $ = (id) => document.getElementById(id);

// Fetch Stock Prediction
async function fetchPrediction() {
    const ticker = $("ticker").value.trim();
    const algorithm = $("algorithm").value;

    if (!ticker) {
        alert("⚠️ Please enter a valid stock ticker.");
        return;
    }

    const endpoint = "/stock_prediction";
    const data = { ticker, model: algorithm };

    console.log("📤 Sending Request:", JSON.stringify(data));

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`❌ Failed to fetch prediction: ${await response.text()}`);
        }

        const result = await response.json();
        console.log("📥 Received Response:", result);

        if (result.error) {
            alert(`⚠️ Error: ${result.error}`);
            return;
        }

        // Display Chart
        if (result.chartUrl) {
            $("chart").src = result.chartUrl;
            $("chart-container").style.display = "block";
        }
    } catch (error) {
        console.error("❌ Error fetching prediction:", error);
        alert("An unexpected error occurred while fetching the prediction.");
    }
}

// Fetch default stock prediction (AAPL)
async function fetchDefaultStockPrediction() {
    try {
        const response = await fetch('/stock_prediction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: "AAPL", model: "LSTM" })
        });

        if (!response.ok) throw new Error(`❌ Default prediction failed: ${await response.text()}`);

        const data = await response.json();
        console.log("📊 Default Prediction Response:", data);

        if (data.chartUrl) {
            $("chart").src = data.chartUrl;
            $("chart-container").style.display = "block";
        }
    } catch (error) {
        console.error("❌ Error fetching default stock prediction:", error);
    }
}

// Run the default stock prediction when the page loads
fetchDefaultStockPrediction();