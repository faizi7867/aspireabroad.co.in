import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbbs_visa.settings')
django.setup()

from students.models import StudentProfile
from documents.models import Document

def check_media():
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print("-" * 30)
    
    print("Checking Student Profiles:")
    for profile in StudentProfile.objects.all():
        if profile.photo:
            print(f"User: {profile.user.username}")
            print(f"  Field: {profile.photo}")
            print(f"  URL: {profile.photo.url}")
            try:
                path = profile.photo.path
                exists = os.path.exists(path)
                print(f"  Path: {path} [{'EXISTS' if exists else 'MISSING'}]")
            except Exception as e:
                print(f"  Error getting path: {e}")
        else:
            print(f"User: {profile.user.username} - No photo")

    print("-" * 30)
    print("Checking Documents:")
    for doc in Document.objects.all():
        if doc.file:
            print(f"Doc: {doc.filename()}")
            print(f"  Field: {doc.file}")
            print(f"  URL: {doc.file.url}")
            try:
                path = doc.file.path
                exists = os.path.exists(path)
                print(f"  Path: {path} [{'EXISTS' if exists else 'MISSING'}]")
            except Exception as e:
                print(f"  Error getting path: {e}")

if __name__ == "__main__":
    check_media()
