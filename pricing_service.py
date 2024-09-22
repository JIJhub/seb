"""
This module provides the pricing service for our application.

It uses Flask to create a web server that handles prediction requests.
"""

from flask import Flask, request, jsonify, redirect
import requests  # pylint: disable=E040
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

PREDICT_API_URL = "http://predict_service:5000/predict_proba"

# Configure Swagger UI blueprint
SWAGGER_URL = "/swagger"
API_URL = "/static/openapi_pricing.yaml"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Simple Pricing Service"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/get_price", methods=["POST"])
def get_price() -> any:
    """
    Calculate prices based on the predicted probability from the
    prediction service.
    The price is determined by the following rules:
        - If probability < 0.25, price = 250
        - If 0.25 <= probability < 0.5, price = 500
        - If 0.5 <= probability < 0.75, price = 750
        - If probability >= 0.75, price = 1000
    """
    try:
        # Get features from the POST request
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Forward the request to the main prediction API
        response = requests.post(PREDICT_API_URL, json=data, timeout=10)

        if response.status_code != 200:
            return jsonify(
                {"error": "Failed to get probabilities from prediction API"}
            ), 500

        probabilities = response.json().get("probabilities", [])

        if not probabilities:
            return jsonify(
                {"error": "No probabilities returned from prediction API"}
            ), 500

        # Calculate prices based on probabilities
        prices = []
        for proba in probabilities:
            if proba < 0.25:
                prices.append(250)
            elif 0.25 <= proba < 0.5:
                prices.append(500)
            elif 0.5 <= proba < 0.75:
                prices.append(750)
            else:
                prices.append(1000)

        return jsonify({"probabilities": probabilities, "prices": prices})

    except Exception as e:  # pylint: disable=W0718
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
    app.run(host="0.0.0.0", port=5001)
