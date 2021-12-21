"""
This file contains two lists:
    1. List of all the extensions/types of any image, so only those images will be downloaded which are in this list.
       Add or remove items as needed.
    2. Contains the two image tags attributes which contain image url 'src' and 'srcset'.
"""

SUPPORTED_IMAGE_TYPES = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico", ".eps", ".psd"]
SUPPORTED_IMAGE_ATTRIBUTES = ["src", "srcset"]