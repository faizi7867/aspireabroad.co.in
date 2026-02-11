
import sys
import os
import django
from django.conf import settings
from django.core.files.base import ContentFile

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage

def run_test():
    output = []
    output.append("--- Cloudinary PDF Verification ---")
    
    try:
        # 1. Test RawMediaCloudinaryStorage
        storage = RawMediaCloudinaryStorage()
        filename = "verify_raw.pdf"
        content = b"%PDF-1.4 TEST CONTENT"
        
        output.append(f"Uploading {filename} using RawMediaCloudinaryStorage...")
        
        # Check if exists and delete
        try:
            if storage.exists(filename):
                storage.delete(filename)
        except Exception as ignored:
            pass
            
        saved_path = storage.save(filename, ContentFile(content))
        output.append(f"Saved path: {saved_path}")
        
        url = storage.url(saved_path)
        output.append(f"URL: {url}")
        
        if "/raw/upload" in url:
             output.append("VERDICT: RawMediaCloudinaryStorage uses resource_type='raw'. CORRECT for PDFs.")
        else:
             output.append(f"VERDICT: RawMediaCloudinaryStorage generated URL: {url}")

    except Exception as e:
        output.append(f"ERROR: {str(e)}")
        import traceback
        output.append(traceback.format_exc())

    # Write results to file
    with open("verification_result.txt", "w") as f:
        f.write("\n".join(output))
    
    print("\n".join(output))

if __name__ == "__main__":
    run_test()
