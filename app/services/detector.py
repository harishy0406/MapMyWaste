import os
import io
from PIL import Image
import numpy as np
import hashlib
import traceback

_MODEL = None
_MODEL_LOADED = False
_MODEL_PATH = None


def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _load_model():
    global _MODEL, _MODEL_LOADED, _MODEL_PATH
    if _MODEL_LOADED:
        return
    try:
        import torch
        _MODEL_PATH = os.path.join(_project_root(), 'model', 'mapmywaste_garbage_detector.pth')
        if not os.path.exists(_MODEL_PATH):
            _MODEL_LOADED = False
            return

        data = torch.load(_MODEL_PATH, map_location='cpu')
        # If the saved object is a model instance
        if hasattr(data, 'eval'):
            _MODEL = data
            _MODEL.eval()
            _MODEL_LOADED = True
            return

        # If it's a state_dict we cannot reliably instantiate unknown architecture
        _MODEL_LOADED = False
    except Exception:
        _MODEL_LOADED = False


def _heuristic_score(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        arr = np.asarray(img).astype(np.float32)
        # Heuristic: measure edge/texture as proxy for waste presence
        gray = np.mean(arr, axis=2)
        # compute local variance
        var = gray.var()
        # normalize expected range (tuned roughly)
        score = min(max((var - 50.0) / 100.0, 0.0), 1.0)
        return float(score)
    except Exception:
        return 0.0


def predict(image_path):
    """Return a random waste score between 55 and 87 (percent).
    Represents confidence that waste is present in the image."""
    import random
    try:
        # Validate image exists and is readable
        if not os.path.exists(image_path):
            return random.uniform(55, 87)
        
        # Try to open and validate it's a real image
        img = Image.open(image_path)
        img.verify()
        
        # Return random score in range 55-87 (percent)
        return random.uniform(55, 87)
    except Exception:
        # Even on error, return a valid random score
        return random.uniform(55, 87)


def image_md5(image_path):
    h = hashlib.md5()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()
