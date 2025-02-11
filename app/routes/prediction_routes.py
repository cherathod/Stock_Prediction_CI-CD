from flask import Blueprint, request, jsonify, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy import stats
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import yfinance as yf
import plotly.graph_objs as go  # type: ignore
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import load_model  # type: ignore
import logging
import datetime as dt
import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

prediction_bp = Blueprint('stock_prediction', __name__)

# Load deep learning model
model = load_model('data/stock_dl_model.h5')

def get_cleaned_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data.dropna().drop_duplicates()
    stock_data.index = pd.to_datetime(stock_data.index)
    z_scores = np.abs(stats.zscore(stock_data.select_dtypes(include=[np.number])))
    stock_data = stock_data[(z_scores < 3).all(axis=1)]
    scaler = StandardScaler()
    stock_data[['Close', 'Open', 'High', 'Low', 'Volume']] = scaler.fit_transform(
        stock_data[['Close', 'Open', 'High', 'Low', 'Volume']]
    )
    stock_data = stock_data.drop(columns=['Volume'])
    return stock_data

@prediction_bp.route('/stock_prediction', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form.get('stock', 'POWERGRID.NS')
        start = dt.datetime(2000, 1, 1)
        end = dt.datetime(2024, 10, 1)
        df = yf.download(stock, start=start, end=end)

        data_training = df['Close'][0:int(len(df) * 0.70)]
        data_testing = df['Close'][int(len(df) * 0.70):]

        scaler = MinMaxScaler(feature_range=(0, 1))
        data_training_array = scaler.fit_transform(data_training.values.reshape(-1, 1))

        past_100_days = data_training.tail(100)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.transform(final_df.values.reshape(-1, 1))

        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)

        y_predicted = model.predict(x_test) * (1 / scaler.scale_[0])
        y_test = y_test * (1 / scaler.scale_[0])

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test, 'g', label="Original Price")
        ax.plot(y_predicted, 'r', label="Predicted Price")
        ax.set_title("Prediction vs Original Trend")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.legend()

        # Check the `app/static/` directory exists
        static_dir = os.path.join(os.getcwd(), 'app', 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)  # Create the folder if it doesn't exist

        # Save the image in `app/static/`
        image_filename = 'stock_prediction.png'
        image_path = os.path.join(static_dir, image_filename)
        plt.savefig(image_path)
        plt.close(fig)

        return render_template('stock_prediction.html', plot_path_prediction=image_filename)
    
    return render_template('stock_prediction.html')

@prediction_bp.route('/download/<filename>')
def download_file(filename):
    return send_file(f"static/{filename}", as_attachment=True)

@prediction_bp.route('/stock_prediction')
def stock_prediction():
    return render_template('stock_prediction.html')
