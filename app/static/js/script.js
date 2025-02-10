async function fetchPrediction() {
    const ticker = document.getElementById("ticker").value;
    const algorithm = document.getElementById("algorithm").value;
    let endpoint = "";
    let data = {};

    // Set the correct endpoint and data based on prediction type
    if (document.getElementById('time-series-fields').style.display === 'block') {
        const years = document.getElementById("years").value;
        endpoint = "/time_predict";
        data = { ticker, years: years, model: algorithm };
    } else if (document.getElementById('feature-fields').style.display === 'block') {
        const highPrice = document.getElementById("high-price").value;
        const lowPrice = document.getElementById("low-price").value;
        endpoint = "/feature_prediction";
        data = { ticker, features: [highPrice, lowPrice], algorithm };
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("chart-container").style.display = "none";
    document.getElementById("3d-chart-container").style.display = "none";

    // Fetch the prediction from the correct endpoint
    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    document.getElementById("loading").style.display = "none";

    if (response.ok) {
        const result = await response.json();
        if (result.error) {
            alert(result.error);
            return;
        }

        // Handle time-series chart (if returned by backend)
        if (result.chartUrl) {
            document.getElementById("chart").src = result.chartUrl;
            document.getElementById("chart-container").style.display = "block";
        }

        // Handle 3D chart (if returned by backend)
        if (result.data) {
            Plotly.newPlot("plotly-3d", result.data, result.layout);
            document.getElementById("3d-chart-container").style.display = "block";
        }
    } else {
        alert("Failed to fetch prediction");
    }
}
