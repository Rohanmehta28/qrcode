# Easy Deployment & Integration Guide

This guide explains how to put your QR Code Generator on the internet for **FREE** and how to connect it to your manufacturing software.

## Part 1: How to Deploy for Free (Using Render)

We will use a service called **Render**. It has a free tier that is perfect for this.

### Step 1: Put your code on GitHub
1.  Create a new repository on [GitHub](https://github.com).
2.  Upload all the files in this folder (`main.py`, `requirements.txt`, `static/`, `templates/`, etc.) to that repository.

### Step 2: Create a Web Service on Render
1.  Go to [render.com](https://render.com) and sign up (you can use your GitHub account).
2.  Click **"New +"** and select **"Web Service"**.
3.  Connect your GitHub repository.
4.  Fill in these details:
    -   **Name**: `my-qr-api` (or whatever you like)
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    -   **Instance Type**: Select **"Free"**.
5.  Click **"Create Web Service"**.

Wait a few minutes. Render will give you a URL like:
`https://my-qr-api.onrender.com`

**That's it! Your API is now online.**

---

## Part 2: How to Call the API from Your Software

Your software team needs to send data to your new URL.

### The Logic
1.  Your software collects data (Batch ID, Supervisor, etc.).
2.  It bundles this data into a **JSON** (a simple data format).
3.  It sends this JSON to your API.
4.  Your API sends back a **QR Code image**.
5.  Your software prints that image.

### Example Code (Python)
Give this snippet to your software team. They can adapt it to whatever language they use (Java, C#, etc.).

```python
import requests
import time

# 1. The URL of your deployed API
api_url = "https://my-qr-api.onrender.com/generate-qr"

# 2. Your Data (Define ANY fields you want here)
my_data = {
    "Batch_ID": "BATCH-2024-001",
    "Product": "Super Widget",
    "Supervisor": "Rohan Mehta",
    "Shift": "Morning",
    "Location": "Plant A",
    "Expiry_Date": "2025-12-31"
}

# 3. Send the data
response = requests.post(api_url, json=my_data)

# 4. Save the QR Code image
if response.status_code == 200:
    # Use Batch ID + Timestamp to ensure unique filenames
    timestamp = int(time.time())
    filename = f"label_{my_data['Batch_ID']}_{timestamp}.png"
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Success! Label saved as {filename}")
else:
    print("Error:", response.text)
```

### Key Features
-   **Dynamic Fields**: Notice `my_data` above? You can add *any* key-value pair you want. You don't need to change the API code. If you add `"Temperature": "45C"`, it will automatically appear on the web page when scanned.
-   **Automatic Linking**: The QR code generated will automatically link to a web page hosted on your API that displays all these details nicely.
