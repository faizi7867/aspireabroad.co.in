
from django.core.files.base import ContentFile
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage

def verify_pdf_upload():
    print("--- PDF Upload Verification ---")
    
    # Test RawMediaCloudinaryStorage
    print("\nTesting RawMediaCloudinaryStorage with PDF content...")
    raw_storage = RawMediaCloudinaryStorage()
    pdf_content = b"%PDF-1.4 ... dummy pdf content ..."
    file_name = "test_doc.pdf"
    
    try:
        if raw_storage.exists(file_name):
            raw_storage.delete(file_name)
            
        path = raw_storage.save(file_name, ContentFile(pdf_content))
        print(f"Saved to: {path}")
        url = raw_storage.url(path)
        print(f"URL: {url}")
        
        # Check if URL indicates raw resource type (usually no formatting/transformations)
        # Cloudinary raw URLs typically look like: .../raw/upload/...
        if "/raw/upload/" in url:
            print("SUCCESS: PDF uploaded as raw resource.")
        else:
            print(f"WARNING: URL does not contain '/raw/upload/'. Check if it works: {url}")

    except Exception as e:
        print(f"ERROR with RawMediaCloudinaryStorage: {e}")
        import traceback
        traceback.print_exc()

    # Test MediaCloudinaryStorage (Expectation: Might allow it but maybe as image?)
    print("\nTesting MediaCloudinaryStorage with PDF content (for comparison)...")
    media_storage = MediaCloudinaryStorage()
    file_name_media = "test_media_doc.pdf"
    
    try:
        if media_storage.exists(file_name_media):
            media_storage.delete(file_name_media)
            
        path = media_storage.save(file_name_media, ContentFile(pdf_content))
        print(f"Saved to: {path}")
        url = media_storage.url(path)
        print(f"URL: {url}")
        
        if "/image/upload/" in url:
            print("INFO: PDF uploaded as image resource (default for MediaCloudinaryStorage).")
        elif "/raw/upload/" in url:
            print("INFO: PDF uploaded as raw resource.")
        else:
            print(f"INFO: URL format: {url}")

    except Exception as e:
        print(f"ERROR with MediaCloudinaryStorage: {e}")

if __name__ == "__main__":
    verify_pdf_upload()
