from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='.')  # Keep template_folder='.' for HTML files

# Redirect root URL to /delivery
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))

# Fetch pending orders
def get_pending_orders():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE status = 'Pending'")
    orders = c.fetchall()
    conn.close()
    return orders

# Serve the dashboard
@app.route('/delivery')
def dashboard():
    return render_template('delivery_dashboard.html')

# API to get orders
@app.route('/get_orders', methods=['GET'])
def get_orders():
    orders = get_pending_orders()
    return jsonify([{"id": o[0], "items": o[1], "total": o[2], "timestamp": o[4]} for o in orders])

# Accept an order
@app.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("UPDATE orders SET status = 'Accepted' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order accepted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)