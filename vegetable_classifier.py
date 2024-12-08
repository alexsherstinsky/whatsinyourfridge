#<ALEX>
from collections import defaultdict
#</ALEX>
from pillow_heif import register_heif_opener
from vision_agent.tools import load_image, owl_v2_image, overlay_bounding_boxes

register_heif_opener()


def identify_vegetables(image_path, box_threshold: float = 0.1):
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
    detections = owl_v2_image(prompt, image, box_threshold=box_threshold)

    # Initialize a dictionary to store vegetable counts
    #<ALEX>
    # vegetable_counts = {veg: 0 for veg in vegetable_types}
    #</ALEX>
    #<ALEX>
    vegetable_counts = defaultdict(lambda: 0)
    #</ALEX>

    # Count vegetables
    for detection in detections:
        # print(f'Detected: {detection["label"]} ; score: {detection["score"]}')
        if detection['score'] >= box_threshold:
            vegetable_counts[detection['label']] += 1

    #<ALEX>
    vegetable_counts = dict(vegetable_counts)
    detected_vegetable_types = set(vegetable_counts.keys())
    if detected_vegetable_types != set(vegetable_types):
        raise ValueError("List of vegetables detected is inconsistent with the prompt.")
    #</ALEX>

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
#<ALEX>
# result = identify_vegetables('/Users/alexsherstinsky/Development/VisionAgent/alex_workspace_test_0/RefrigeratorContents11142024as01.png')
# print(result['vegetable_counts'])
#<ALEX>
#print(result['summary'])
# display(result['image_with_boxes'])
