"""Flask UI and JSON API for a tiny ML classification app."""
from flask import Flask, jsonify, render_template_string, request
from model import predict_species

app = Flask(__name__, static_folder="images", static_url_path="/images")

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Iris Predictor</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 580px; margin: 3rem auto;
           padding: 0 1rem; background: #f5f7fb; color: #1d2939; }
    main { background: white; border-radius: 14px; padding: 2rem;
           box-shadow: 0 4px 22px #0001; }
    label { display: block; margin-top: 1rem; }
    input { width: 100%; box-sizing: border-box; padding: .65rem; margin-top: .3rem; }
    button { background: #2358b8; color: white; padding: .8rem 1.2rem; border: 0;
             border-radius: 7px; margin-top: 1.2rem; cursor: pointer; }
    #result { margin-top: 1.2rem; font-weight: 600; }
    #species-image { display: block; max-width: 100%; height: auto; margin-top: 1rem; }
  </style>
</head>
<body>
<main>
  <h1>Iris species predictor</h1>
  <p>Enter four flower measurements (cm) to test the ML model.</p>
  <form id="prediction-form">
    <label>Sepal length <input name="sepal_length" type="number" step="any" value="5.1" required></label>
    <label>Sepal width <input name="sepal_width" type="number" step="any" value="3.5" required></label>
    <label>Petal length <input name="petal_length" type="number" step="any" value="1.4" required></label>
    <label>Petal width <input name="petal_width" type="number" step="any" value="0.2" required></label>
    <button type="submit">Predict</button>
  </form>
  <p id="result" role="status"></p>
  <img id="species-image" alt="" hidden>
</main>
<script>
  const speciesImages = {
    setosa: 'iris_setosa.jpg',
    versicolor: 'Iris_versicolor.jpg',
    virginica: 'Iris_virginica.jpg'
  };

  document.getElementById('prediction-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const values = [...event.target.elements]
      .filter(element => element.tagName === 'INPUT')
      .map(element => Number(element.value));
    const result = document.getElementById('result');
    try {
      const response = await fetch('/predict', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ measurements: values })
      });
      const data = await response.json();
      result.textContent = response.ok ? `Prediction: ${data.species}` : `Error: ${data.error}`;
      const image = document.getElementById('species-image');
      const imagePath = response.ok ? speciesImages[data.species] : undefined;
      if (imagePath) {
        image.src = `/images/${imagePath}`;
        image.alt = `An image of ${data.species}`;
        image.hidden = false;
      } else {
        image.hidden = true;
        image.removeAttribute('src');
        image.alt = '';
      }
    } catch (error) {
      result.textContent = 'Error: could not contact the server.';
      const image = document.getElementById('species-image');
      image.hidden = true;
      image.removeAttribute('src');
      image.alt = '';
    }
  });
</script>
</body>
</html>"""


@app.get("/")
def index():
    return render_template_string(PAGE)


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object."), 400
    try:
        species = predict_species(payload.get("measurements"))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(species=species)


if __name__ == "__main__":
    app.run(debug=True)
