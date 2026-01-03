import requests
import time
import subprocess
import sys
import os
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

def test_uniqueness():
    # Start the API in a subprocess
    process = subprocess.Popen([sys.executable, "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Starting API server...")
    time.sleep(5)  # Wait for server to start

    try:
        url = "http://127.0.0.1:8000/generate-qr"
        payload = {
            "Batch_ID": "UNIQUE-TEST-001",
            "Product": "Test Product"
        }

        print("Generating QR Code 1...")
        response1 = requests.post(url, json=payload)
        
        print("Generating QR Code 2 (Same Data)...")
        response2 = requests.post(url, json=payload)

        if response1.status_code == 200 and response2.status_code == 200:
            # Decode both QR codes
            img1 = Image.open(BytesIO(response1.content))
            img2 = Image.open(BytesIO(response2.content))
            
            url1 = decode(img1)[0].data.decode("utf-8")
            url2 = decode(img2)[0].data.decode("utf-8")
            
            print(f"URL 1: {url1}")
            print(f"URL 2: {url2}")
            
            if url1 != url2:
                print("Success! URLs are different.")
                if "_uid=" in url1 and "_uid=" in url2:
                    print("Success! URLs contain _uid.")
            else:
                print("Error: URLs are identical!")
                
            # Verify view page does NOT show _uid
            print("Verifying view page...")
            view_response = requests.get(url1)
            if "_uid" not in view_response.text and "UNIQUE-TEST-001" in view_response.text:
                 print("Success! View page shows data but hides _uid.")
            else:
                 print("Error: View page content incorrect.")
                 
        else:
            print("Error: API failed.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Stopping API server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_uniqueness()
