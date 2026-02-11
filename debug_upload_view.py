
import sys
import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

from documents.forms import DocumentUploadForm
from django.contrib.auth import get_user_model

User = get_user_model()

def reproduce_upload_failure():
    print("--- Reproduction Script: Document Upload View Logic ---")
    
    # Get or create a test user
    user, _ = User.objects.get_or_create(username='debug_user', defaults={'email': 'debug@example.com'})
    print(f"User: {user.username}")

    # Create a dummy PDF file
    pdf_content = b"%PDF-1.4 ... dummy content ..."
    file_data = SimpleUploadedFile("debug_upload_v2.pdf", pdf_content, content_type="application/pdf")
    
    # Simulate POST data (Use a timestamp in title to avoid unique constraint)
    import time
    post_data = {
        'document_type': 'ADDITIONAL',
        'title': f'Debug Upload Title {int(time.time())}'
    }
    file_data_dict = {
        'file': file_data
    }
    
    # Instantiate Form (Exactly as in views.py)
    print("Instantiating DocumentUploadForm...")
    form = DocumentUploadForm(
        data=post_data,
        files=file_data_dict,
        student=user,
        uploaded_by=user
    )
    
    if form.is_valid():
        print("Form is VALID.")
        try:
            print("Attempting to save form...")
            instance = form.save()
            print(f"SUCCESS: Document saved. ID: {instance.id}")
            print(f"File URL: {instance.file.url}")
            
            if "/raw/upload" in instance.file.url:
                print("URL check: CORRECT (Raw resource)")
            else:
                print(f"URL check: SUSPICIOUS -> {instance.file.url}")
                
        except Exception as e:
            print(f"ERROR during save(): {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Form is INVALID.")
        print(f"Errors: {form.errors}")

if __name__ == "__main__":
    reproduce_upload_failure()
