from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_BASE_URL = "https://api.quieromac.com/agendas"

def api_request(method, endpoint, json_data=None):
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        headers = {'Content-Type': 'application/json', 'accept': '*/*'}
        response = requests.request(method, url, headers=headers, json=json_data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": str(e)}

@app.route('/sellers/', methods=['GET', 'POST'])
def sellers():
    if request.method == 'POST':
        data = request.json
        result = api_request('POST', 'sellers/', json_data=data)
        return jsonify(result)
    else:
        result = api_request('GET', 'sellers/')
        print(result)  # Verificar los datos en la consola
        return jsonify(result)

@app.route('/sellers/update/<int:seller_id>/', methods=['POST'])
def update_seller(seller_id):
    data = request.json
    result = api_request('PUT', f'sellers/{seller_id}/', json_data=data)
    print(result)
    return jsonify(result)

@app.route('/sellers_page')
def sellers_page():
    sellers = api_request('GET', 'sellers/')
    print(sellers)  # Verificar los datos en la consola
    return render_template('sellers.html', sellers=sellers)

if __name__ == '__main__':
    app.run(debug=True)

