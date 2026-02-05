import os
from decouple import config
import resend

# Manually load env if needed, but decouple does it automatically from .env
print("--- Direct Resend Debug ---")

try:
    api_key = config('RESEND_API_KEY')
    print(f"API Key found via decouple: {bool(api_key)}")
    resend.api_key = api_key
    
    from_email = config('DEFAULT_FROM_EMAIL', default='onboarding@resend.dev')
    to_email = "aspire.abroadwithus@gmail.com"
    
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    
    params = {
        "from": from_email,
        "to": [to_email],
        "subject": "Direct Resend Test",
        "html": "<p>Direct test</p>"
    }
    
    print("Sending...")
    r = resend.Emails.send(params)
    print("Response:", r)

except Exception as e:
    print("ERROR:")
    print(e)
