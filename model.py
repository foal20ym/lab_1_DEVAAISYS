"""Tiny deterministic Iris classifier for the introductory lab."""
from functools import lru_cache
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


@lru_cache(maxsize=1)
def get_model():
    iris = load_iris()
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, random_state=42))
    model.fit(iris.data, iris.target)
    return model, list(iris.target_names)


def predict_species(measurements):
    """Predict an Iris species from four measurements in centimeters."""
    if not isinstance(measurements, (list, tuple)) or len(measurements) != 4:
        raise ValueError("Exactly four measurements are required.")
    try:
        values = [float(item) for item in measurements]
    except (TypeError, ValueError) as exc:
        raise ValueError("Measurements must be numbers.") from exc
    if any(not (0 < value < 100) for value in values):
        raise ValueError("Measurements must be between 0 and 100 (exclusive).")
    model, names = get_model()
    return names[int(model.predict([values])[0])]
