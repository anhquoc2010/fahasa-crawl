from flask import Flask, render_template, request
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/search/", methods=['GET'])
def search():
    q = request.args.get('q') # Lấy tham số q từ URL
    response = requests.get(f'10.5.0.1:5555/products/{q}') # Gọi API để lấy kết quả
    products = response.json() # Chuyển đổi kết quả trả về thành đối tượng Python
    return render_template('product.html', products=products) # Truyền kết quả cho product.html