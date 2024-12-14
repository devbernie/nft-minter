# utils.py
import re
import requests

def convert_metadata_to_hex(metadata):
    """
    Convert metadata dictionary to hex format for blockchain submission.

    :param metadata: Metadata dictionary
    :return: Hex-encoded metadata string
    """
    import json
    return json.dumps(metadata).encode("utf-8").hex()

def parse_asset_name(asset_name):
    """
    Convert human-readable asset name to hex-encoded format.

    :param asset_name: Human-readable asset name
    :return: Hex-encoded asset name
    """
    return asset_name.encode("utf-8").hex()

def validate_image_url(image_url):
    """
    Validate the image URL.

    :param image_url: URL of the image for the NFT
    :return: True if valid, otherwise raise ValueError
    """
    valid_domains = [
        "drive.google.com",
        "onedrive.live.com",
        "dropbox.com",
        "imgur.com"
    ]

    # Check if the URL is from a valid domain
    if not any(domain in image_url for domain in valid_domains):
        raise ValueError("Image URL must be from Google Drive, OneDrive, Dropbox, or Imgur.")

    # Handle platform-specific URL adjustments
    if "drive.google.com" in image_url:
        match = re.search(r'/file/d/([^/]+)/', image_url)
        if match:
            file_id = match.group(1)
            image_url = f"https://drive.google.com/uc?id={file_id}"
    elif "dropbox.com" in image_url:
        image_url = image_url.replace("?dl=0", "?dl=1")
    elif "onedrive.live.com" in image_url:
        image_url += "&download=1"
    elif "imgur.com" in image_url:
        # Ensure Imgur URLs point directly to an image file
        if not re.search(r'\.(jpg|jpeg|png|gif|bmp|webp)$', image_url, re.IGNORECASE):
            raise ValueError("Imgur URL must point directly to an image file.")

    # Check if the URL points to an image by inspecting the content type
    try:
        response = requests.head(image_url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise ValueError("The URL does not point to a valid image file.")
    except requests.RequestException as e:
        raise ValueError(f"Failed to verify image URL: {e}")

    return True