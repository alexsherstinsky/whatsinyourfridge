import os
import numpy as np
from vision_agent.tools import *
from typing import *
from pillow_heif import register_heif_opener
register_heif_opener()
import vision_agent as va
from vision_agent.tools import register_tool


import numpy as np
from vision_agent.tools import load_image, owl_v2_image, overlay_bounding_boxes

def identify_vegetables(image_path):
    try:
        # Load the image
        image = load_image(image_path)
    except FileNotFoundError:
        return {"error": f"Image file not found: {image_path}"}
    except Exception as e:
        return {"error": f"Error loading image: {str(e)}"}
    
    # Define vegetable types to detect
    vegetable_types = ['lettuce', 'carrots', 'tomatoes', 'celery', 'mushrooms', 'green onions']
    prompt = ', '.join(vegetable_types)
    
    # Use owl_v2_image to detect vegetables
    detections = owl_v2_image(prompt, image, box_threshold=0.3)
    
    # Initialize a dictionary to store vegetable counts
    vegetable_counts = {veg: 0 for veg in vegetable_types}
    
    # Count vegetables
    for detection in detections:
        if detection['score'] >= 0.3:
            vegetable_counts[detection['label']] += 1
    
    # Create a summary of findings
    summary = "Vegetables found in the refrigerator:\n"
    for veg, count in vegetable_counts.items():
        if count > 0:
            summary += f"- {veg.capitalize()}: {count}\n"
    
    # Create an image with bounding boxes
    image_with_boxes = overlay_bounding_boxes(image, detections)
    
    return {
        "vegetable_counts": vegetable_counts,
        "summary": summary,
        "image_with_boxes": image_with_boxes
    }

# The function can be called like this:
# result = identify_vegetables('/home/user/gcrgkLJ_RefrigeratorContents11142024as01.png')
# print(result['summary'])
# display(result['image_with_boxes'])
