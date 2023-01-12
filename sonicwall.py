from fastapi import FastAPI
from pydantic import BaseModel
import pyodbc
import re

class sonicwallContent(BaseModel):
    subject: str
    body: str

app = FastAPI()

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.1.103;'
                      'Database=graphAPI;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

@app.get("/")
def helloworld():
    return "hello world"


@app.post("/sonicwall")
def sonicwall(requestBody: sonicwallContent):
    subject = requestBody.subject
    phishing= None
    malware= None
    securityEvent = None
    if 'phishing' in subject.lower():
        phishing = True
    elif 'malware' in subject.lower():
        malware = True
    elif 'security' in subject.lower():
        securityEvent = True
    body = requestBody.body
    body = re.sub('\n', '', body)
    cursor.execute("""INSERT INTO sonicwall_counter
                          (
                          subject,
                          body,
                          phishing,
                          malware,
                          securityEvent
                          )
                    VALUES (?,?,?,?,?)""", (subject, body, phishing, malware, securityEvent))
    conn.commit()
    return {"status":"success"}

