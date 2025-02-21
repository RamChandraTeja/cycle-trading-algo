from flask import Flask, request, jsonify
from flask_cors import CORS  # For handling CORS in development
import json
from your_stock_analysis_module import stock_analysis  # Assuming this is your module with stock analysis functions

app = Flask(__name__)
CORS(app)  # This will enable CORS, which is necessary when your frontend is served from a different origin

@app.route('/api/stock_analysis', methods=['POST'])
def analyze_stock():
    data = request.json
    symbol = data.get('symbol')
    stock_api_key = data.get('stock_api_key')
    news_api_key = data.get('news_api_key')
    
    if not all([symbol, stock_api_key, news_api_key]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    result = stock_analysis(symbol, stock_api_key, news_api_key)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Analysis failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)