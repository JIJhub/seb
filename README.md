# Very simple Pricing Engine
This project is a simple pricing engine based on two Docker APIs that communicate with each other.

- The `predict_service` returns a probability given a set of features.
- The `pricing_service` calls the `predict_service` with a specific set of 
  features and receives a prediction in return, which is then used to generate a price.

The programming language is Python (version 3.12), and the APIs are based on Flask and uWSGI. 
uWSGI is used to handle varying amounts of traffic and to enable configuration
changes, such as not using root privileges.

## Features

- Endpoint to predict probabilities based on input features.
- Endpoint to predict prices based on input features.
- Swagger UI for interactive API documentation and testing.
- Containerized using Docker
- Built with uWSGI for safety and performance.

## Requirements

- **Docker**: To build and run the application in a container.
- **Docker Compose** : For easier management of multi-container applications.

### Python Packages

The application requires the following Python packages:

- Flask==3.0.3
- scikit-learn==1.5.2
- pandas==2.2.2
- flask_swagger_ui==4.11.1
- uWSGI==2.0.26
- Jinja2==3.1.4
- requests==2.32.3

These dependencies are listed in the `requirements.txt` file.

## Folder Structure
```plaintext
project-root/
│   README.md
│   Dockerfile.lint
│   Dockerfile.predict
│   Dockerfile.pricing
│   docker-compose.yml
│   pricing_service.py
│   predict_service.py
│   requirements.txt
└── static/
    ├── openapi.predict.yaml
    └── openapi_pricing.yaml
└── .github/
    └── workflows/
        └── ci_check.yml
```

## Running Linting and Vulnerability Checks

When you push to GitHub, automatic linting tests using Pylint 
will be performed, along with a safety check for vulnerabilities.

## Usage prediction service
```bash
docker build -f Dockerfile.predict -t predict_image .
docker run -p 5000:5000 predict_image
```
To make predictions, send a request to the 
/predict_proba endpoint with a JSON body containing the input features.
```json
{
  "features": [[1.0, 2.0], [3.0, 4.0]]
}
```
### Example using `curl`

Use `curl` to test the API:

```bash
curl -X POST http://localhost:5000/predict_proba -H \
"Content-Type: application/json" -d '{"features": [[1.0, 2.0], [3.0, 4.0]]}'
```
## Usage pricing service
```bash
docker-compose up --build
docker-compose down
```

## API Documentation
The API documentation is available via Swagger UI and can be 
used for sending requests. You can access it by navigating to:

- **Predict Service**: [http://localhost:5000/swagger](http://localhost:5000/swagger)
- **Pricing Service**: [http://localhost:5001/swagger](http://localhost:5001/swagger)

## What's Missing
- **User Authentication and Authorization**: Verifying user identity and 
setting access credentials is not implemented.
- **Configuration Files**: There are no dedicated configuration files for 
environment settings.
- **Tests**: The project currently lacks unit and integration tests to ensure 
functionality and reliability.
- **Type Checking** Add mypy to ci checks
- **Monitoring/Logging/Health**, **Message queue**, **...**