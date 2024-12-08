import os
import numpy as np
from vision_agent.tools import *
from typing import *
from pillow_heif import register_heif_opener
register_heif_opener()
import vision_agent as va
from vision_agent.tools import register_tool


import json
from vision_agent.tools import load_image, owl_v2_image, ocr

def find_vegetables_and_prices(image_path):
    # Load the image
    image = load_image(image_path)
    
    # Detect vegetables
    vegetables = owl_v2_image("brussels sprouts, tomato, cucumber, lettuce, squash", image, box_threshold=0.2)
    
    # Extract text
    text_data = ocr(image)
    
    # Initialize results dictionary
    results = {}
    
    # Get image dimensions for unnormalization
    height, width = image.shape[:2]
    
    # Process each detected vegetable
    for veg in vegetables:
        veg_name = veg['label']
        veg_center_x = ((veg['bbox'][0] + veg['bbox'][2]) / 2) * width
        veg_center_y = ((veg['bbox'][1] + veg['bbox'][3]) / 2) * height
        
        closest_price = None
        min_distance = float('inf')
        
        # Find the closest price in OCR results
        for text in text_data:
            if '$' in text['label']:
                text_center_x = ((text['bbox'][0] + text['bbox'][2]) / 2) * width
                text_center_y = ((text['bbox'][1] + text['bbox'][3]) / 2) * height
                
                distance = ((veg_center_x - text_center_x) ** 2 + (veg_center_y - text_center_y) ** 2) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_price = text['label']
        
        # Add to results if a price was found
        if closest_price:
            if veg_name not in results:
                results[veg_name] = []
            results[veg_name].append(closest_price)
    
    # Convert results to JSON
    return json.dumps(results, indent=2)

# The function can be called with the image path
# result = find_vegetables_and_prices('/path/to/image.png')
# print(result)
