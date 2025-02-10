import io
import base64
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.graph_objs as go # type: ignore
from app.models import StockData

plot_bp = Blueprint("plot", __name__)

# Route to generate and display a 3D plot of stock prices and features
@plot_bp.route("/plot3d", methods=["GET"])
def plot_3d_stock_prices():
    stock_symbol = request.args.get("symbol", default=None)
    if not stock_symbol:
        return render_template("plot.html", error="Please provide a stock symbol.")

    start_date = request.args.get("start", "2000-01-01")
    end_date = request.args.get("end", "2022-01-01")

    # Fetch stock data
    stock_data = StockData.query.filter_by(symbol=stock_symbol).filter(
        StockData.date.between(start_date, end_date)
    ).order_by(StockData.date.asc()).all()

    if not stock_data:
        return render_template("plot.html", error=f"No data found for '{stock_symbol}'.")

    # Convert to DataFrame
    data = pd.DataFrame([{
        "date": record.date,
        "price": record.price,
        "pct_change": record.pct_change,
        "rolling_mean": record.rolling_mean,
        "rolling_std": record.rolling_std
    } for record in stock_data])

    # Create 3D scatter plot
    trace = go.Scatter3d(
        x=data["pct_change"],
        y=data["rolling_mean"],
        z=data["rolling_std"],
        mode='markers',
        marker=dict(size=5, color=data["price"], colorscale='Viridis', opacity=0.8)
    )

    layout = go.Layout(
        title=f'{stock_symbol} 3D Stock Price Features',
        scene=dict(
            xaxis_title='Pct Change',
            yaxis_title='Rolling Mean',
            zaxis_title='Rolling Std'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Convert plot to HTML instead of PNG
    plot_html = fig.to_html(full_html=False)

    return render_template("plot.html", plot_html=plot_html, symbol=stock_symbol)

# API endpoint to retrieve 3D stock price trends as JSON
@plot_bp.route("/api/plot3d", methods=["GET"])
def api_plot_3d_stock_prices():
    stock_symbol = request.args.get("symbol", default=None)
    if not stock_symbol:
        return jsonify({"error": "Please provide a stock symbol."}), 400

    start_date = request.args.get("start", "2000-01-01")
    end_date = request.args.get("end", "2022-01-01")

    stock_data = StockData.query.filter_by(symbol=stock_symbol).filter(
        StockData.date.between(start_date, end_date)
    ).order_by(StockData.date.asc()).all()

    if not stock_data:
        return jsonify({"error": f"No data found for '{stock_symbol}'."}), 404

    data = pd.DataFrame([{
        "date": record.date,
        "price": record.price,
        "pct_change": record.pct_change,
        "rolling_mean": record.rolling_mean,
        "rolling_std": record.rolling_std
    } for record in stock_data])

    trace = go.Scatter3d(
        x=data["pct_change"],
        y=data["rolling_mean"],
        z=data["rolling_std"],
        mode='markers',
        marker=dict(size=5, color=data["price"], colorscale='Viridis', opacity=0.8)
    )

    layout = go.Layout(
        title=f'{stock_symbol} 3D Stock Price Features',
        scene=dict(
            xaxis_title='Pct Change',
            yaxis_title='Rolling Mean',
            zaxis_title='Rolling Std'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Convert plot to JSON instead of an image
    plot_json = fig.to_json()

    return jsonify({"symbol": stock_symbol, "plot_data": plot_json})

@plot_bp.route('/explore')
def explore():
    return render_template('explore.html')
