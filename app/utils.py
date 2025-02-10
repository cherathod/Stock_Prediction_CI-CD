import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def fetch_and_clean_data(ticker):
    # Mock implementation; replace with actual data-fetching logic
    return pd.DataFrame({"Date": pd.date_range(start="2020-01-01", periods=100), "Close": np.random.rand(100)})

def train_linear_regression(df):
    model = LinearRegression()
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Close"].values
    model.fit(X, y)
    return model

def train_random_forest(df):
    model = RandomForestRegressor()
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Close"].values
    model.fit(X, y)
    return model
