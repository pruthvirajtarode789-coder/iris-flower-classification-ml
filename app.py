from flask import Flask, request, jsonify, Response
import pickle
import os

# -------------------------------
# App & Model Load
# -------------------------------
app = Flask(__name__)
model = pickle.load(open("iris_model.pkl", "rb"))

# -------------------------------
# Biologically valid ranges
# -------------------------------
sl_min, sl_max = 4.3, 7.9
sw_min, sw_max = 2.0, 4.4
pl_min, pl_max = 1.0, 6.9
pw_min, pw_max = 0.1, 2.5

# -------------------------------
# HTML + CSS + JS
# -------------------------------
HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iris Flower Classification</title>
    <style>
        body {{
            background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
            min-height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .container {{
            background: #fff;
            max-width: 420px;
            margin: 60px auto;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
            padding: 32px 24px;
            text-align: center;
        }}
        h1 {{
            color: #ff6f61;
            margin-bottom: 10px;
        }}
        .hint {{
            font-size: 0.85rem;
            color: #777;
            margin-bottom: 14px;
        }}
        .input-group {{
            margin-bottom: 18px;
            text-align: left;
        }}
        .input-group label {{
            display: block;
            margin-bottom: 6px;
            color: #333;
            font-weight: 500;
        }}
        .input-group input {{
            width: 100%;
            padding: 8px 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 1rem;
        }}
        button {{
            background: linear-gradient(90deg, #ff6f61 0%, #fda085 100%);
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 12px 0;
            width: 100%;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }}
        #result {{
            margin-top: 22px;
            font-size: 1.1rem;
            min-height: 32px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌸 Iris Flower Classification</h1>
        <div class="hint">Enter biologically valid measurements (in cm)</div>

        <form id="iris-form">
            <div class="input-group">
                <label>Sepal Length ({sl_min} – {sl_max})</label>
                <input type="number" step="0.1" min="{sl_min}" max="{sl_max}" name="sl" required>
            </div>

            <div class="input-group">
                <label>Sepal Width ({sw_min} – {sw_max})</label>
                <input type="number" step="0.1" min="{sw_min}" max="{sw_max}" name="sw" required>
            </div>

            <div class="input-group">
                <label>Petal Length ({pl_min} – {pl_max})</label>
                <input type="number" step="0.1" min="{pl_min}" max="{pl_max}" name="pl" required>
            </div>

            <div class="input-group">
                <label>Petal Width ({pw_min} – {pw_max})</label>
                <input type="number" step="0.1" min="{pw_min}" max="{pw_max}" name="pw" required>
            </div>

            <button type="submit">Predict</button>
        </form>

        <div id="result"></div>
    </div>

<script>
document.getElementById('iris-form').addEventListener('submit', async function(e) {{
    e.preventDefault();

    const sl = parseFloat(document.querySelector('input[name="sl"]').value);
    const sw = parseFloat(document.querySelector('input[name="sw"]').value);
    const pl = parseFloat(document.querySelector('input[name="pl"]').value);
    const pw = parseFloat(document.querySelector('input[name="pw"]').value);

    const resultDiv = document.getElementById('result');

    // HARD CLIENT-SIDE VALIDATION
    if (sl < {sl_min} || sl > {sl_max}) {{
        resultDiv.textContent = "❌ Sepal Length must be between {sl_min} and {sl_max} cm";
        resultDiv.style.color = "#d32f2f";
        return;
    }}
    if (sw < {sw_min} || sw > {sw_max}) {{
        resultDiv.textContent = "❌ Sepal Width must be between {sw_min} and {sw_max} cm";
        resultDiv.style.color = "#d32f2f";
        return;
    }}
    if (pl < {pl_min} || pl > {pl_max}) {{
        resultDiv.textContent = "❌ Petal Length must be between {pl_min} and {pl_max} cm";
        resultDiv.style.color = "#d32f2f";
        return;
    }}
    if (pw < {pw_min} || pw > {pw_max}) {{
        resultDiv.textContent = "❌ Petal Width must be between {pw_min} and {pw_max} cm";
        resultDiv.style.color = "#d32f2f";
        return;
    }}

    resultDiv.textContent = "Predicting...";
    resultDiv.style.color = "#333";

    const response = await fetch('/predict', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ sl, sw, pl, pw }})
    }});

    const res = await response.json();
    resultDiv.textContent = res.result;
    resultDiv.style.color = res.result.includes("Iris") ? "#2e7d32" : "#d32f2f";
}});
</script>
</body>
</html>
"""

# -------------------------------
# Routes
# -------------------------------
@app.route("/", methods=["GET"])
def index():
    return Response(HTML, mimetype="text/html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        sl = float(data["sl"])
        sw = float(data["sw"])
        pl = float(data["pl"])
        pw = float(data["pw"])

        # SERVER-SIDE VALIDATION (FINAL SAFETY)
        if not (sl_min <= sl <= sl_max):
            return jsonify({"result": f"❌ Sepal Length must be between {sl_min} and {sl_max} cm"})
        if not (sw_min <= sw <= sw_max):
            return jsonify({"result": f"❌ Sepal Width must be between {sw_min} and {sw_max} cm"})
        if not (pl_min <= pl <= pl_max):
            return jsonify({"result": f"❌ Petal Length must be between {pl_min} and {pl_max} cm"})
        if not (pw_min <= pw <= pw_max):
            return jsonify({"result": f"❌ Petal Width must be between {pw_min} and {pw_max} cm"})

        prediction = model.predict([[sl, sw, pl, pw]])
        return jsonify({"result": f"🌸 Iris Species: {prediction[0]}"})

    except Exception:
        return jsonify({"result": "❌ Invalid input. Please enter correct values."})

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
