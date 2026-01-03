from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
import qrcode
from io import BytesIO
import urllib.parse
import uuid

app = FastAPI(
    title="QR Code Generator API",
    description="API to generate QR codes that link to a batch details page with dynamic fields.",
    version="3.0.0"
)

# Mount static files for logo
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/view", response_class=HTMLResponse, summary="View Batch Details")
async def view_batch(request: Request):
    """
    Renders a web page with the batch details.
    Accepts arbitrary query parameters.
    """
    # Extract all query parameters into a dictionary
    data = dict(request.query_params)
    
    # Remove the unique identifier used for QR uniqueness
    data.pop('_uid', None)
    
    return templates.TemplateResponse(
        "view_batch.html",
        {
            "request": request,
            "data": data
        }
    )

@app.post("/generate-qr", summary="Generate QR Code for Web View", responses={200: {"content": {"image/png": {}}}})
async def generate_qr(request: Request, details: Dict[str, Any]):
    """
    Generates a QR code containing a URL to the /view page with the provided details.
    Accepts any JSON object (key-value pairs).
    """
    try:
        # Construct the URL
        base_url = str(request.base_url).rstrip("/")
        
        # Convert all values to strings for the query string
        params = {k: str(v) for k, v in details.items()}
        
        # Add a unique identifier to ensure the URL (and thus the QR code) is unique
        # even if the data is identical.
        params['_uid'] = str(uuid.uuid4())
            
        query_string = urllib.parse.urlencode(params)
        view_url = f"{base_url}/view?{query_string}"
        
        print(f"Generated URL: {view_url}")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(view_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save image to bytes
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return Response(content=img_byte_arr.getvalue(), media_type="image/png")

    except Exception as e:
        print(f"Error generating QR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Host on 0.0.0.0 to be accessible from other devices
    uvicorn.run(app, host="0.0.0.0", port=8000)
