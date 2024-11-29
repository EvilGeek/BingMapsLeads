import json
from flask import Flask, render_template, request, jsonify
import requests
from bing import _search, extract_listings

app = Flask(__name__)

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the lead search
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    html = _search(query)
    if html:
        listings = extract_listings(html)
        return jsonify(listings)
    else:
        return jsonify({'error': 'Failed to retrieve data from Bing Maps'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
