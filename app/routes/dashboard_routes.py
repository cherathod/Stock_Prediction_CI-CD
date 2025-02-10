from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/options-trading')
def options_trading():
    return render_template('options_trading.html')
