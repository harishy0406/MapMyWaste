from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def extract_gps_from_image(image_path):
    """
    Extract GPS coordinates from image EXIF data.
    Returns tuple (latitude, longitude) if found, else (None, None)
    """
    try:
        if not os.path.exists(image_path):
            return None, None
        
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if exif_data is None:
            return None, None
        
        # Find GPS info
        gps_info = None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'GPSInfo':
                gps_info = value
                break
        
        if gps_info is None:
            return None, None
        
        # Extract GPS coordinates
        gps_data = {}
        for tag_id, value in gps_info.items():
            tag = GPSTAGS.get(tag_id, tag_id)
            gps_data[tag] = value
        
        # Convert to decimal degrees
        lat = None
        lon = None
        
        if 'GPSLatitude' in gps_data and 'GPSLatitudeRef' in gps_data:
            lat = _convert_to_degrees(gps_data['GPSLatitude'])
            if gps_data['GPSLatitudeRef'] != 'N':
                lat = -lat
        
        if 'GPSLongitude' in gps_data and 'GPSLongitudeRef' in gps_data:
            lon = _convert_to_degrees(gps_data['GPSLongitude'])
            if gps_data['GPSLongitudeRef'] != 'E':
                lon = -lon
        
        if lat is not None and lon is not None:
            return lat, lon
        
        return None, None
    
    except Exception as e:
        print(f"Error extracting GPS from image: {e}")
        return None, None


def _convert_to_degrees(value):
    """Convert GPS coordinate to decimal degrees"""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

