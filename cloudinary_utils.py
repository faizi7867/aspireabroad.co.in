
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

def upload_file_to_cloudinary(file_obj, filename, folder="manual_uploads"):
    """
    Upload a file to Cloudinary with correct resource_type handling.
    
    Args:
        file_obj: The file object to upload (e.g., from request.FILES)
        filename: The desired filename on Cloudinary
        folder: The folder to upload to
        
    Returns:
        dict: The result from Cloudinary API
    """
    # Determine resource_type based on extension
    if filename.lower().endswith('.pdf'):
        resource_type = 'raw'
    else:
        resource_type = 'auto'  # Let Cloudinary decide for images/videos
        
    try:
        result = cloudinary.uploader.upload(
            file_obj,
            public_id=filename,
            folder=folder,
            resource_type=resource_type,
            use_filename=True,
            unique_filename=False,
            overwrite=True
        )
        return result
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None

def get_download_url(public_id, resource_type='auto'):
    """
    Get a download URL for a Cloudinary resource.
    """
    url, options = cloudinary_url(public_id, resource_type=resource_type)
    return url
