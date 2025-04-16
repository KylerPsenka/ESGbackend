import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

stock_esf_df = pd.read_csv('data/Bloomberg_cleaned.csv')

@app.route('/api/stock')
def get_stock():
    ticker = request.args.get('ticker')
    stock_esg_data = stock_esf_df[stock_esf_df['Ticker'] == ticker]

    if stock_data.empty or esg_data.empty:
        return jsonify({'error': 'Ticker not found'}), 404

    result = {
        'stock_prices': stock_esf_df[['Year', 'Price at beginning of year']].to_dict(orient='records'),
        'esg_scores': stock_esf_df[['Year', 'ESG_Score', 'Enviornmental_Score', 'Governance_Score', 'Social_Score']].to_dict(orient='records'),
        'prediction': {
            '1_year': {'change': 0.10, 'confidence': 0.85},
            '3_year': {'change': 0.30, 'confidence': 0.78},
            '5_year': {'change': 0.50, 'confidence': 0.70}
        }
    }
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
