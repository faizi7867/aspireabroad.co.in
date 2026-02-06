import os
import django
from django.conf import settings
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

def debug_settings():
    print("--- Settings Debug ---")
    print(f"CLOUDINARY_CLOUD_NAME (env): '{config('CLOUDINARY_CLOUD_NAME', default='MISSING')}'")
    
    print(f"settings.MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"settings.MEDIA_URL: {settings.MEDIA_URL}")
    print(f"settings.DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    if hasattr(settings, 'CLOUDINARY_STORAGE'):
        print(f"settings.CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
    else:
        print("settings.CLOUDINARY_STORAGE: NOT FOUND")

    # Test instantiation
    from django.core.files.storage import get_storage_class
    cls = get_storage_class()
    print(f"Storage Class: {cls}")
    
if __name__ == "__main__":
    debug_settings()
