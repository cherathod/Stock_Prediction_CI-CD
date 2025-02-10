from flask import Blueprint, request, jsonify, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy import stats
import pandas as pd
from sklearn.preprocessing import StandardScaler
import yfinance as yf
import plotly.graph_objs as go  # type: ignore
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import load_model  # type: ignore
import logging

prediction_bp = Blueprint('prediction', __name__)

# Function to fetch and clean stock data
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

@prediction_bp.route('/time_predict', methods=['POST'])
def time_predict():
    try:
        data = request.get_json()
        if not data or 'ticker' not in data or 'years' not in data or 'model' not in data:
            return jsonify({'error': 'Invalid input data'}), 400

        ticker = data['ticker']
        years = int(data['years'])
        model_name = data['model']
        stock_data = get_cleaned_stock_data(ticker, '2021-01-01', '2022-01-01')
        
        stock_data['pct_change'] = stock_data['Close'].pct_change()
        stock_data['rolling_mean'] = stock_data['Close'].rolling(window=10).mean()
        stock_data['rolling_std'] = stock_data['Close'].rolling(window=10).std()
        required_columns = ['pct_change', 'rolling_mean', 'rolling_std']

        if model_name == "LSTM":
            model = load_model('models/lstm_model.h5')
        elif model_name == "Random Forest":
            model = RandomForestRegressor()
            model.fit(stock_data[required_columns].dropna(), stock_data['Close'].dropna())
        else:
            model = LinearRegression()
            model.fit(stock_data[required_columns].dropna(), stock_data['Close'].dropna())

        prediction = model.predict(stock_data[required_columns].tail(1))[0]

        plt.figure(figsize=(10, 6))
        plt.plot(stock_data.index, stock_data['Close'], label='Close Price')
        plt.title(f'{ticker} Stock Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()

        return jsonify({'prediction': prediction, 'chartUrl': f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        logging.error(f"Error in /time_predict: {str(e)}")
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/feature_prediction', methods=['POST'])
def feature_prediction():
    try:
        data = request.get_json()
        if not data or 'ticker' not in data or 'features' not in data or 'model' not in data:
            return jsonify({'error': 'Invalid input data'}), 400

        ticker = data['ticker']
        features = data['features']
        model_name = data['model']
        stock_data = get_cleaned_stock_data(ticker, '2021-01-01', '2022-01-01')
        
        stock_data['pct_change'] = stock_data['Close'].pct_change()
        stock_data['rolling_mean'] = stock_data['Close'].rolling(window=10).mean()
        stock_data['rolling_std'] = stock_data['Close'].rolling(window=10).std()

        if model_name == "LSTM":
            model = load_model('models/lstm_model.h5')
        elif model_name == "Random Forest":
            model = RandomForestRegressor()
            model.fit(stock_data[['pct_change', 'rolling_mean', 'rolling_std']].dropna(), stock_data['Close'].dropna())
        else:
            model = LinearRegression()
            model.fit(stock_data[['pct_change', 'rolling_mean', 'rolling_std']].dropna(), stock_data['Close'].dropna())

        prediction = model.predict([features])[0]

        plt.figure(figsize=(10, 6))
        plt.plot(stock_data.index, stock_data['Close'], label='Close Price')
        plt.title(f'{ticker} Stock Price Prediction with Features')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()

        return jsonify({'prediction': prediction, 'chartUrl': f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        logging.error(f"Error in /feature_prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/stock_prediction')
def stock_prediction():
    return render_template('stock_prediction.html')
