import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Add a try/except to load the CSV safely
try:
    stock_esf_df = pd.read_csv('data/Bloomberg(Sheet3).csv')
    print("✅ CSV loaded successfully")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    stock_esf_df = pd.DataFrame()  # prevent crash

@app.route('/api/stock')
def get_stock():
    ticker = request.args.get('ticker')
    print(f"📥 Received request for ticker: {ticker}")

    try:
        stock_data = stock_esf_df[stock_esf_df['Ticker'] == ticker]
        if stock_data.empty:
            print("⚠️ No matching ticker in data")
            return jsonify({'error': 'Ticker not found'}), 404

        result = {
            'stock_prices': stock_data[['Year', 'Price']].to_dict(orient='records'),
            'esg_scores': stock_data[['Year', 'ESG', 'Env', 'Soc', 'Gov']].to_dict(orient='records'),
            'prediction': {
                '1_year': {'change': 0.10, 'confidence': 0.85},
                '3_year': {'change': 0.30, 'confidence': 0.78},
                '5_year': {'change': 0.50, 'confidence': 0.70}
            }
        }

        return jsonify(result)

    except Exception as e:
        print(f"❌ Internal server error: {e}")
        return jsonify({'error': 'internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
