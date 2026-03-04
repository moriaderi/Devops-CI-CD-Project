from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
import logging
#testing_merge_request
app = Flask(__name__, template_folder='./templates', static_folder='./static')

logging.basicConfig(level=logging.DEBUG)

# הגדרת משתנים עם פרטי ההתחברות
username = "root"
password = "root"
port = 27017

# כתובת ה-URI של MongoDB
uri = f"mongodb://mongo:27017/"

# יצירת חיבור למסד הנתונים
client = MongoClient(uri)
db = client.clothing_store
clothes_collection = db.clothes
sellers_collection = db.sellers
branches_collection = db.branches

@app.route('/')
def home():
    return render_template('about.html')

@app.route('/index')
def index():
    logging.debug('Index route accessed')
    try:
        clothes = list(clothes_collection.find())
        sellers = list(sellers_collection.find())
        branches = list(branches_collection.find())
        logging.debug(f'Clothes: {clothes}')
        logging.debug(f'Sellers: {sellers}')
        logging.debug(f'Branches: {branches}')
        return render_template('index.html', clothes=clothes, sellers=sellers, branches=branches)
    except Exception as e:
        logging.error(f'Error: {e}')
        return str(e), 500

@app.route('/add_clothing', methods=['POST'])
def add_clothing():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        logging.debug(f'Adding clothing: {name}, {price}, {stock}')
        clothes_collection.insert_one({
            'name': name,
            'price': price,
            'stock': stock
        })
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Error: {e}')
        return str(e), 500

@app.route('/add_seller', methods=['POST'])
def add_seller():
    try:
        name = request.form.get('name')
        role = request.form.get('role')
        email = request.form.get('email')
        logging.debug(f'Adding seller: {name}, {role}, {email}')
        sellers_collection.insert_one({
            'name': name,
            'role': role,
            'email': email
        })
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Error: {e}')
        return str(e), 500

@app.route('/add_branch', methods=['POST'])
def add_branch():
    try:
        city = request.form.get('city')
        address = request.form.get('address')
        phone = request.form.get('phone')
        logging.debug(f'Adding branch: {city}, {address}, {phone}')
        branches_collection.insert_one({
            'city': city,
            'address': address,
            'phone': phone
        })
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Error: {e}')
        return str(e), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
