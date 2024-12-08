from pillow_heif import register_heif_opener
from vision_agent.tools import load_image, owl_v2_image, ocr

register_heif_opener()


def find_vegetables_and_prices(image_path, box_threshold: float = 0.1):
    # Load the image
    image = load_image(image_path)
    
    # Detect vegetables
    vegetables = owl_v2_image("brussels sprouts, tomatoes, cucumber, lettuce, squash", image, box_threshold=box_threshold)
    
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
            #<ALEX>
            # if veg_name not in results:
            #     results[veg_name] = []
            # results[veg_name].append(closest_price)
            #</ALEX>
            #<ALEX>
            results[veg_name] = closest_price
            #</ALEX>

    # Convert results to JSON
    # return json.dumps(results, indent=2)

    #<ALEX>
    results = {
        veg: price.split("/")[0].strip()
        for veg, price in results.items()
    }
    #</ALEX>
    return results

# The function can be called with the image path
# result = find_vegetables_and_prices('/path/to/image.png')
#<ALEX>
# result = find_vegetables_and_prices('/Users/alexsherstinsky/Development/VisionAgent/alex_workspace_test_0/SafewayFlyer11142024as0.png')
# print(result)
#</ALEX>
