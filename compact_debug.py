import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()
from django.conf import settings

print(f"KEY: '{config('CLOUDINARY_CLOUD_NAME', default='MISSING')}'")
print(f"STORAGE: {settings.DEFAULT_FILE_STORAGE}")
