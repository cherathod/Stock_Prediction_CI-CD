from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..models import Order
from .. import db
from datetime import datetime

order_bp = Blueprint("order", __name__)

@order_bp.route("/orders", methods=["GET"])
def view_orders():
    """Display the list of all orders."""
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template("orders.html", orders=orders)

@order_bp.route("/orders/create", methods=["GET", "POST"])
def create_order():
    """Create a new order."""
    if request.method == "POST":
        name = request.form.get("name")
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("quantity"))
        price_per_unit = float(request.form.get("price_per_unit"))
        total = quantity * price_per_unit

        new_order = Order(
            name=name,
            symbol=symbol,
            quantity=quantity,
            total=total,
            status="Pending",
            date=datetime.utcnow()
        )
        db.session.add(new_order)
        db.session.commit()

        flash("Order created successfully!", "success")
        return redirect(url_for("order.view_orders"))

    return render_template("create_order.html")

@order_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def delete_order(order_id):
    """Delete an existing order."""
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash("Order deleted successfully!", "success")
    return redirect(url_for("order.view_orders"))

@order_bp.route("/orders/<int:order_id>/update", methods=["GET", "POST"])
def update_order(order_id):
    """Update the details of an existing order."""
    order = Order.query.get_or_404(order_id)

    if request.method == "POST":
        order.name = request.form.get("name")
        order.symbol = request.form.get("symbol")
        order.quantity = int(request.form.get("quantity"))
        price_per_unit = float(request.form.get("price_per_unit"))
        order.total = order.quantity * price_per_unit
        order.status = request.form.get("status")
        db.session.commit()
        flash("Order updated successfully!", "success")
        return redirect(url_for("order.view_orders"))

    return render_template("update_order.html", order=order)

@order_bp.route("/orders/api", methods=["GET"])
def orders_api():
    """API to retrieve all orders as JSON."""
    orders = Order.query.all()
    orders_list = [
        {
            "id": order.id,
            "name": order.name,
            "symbol": order.symbol,
            "quantity": order.quantity,
            "total": order.total,
            "status": order.status,
            "date": order.date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for order in orders
    ]
    return jsonify(orders_list)
