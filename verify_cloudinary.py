import os
import django
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

def verify_cloudinary():
    print("--- Cloudinary Verification ---")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    file_name = "test_upload.txt"
    content = b"Hello Cloudinary from Render!"
    
    print(f"Attempting to save {file_name}...")
    try:
        if default_storage.exists(file_name):
            default_storage.delete(file_name)
            
        path = default_storage.save(file_name, ContentFile(content))
        print(f"Saved to: {path}")
        
        url = default_storage.url(path)
        print(f"URL: {url}")
        
        if "cloudinary" in url:
            print("SUCCESS: File uploaded to Cloudinary.")
        else:
            print("WARNING: URL does not look like Cloudinary (check settings).")
            
    except Exception as e:
        print("ERROR:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_cloudinary()
