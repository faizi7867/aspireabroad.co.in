
import sys
import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

from documents.models import Document
from students.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

def test_validators():
    print("--- Testing Model Validators ---")
    
    # Create dummy user
    user, created = User.objects.get_or_create(username='test_validator_user', defaults={'email': 'test@example.com'})
    
    # 1. Test Document Validator (Should accept PDF)
    print("\n1. Testing Document model with PDF...")
    doc = Document(
        student=user,
        document_type='ADDITIONAL',
        title='Test PDF',
        file=SimpleUploadedFile("test.pdf", b"dummy content", content_type="application/pdf")
    )
    try:
        doc.full_clean()
        print("SUCCESS: Document accepted PDF.")
    except ValidationError as e:
        print(f"FAILURE: Document rejected PDF: {e}")

    # 2. Test Document Validator (Should reject EXE)
    print("\n2. Testing Document model with EXE (invalid)...")
    doc_invalid = Document(
        student=user,
        document_type='ADDITIONAL',
        title='Test EXE',
        file=SimpleUploadedFile("test.exe", b"dummy content", content_type="application/x-msdownload")
    )
    try:
        doc_invalid.full_clean()
        print("FAILURE: Document accepted EXE (Should have rejected).")
    except ValidationError as e:
        print(f"SUCCESS: Document rejected EXE as expected: {e}")

    # 3. Test StudentProfile Validator (Should reject PDF)
    print("\n3. Testing StudentProfile model with PDF (invalid for photo)...")
    # Ensure profile exists or create dummy
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    
    profile.photo = SimpleUploadedFile("test.pdf", b"dummy pdf content", content_type="application/pdf")
    
    try:
        profile.full_clean()
        print("FAILURE: StudentProfile accepted PDF for photo (Should have rejected).")
    except ValidationError as e:
        print(f"SUCCESS: StudentProfile rejected PDF as expected: {e}")

if __name__ == "__main__":
    test_validators()
