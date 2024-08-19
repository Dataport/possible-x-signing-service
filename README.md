# Normalization-URDNA2015

This project provides a simple Flask-based API for normalizing, hashing, and signing Verifiable Credential (VC) documents. The API supports two main operations: normalizing and hashing a VC document, and signing a VC document with a private key.

## Features
- **Normalization & Hashing**: Normalize JSON-LD documents using the URDNA2015 algorithm and generate a SHA-256 hash.
- **Signing**: Sign Verifiable Credential documents using a private key and return the signed document.
- **Error Handling**: Handles bad requests, missing data, and internal server errors with appropriate HTTP status codes and error messages.
- **Logging**: Integrated logging using Python's `logging` module for better traceability of operations and errors.

## Endpoints

### `POST /normalize/urdna2015`
Normalizes a JSON-LD document using the URDNA2015 algorithm and returns a SHA-256 hash of the normalized document.

#### Request Body
```json
{
  "document": { 
    // Your JSON-LD document here 
  }
}
```

#### Response
- **Success (201)**:
  ```json
  {
    "message": "VC document successfully normalized and hashed!",
    "data": "<SHA256 hash>"
  }
  ```
- **Invalid JSON Data (400)**:
  ```json
  {
    "error": "Invalid JSON data",
    "message": "<Error details>"
  }
  ```
- **Missing Data (400)**:
  ```json
  {
    "error": "Missing data",
    "message": "<Error details>"
  }
  ```
- **Internal Server Error (500)**:
  ```json
  {
    "error": "Internal Server Error",
    "message": "<Error details>"
  }
  ```

### `POST /sign`
Signs a Verifiable Credential (VC) document with a private key and returns the signed VC.

#### Request Body
```json
{
  "document": { 
    // Your VC document here 
  },
  "verification_method": "Verification Method URI"
}
```

#### Response
- **Success (201)**:
  ```json
  {
    "message": "VC document successfully signed",
    "data": "<Signed VC document>"
  }
  ```
- **Internal Server Error (500)**:
  ```json
  {
    "error": "Internal Server Error",
    "message": "<Error details>"
  }
  ```

### Error Handling
- **404 Page Not Found**: Returns a `404` response when an endpoint is not found.
  ```json
  {
    "error": "Page not found!"
  }
  ```

## Setup and Installation

### Prerequisites
- Docker

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://gitlab.fokus.fraunhofer.de/possible/normalization-urdna2015.git
   cd normalization-urdna2015
   ```

2. **Add a Private Key**:
    Add an RSA private key in a `privkey.pem` file in the root folder or set the raw key via the environment variable `FLASK_PRIVATE_KEY`

3. **Build the Docker Image**:
   ```bash
    docker build -t normalization-urdna2015 .
    ```

4. **Build the Docker Container**:
   ```bash
    docker run -d -p PORT:2021 --name normalization-urdna2015 normalization-urdna2015
    ```
    This command starts the container and maps port PORT on your local machine to port 8080 in the container.

5. **Access the Application**:
    Open your browser and navigate to http://localhost:PORT. The application will be accessible at this address.

## Project Structure

- **`server.py`**: The main Flask application file containing the API endpoints and core logic.
- **`utils.py`**: Utility functions for JSON-LD normalization, SHA-256 hashing, and document signing.
- **`privkey.pem`**: The private key file used for signing Verifiable Credential documents. 