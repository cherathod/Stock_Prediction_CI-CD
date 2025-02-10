// Utility function for element selection
const $ = (id) => document.getElementById(id);

// Show form fields based on prediction type
function showForm(type) {
    $("time-series-fields").style.display = (type === "Time-Series") ? "block" : "none";
    $("feature-fields").style.display = (type === "Feature-Based") ? "block" : "none";
}

// Fetch Stock Prediction based on selected input type
async function fetchPrediction() {
    const ticker = $("ticker").value.trim();
    const algorithm = $("algorithm").value;
    let endpoint = "";
    let data = {};

    if (!ticker) {
        alert("⚠️ Please enter a valid stock ticker.");
        return;
    }

    if ($("time-series-fields").style.display === "block") {
        const years = parseInt($("years").value);
        if (isNaN(years) || years <= 0) {
            alert("⚠️ Please enter a valid number of years.");
            return;
        }
        endpoint = "/time_predict";
        data = { ticker, years, model: algorithm };
    } else {
        const highPrice = parseFloat($("high-price").value);
        const lowPrice = parseFloat($("low-price").value);

        if (isNaN(highPrice) || isNaN(lowPrice)) {
            alert("⚠️ Please enter valid numerical values for High Price and Low Price.");
            return;
        }

        endpoint = "/feature_prediction";
        data = { ticker, features: [highPrice, lowPrice], algorithm };
    }

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

        // Display Time-Series Chart
        if (result.chartUrl) {
            $("chart").src = result.chartUrl;
            $("chart-container").style.display = "block";
        }

        // Display Feature-Based 3D Chart
        if (result.data) {
            Plotly.newPlot("plotly-3d", result.data, result.layout);
            $("3d-chart-container").style.display = "block";
        }
    } catch (error) {
        console.error("❌ Error fetching prediction:", error);
        alert("An unexpected error occurred while fetching the prediction.");
    }
}

// Toggle additional input fields dynamically
function toggleFields(fieldId) {
    document.querySelectorAll(".hidden-fields").forEach(field => field.style.display = "none");
    let selectedField = $(fieldId);
    selectedField.style.display = (selectedField.style.display === "none" || !selectedField.style.display) ? "block" : "none";
}

// Fetch default stock prediction (AAPL)
fetch('/stock-prediction', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stock: "AAPL" })
})
    .then(response => response.json())
    .then(data => console.log("📊 Default Prediction Response:", data))
    .catch(error => console.error("❌ Error fetching default stock prediction:", error));
