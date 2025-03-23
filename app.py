from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__, template_folder='.')  # Keep template_folder='.' for HTML files

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  items TEXT, 
                  total REAL, 
                  status TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

# Serve existing pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categories.html')
def categories():
    return render_template('categories.html')

@app.route('/cart.html')
def cart():
    return render_template('cart.html')

# Handle order submission
@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    cart = data.get('order')
    total = sum(item['price'] for item in cart)
    items = ', '.join(item['name'] for item in cart)
    
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (items, total, status, timestamp) VALUES (?, ?, ?, ?)",
              (items, total, 'Pending', datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Order placed successfully"}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)