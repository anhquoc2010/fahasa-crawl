from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests, json
app = Flask(__name__)
CORS(app)

API_URL = 'http://127.0.0.1:5555/'

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/search/", methods=['GET'])
def search():
    q = request.args.get('q') # Lấy tham số q từ URL
    response = requests.get(f'{API_URL}/products/{q}') # Gọi API để lấy kết quả
    products = response.json() # Chuyển đổi kết quả trả về thành đối tượng Python
    return render_template('product.html', products=products) # Truyền kết quả cho product.html

@app.route("/product/search/", methods=['GET'])
async def product_search():
    response = requests.get(url=f'{API_URL}/products')
    print(response)
    products = response.json() 
    results = []
    for product in products:
        results.append(product)
    print(results)
    return results


if __name__=="__main__":
    app.run(debug=True)