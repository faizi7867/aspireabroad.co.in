import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

from accounts.notifications import send_email

def test_otp_send():
    print("Testing send_email from accounts.notifications...")
    # Using the email from the original .env as a likely valid recipient
    to_email = "aspire.abroadwithus@gmail.com" 
    subject = "Verify your email - Aspire Abroad Debug"
    body = "Your verification code is: 123456"
    
    print(f"Attempting to send to {to_email}...")
    success = send_email(to_email, subject, body)
    
    if success:
        print("SUCCESS: Email sent.")
    else:
        print("FAILURE: Email not sent.")

if __name__ == '__main__':
    test_otp_send()
