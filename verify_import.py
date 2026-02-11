
import sys
import os
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

print("Attempting to import documents.views...")
try:
    import documents.views
    print("SUCCESS: documents.views imported successfully.")
except Exception as e:
    print(f"FAILURE: Could not import documents.views: {e}")
    sys.exit(1)
