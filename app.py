import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load CSV safely
try:
    stock_esf_df = pd.read_csv('data/Bloomberg_cleaned.csv')
    print("✅ CSV loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load CSV: {e}")
    stock_esf_df = pd.DataFrame()

@app.route('/api/stock')
def get_stock():
    ticker = request.args.get('ticker')
    print(f"📥 Received request for ticker: {ticker}")

    try:
        if stock_esf_df.empty:
            return jsonify({'error': 'CSV failed to load'}), 500

        # Filter by ticker
        filtered_data = stock_esf_df[stock_esf_df['Ticker'] == ticker]

        if filtered_data.empty:
            print("⚠️ No data found for ticker.")
            return jsonify({'error': 'Ticker not found'}), 404

        # Convert filtered data
        stock_prices = filtered_data[['Year', 'Price at beginning of year']].to_dict(orient='records')
        esg_scores = filtered_data[['Year', 'ESG_Score', 'Enviornmental_Score', 'Governance_Score', 'Social_Score']].to_dict(orient='records')

        # Dummy predictions for now
        prediction = {
            '1_year': {'change': 0.10, 'confidence': 0.85},
            '3_year': {'change': 0.30, 'confidence': 0.78},
            '5_year': {'change': 0.50, 'confidence': 0.70}
        }

        return jsonify({
            'stock_prices': stock_prices,
            'esg_scores': esg_scores,
            'prediction': prediction
        })

    except Exception as e:
        print("❌ Internal server error:")
        traceback.print_exc()  # <-- prints full error details
        return jsonify({'error': 'internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
