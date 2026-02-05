import os
import django
from django.conf import settings
import resend

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

def debug_resend():
    print("--- Detailed Resend Debug ---")
    api_key = settings.RESEND_API_KEY
    print(f"API Key present: {bool(api_key)}")
    if api_key:
        print(f"API Key prefix: {api_key[:4]}...")
    
    resend.api_key = api_key
    
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = "aspire.abroadwithus@gmail.com"
    
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    
    params = {
        "from": from_email,
        "to": [to_email],
        "subject": "Resend Debug Test",
        "html": "<p>Test email</p>"
    }
    
    try:
        print("Sending...")
        r = resend.Emails.send(params)
        print("Response:", r)
    except Exception as e:
        print("ERROR OCCURRED:")
        print(e)

if __name__ == "__main__":
    debug_resend()
