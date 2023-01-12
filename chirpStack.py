from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import base64

class chirpstackRequest(BaseModel):
    deduplicationId: str
    time: str
    deviceInfo: dict
    devAddr: str
    dr: str
    fCnt: str
    fPort: str
    data: str
    rxInfo: list
    txInfo: dict


app = FastAPI()

@app.get("/")
def helloworld():
    return "hello world"


@app.post("/chirpstack")
def chirpstack(event:str, requestBody: chirpstackRequest):
    print(requestBody)
    if event == 'up':
        print('battery')
    base64_message = requestBody.data
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    data = message_bytes.decode('ascii')
    devAddr = requestBody.devAddr
    devEui = requestBody.deviceInfo['devEui']
    print(event, data,devAddr,devEui)