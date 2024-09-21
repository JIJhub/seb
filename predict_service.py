from flask import Flask, request, jsonify, redirect
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.datasets import make_classification
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configure Swagger UI blueprint
SWAGGER_URL = "/swagger"
API_URL = "/static/openapi_predict.yaml"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Simple prediction service"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# This part is greatly simplified. In a real-world scenario,
# a model is typically generated in a training repository,
# versioned alongside training data, and stored in a system
# like MLflow, where metrics are tracked.
# The model is then loaded into the application for inference.


def generate_sample_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a sample dataset for binary classification.

    This function creates a synthetic dataset with 1000 samples,
    each having 2 features. The dataset consists of 2 informative
    features and no redundant features.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - X (np.ndarray): The feature matrix of shape (1000, 2).
            - y (np.ndarray): The target vector of shape (1000,).
    """
    X, y = make_classification(
        n_samples=1000,
        n_features=2,
        n_classes=2,
        n_informative=2,
        n_redundant=0
    )
    return X, y


def train_model() -> RandomForestClassifier:
    """
    Trains a Random Forest classifier using generated sample data.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    X, y = generate_sample_data()
    model = RandomForestClassifier()
    model.fit(X, y)
    return model


trained_model = train_model()


@app.route("/predict_proba", methods=["POST"])
def predict_proba() -> any:
    """
    Predict probabilities for the positive class based on input features.

    This endpoint receives a JSON object containing a 2D array of
    features and returns the predicted probabilities for the
    positive class.

    Returns:
        Response: A JSON response containing the predicted
        probabilities or an error message.
    """
    try:
        data = request.get_json()
        if not data or "features" not in data:
            return jsonify({"error": "Invalid input"}), 400

        input_features = np.array(data["features"])

        if len(input_features.shape) != 2:
            return jsonify(
                {"error": "Input features should be a 2D array"}
            ), 400

        if input_features.shape[1] != trained_model.n_features_in_:
            return jsonify({"error": "Incorrect number of features"}), 400

        proba = trained_model.predict_proba(input_features)[:, 1]
        return jsonify({"probabilities": proba.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index() -> any:
    """
    Redirect to the Swagger UI documentation.

    This endpoint serves as the home page and redirects users
    to the Swagger UI for API documentation.

    Returns:
        Response: A redirect response to the Swagger UI URL.
    """
    return redirect(f"{SWAGGER_URL}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
