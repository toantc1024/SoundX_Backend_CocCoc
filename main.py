from fastapi import FastAPI, File, UploadFile
import base64
import hashlib
import hmac
import os
import time
import requests
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify a list of allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


ACCESS_KEY = "c086deb7c2e2ba3b6e208931b709ccb2"
ACCESS_SECRET = "Gpb7bJ29oypGsnfuCFiM6uYIe4yiTcm9oDHGagYa"
REQ_URL = "https://identify-ap-southeast-1.acrcloud.com/v1/identify"

@app.post("/identify/")
async def identify_audio(file: UploadFile = File(...)):
    print('Processing...',file.filename)
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = f"{http_method}\n{http_uri}\n{ACCESS_KEY}\n{data_type}\n{signature_version}\n{timestamp}"
    sign = base64.b64encode(hmac.new(ACCESS_SECRET.encode('ascii'), string_to_sign.encode('ascii'), hashlib.sha1).digest()).decode('ascii')

    sample_bytes = await file.read()
    files = [('sample', (file.filename, sample_bytes, 'audio/mpeg'))]
    data = {'access_key': ACCESS_KEY,
        'sample_bytes': sample_bytes,
        'timestamp': str(timestamp),
        'signature': sign,
        'data_type': data_type,
        "signature_version": signature_version}

    r = requests.post(REQ_URL, files=files, data=data)
    r.encoding = "utf-8"
    print(r.json())
    return r.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)