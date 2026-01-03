# QR Code Generator API

This is a FastAPI-based API to generate QR codes for manufacturing batches.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the API

1.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    Or simply:
    ```bash
    python run.py
    ```
    This script will print the URL you should use to access the API from your phone (e.g., `http://192.168.x.x:8000`).

2.  **Ensure Connectivity**: Make sure your phone is connected to the **same WiFi network** as your computer.

3.  **Generate & Scan**:
    -   Open the API URL on your computer (e.g., `http://192.168.0.101:8000/docs`).
    -   Use the `POST /generate-qr` endpoint.
    -   Scan the generated QR code with your phone.
    -   It should open the batch details page on your phone.

## Hosting (Production)

To make the API accessible from anywhere (not just your WiFi), you need to host it.

### Option 1: Cloud Hosting (Recommended)
-   **Render / Railway / Heroku**: These platforms allow you to deploy Python apps easily.
    -   Push this code to GitHub.
    -   Connect your repository to Render/Railway.
    -   They will automatically build and host it.
    -   You will get a public URL (e.g., `https://my-qr-api.onrender.com`).

### Option 2: ngrok (Quick Testing)
-   Install `ngrok`.
-   Run `ngrok http 8000`.
-   Use the generated `https://....ngrok-free.app` URL to generate your QR codes.

## Documentation

-   Swagger UI: `http://127.0.0.1:8000/docs` (or your local IP)
-   ReDoc: `http://127.0.0.1:8000/redoc`

## Usage

### Generate QR Code

**Endpoint:** `POST /generate-qr`

**Request Body:**

```json
{
  "Batch_ID": "BATCH-001",
  "Product": "Widget A",
  "Supervisor": "John Doe",
  "Shift": "Night",
  "Any_Other_Field": "Value"
}
```
*Note: You can send ANY key-value pairs you want. They will all be displayed on the page.*

**Response:**
Returns a PNG image of the QR code.
