from flask import Blueprint, request, jsonify, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import datetime as dt
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model  # type: ignore
import matplotlib

matplotlib.use('Agg')  # Use 'Agg' backend for non-GUI environments

# Define Blueprint
prediction_bp = Blueprint('stock_prediction', __name__)

# Load Deep Learning Model
model_path = os.path.join(os.getcwd(), "data", "stock_dl_model.h5")
if os.path.exists(model_path):
    model = load_model(model_path)
else:
    model = None
    print("⚠️ Deep Learning model not found! Ensure 'data/stock_dl_model.h5' exists.")

# Function to Fetch Stock Data
def fetch_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            print(f"⚠️ No data found for {ticker}. Check ticker or API availability.")
            return None
        return data
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

# Stock Prediction Route
@prediction_bp.route('/stock_prediction', methods=['GET', 'POST'])
def stock_prediction():
    if request.method == 'POST':
        stock = request.form.get('stock', 'POWERGRID.NS')
        start, end = dt.datetime(2000, 1, 1), dt.datetime(2024, 10, 1)

        # Fetch Stock Data
        df = fetch_stock_data(stock, start, end)
        if df is None or df.empty or 'Close' not in df.columns:
            return jsonify({"error": f"Stock data not available for {stock}"}), 500

        # Split Data
        train_size = int(len(df) * 0.70)
        data_training = df['Close'][:train_size]
        data_testing = df['Close'][train_size:]

        if data_training.empty or data_testing.empty:
            return jsonify({"error": "Insufficient data for training/testing"}), 500

        # Scale Data
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_training_array = scaler.fit_transform(data_training.values.reshape(-1, 1))

        # Prepare Test Data
        past_100_days = data_training.tail(100)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.transform(final_df.values.reshape(-1, 1))

        # Generate x_test, y_test
        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)

        # Ensure Model Exists Before Prediction
        if model is None or len(x_test) == 0 or len(y_test) == 0:
            return jsonify({"error": "Model missing or insufficient data for prediction"}), 500

        # Predict and Rescale
        y_predicted = model.predict(x_test) * (1 / scaler.scale_[0])
        y_test = y_test * (1 / scaler.scale_[0])

        # Ensure Static Directory Exists
        static_dir = os.path.join(os.getcwd(), 'app', 'static')
        os.makedirs(static_dir, exist_ok=True)

        # Generate Plots
        def save_plot(fig, filename):
            path = os.path.join(static_dir, filename)
            fig.savefig(path)
            plt.close(fig)
            return f"static/{filename}"

        # 1. Line Plot
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(y_test, 'g', label="Original Price")
        ax1.plot(y_predicted, 'r', label="Predicted Price")
        ax1.set_title("Line Plot: Prediction vs Original")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Price")
        ax1.legend()
        line_plot_path = save_plot(fig1, "line_plot.png")

        # 2. Scatter Plot
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.scatter(range(len(y_test[:30])), y_test[:30], color='g', label="Original Price")
        ax2.scatter(range(len(y_predicted[:30])), y_predicted[:30], color='r', alpha=0.7, label="Predicted Price")
        ax2.set_title("Scatter Plot: Predicted vs Actual Prices")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Price")
        ax2.legend()
        scatter_plot_path = save_plot(fig2, "scatter_plot.png")

        # 3. Histogram
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        price_changes = np.diff(y_test[:100])
        ax3.hist(price_changes, bins=20, color='b', alpha=0.7)
        ax3.set_title("Histogram of Stock Price Changes")
        ax3.set_xlabel("Price Change")
        ax3.set_ylabel("Frequency")
        histogram_path = save_plot(fig3, "histogram.png")

        return render_template(
            'stock_prediction.html',
            line_plot=line_plot_path,
            scatter_plot=scatter_plot_path,
            histogram=histogram_path
        )

    return render_template('stock_prediction.html')

# File Download Route
@prediction_bp.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join("app", "static", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404
