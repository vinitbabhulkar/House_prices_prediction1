import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained scikit-learn linear regression model
with open('linear-model.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML Template with inline CSS for an attractive UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Price Predictor</title>
    <style>
        :root {
            --primary-color: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }

        .container {
            background-color: var(--card-bg);
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            max-width: 900px;
            width: 100%;
        }

        h1 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 8px;
        }

        p.subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 30px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 18px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-weight: 600;
            margin-bottom: 6px;
            font-size: 0.9rem;
            color: #374151;
        }

        input {
            padding: 10px 14px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 0.95rem;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        .btn-submit {
            grid-column: 1 / -1;
            background-color: var(--primary-color);
            color: white;
            padding: 14px;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 10px;
        }

        .btn-submit:hover {
            background-color: var(--primary-hover);
        }

        .result-box {
            margin-top: 30px;
            padding: 20px;
            background-color: #eef2ff;
            border-left: 5px solid var(--primary-color);
            border-radius: 6px;
            text-align: center;
        }

        .result-box h2 {
            margin: 0 0 5px 0;
            color: var(--primary-color);
        }

        .result-box p {
            margin: 0;
            font-size: 1.5rem;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>House Price Prediction</h1>
    <p class="subtitle">Enter property details below to estimate market value</p>

    <form action="/predict" method="post">
        <div class="form-grid">
            <div class="form-group">
                <label>Bedrooms</label>
                <input type="number" step="any" name="bedrooms" required placeholder="e.g. 3">
            </div>
            <div class="form-group">
                <label>Bathrooms</label>
                <input type="number" step="any" name="bathrooms" required placeholder="e.g. 2">
            </div>
            <div class="form-group">
                <label>Living Area (sq ft)</label>
                <input type="number" step="any" name="living_area" required placeholder="e.g. 2000">
            </div>
            <div class="form-group">
                <label>Lot Area (sq ft)</label>
                <input type="number" step="any" name="lot_area" required placeholder="e.g. 5000">
            </div>
            <div class="form-group">
                <label>Floors</label>
                <input type="number" step="any" name="floors" required placeholder="e.g. 1.5">
            </div>
            <div class="form-group">
                <label>Waterfront Present (0 or 1)</label>
                <input type="number" min="0" max="1" name="waterfront" required placeholder="0 = No, 1 = Yes">
            </div>
            <div class="form-group">
                <label>Number of Views</label>
                <input type="number" step="any" name="views" required placeholder="e.g. 0">
            </div>
            <div class="form-group">
                <label>Condition Rating</label>
                <input type="number" step="any" name="condition" required placeholder="e.g. 3">
            </div>
            <div class="form-group">
                <label>Grade Rating</label>
                <input type="number" step="any" name="grade" required placeholder="e.g. 7">
            </div>
            <div class="form-group">
                <label>Area Above Basement (sq ft)</label>
                <input type="number" step="any" name="area_above" required placeholder="e.g. 1500">
            </div>
            <div class="form-group">
                <label>Basement Area (sq ft)</label>
                <input type="number" step="any" name="area_basement" required placeholder="e.g. 500">
            </div>
            <div class="form-group">
                <label>Built Year</label>
                <input type="number" name="built_year" required placeholder="e.g. 1995">
            </div>
            <div class="form-group">
                <label>Renovation Year</label>
                <input type="number" name="renovation_year" required placeholder="0 if never renovated">
            </div>
            <div class="form-group">
                <label>Lot Area Renovated</label>
                <input type="number" step="any" name="lot_area_renov" required placeholder="e.g. 5000">
            </div>
            <div class="form-group">
                <label>Schools Nearby</label>
                <input type="number" name="schools_nearby" required placeholder="e.g. 2">
            </div>
            <div class="form-group">
                <label>Distance to Airport (km)</label>
                <input type="number" step="any" name="airport_dist" required placeholder="e.g. 15.2">
            </div>

            <button type="submit" class="btn-submit">Predict House Price</button>
        </div>
    </form>

    {% if prediction_text %}
    <div class="result-box">
        <h2>Estimated Value</h2>
        <p>{{ prediction_text }}</p>
    </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract values in the exact feature order expected by the model
    features = [
        float(request.form['bedrooms']),
        float(request.form['bathrooms']),
        float(request.form['living_area']),
        float(request.form['lot_area']),
        float(request.form['floors']),
        float(request.form['waterfront']),
        float(request.form['views']),
        float(request.form['condition']),
        float(request.form['grade']),
        float(request.form['area_above']),
        float(request.form['area_basement']),
        float(request.form['built_year']),
        float(request.form['renovation_year']),
        float(request.form['lot_area_renov']),
        float(request.form['schools_nearby']),
        float(request.form['airport_dist'])
    ]
    
    input_data = np.array([features])
    prediction = model.predict(input_data)[0]
    
    formatted_prediction = f"${prediction:,.2f}"
    
    return render_template_string(HTML_TEMPLATE, prediction_text=formatted_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
