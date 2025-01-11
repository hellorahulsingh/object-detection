import os
import cv2
import numpy as np
from datetime import datetime
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
import svgwrite
from PIL import Image

# Initialize Detectron2 configuration
cfg = get_cfg()
cfg.merge_from_file("detectron2/configs/Misc/cascade_mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.WEIGHTS = "detectron2://Misc/cascade_mask_rcnn_R_50_FPN_3x/144998488/model_final_480dd8.pkl"
cfg.MODEL.DEVICE = "cpu"  # Change to "cuda" if available
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1  # Adjust confidence threshold
cfg.TEST.DETECTIONS_PER_IMAGE = 300  # Increase max detections

# Initialize predictor
predictor = DefaultPredictor(cfg)

# Get input file name from the user
image_path = input("Enter the path to the image file: ").strip()

# Check if the file exists
if not os.path.isfile(image_path):
    print(f"Error: File '{image_path}' does not exist.")
else:
    # Read the image
    img = cv2.imread(image_path)

    # Perform inference
    outputs = predictor(img)
    instances = outputs["instances"].to("cpu")

    # Get bounding boxes and masks
    boxes = instances.pred_boxes if instances.has("pred_boxes") else None
    masks = instances.pred_masks if instances.has("pred_masks") else None

    if boxes is None or masks is None:
        print("No objects detected!")
    else:
        # Create output directory
        output_dir = "processed"
        os.makedirs(output_dir, exist_ok=True)

        # Current date-time for file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.splitext(os.path.basename(image_path))[0]

        # Extract and save objects
        for idx, (box, mask) in enumerate(zip(boxes, masks)):
            x1, y1, x2, y2 = map(int, box.tolist())  # Convert box coordinates to integers

            # Crop the mask and convert to NumPy array
            cropped_mask = mask[y1:y2, x1:x2].numpy().astype(np.uint8)

            # Crop the object
            cropped_obj = img[y1:y2, x1:x2]

            # Apply the mask to make the background transparent in PNG
            cropped_obj_rgba = cv2.cvtColor(cropped_obj, cv2.COLOR_BGR2BGRA)
            cropped_obj_rgba[:, :, 3] = cropped_mask * 255  # Set alpha based on mask

            # Save PNG
            png_path = os.path.join(output_dir, f"{base_filename}_{timestamp}_{idx+1}.png")
            Image.fromarray(cropped_obj_rgba).save(png_path)

            # Get contours from the mask
            contours, _ = cv2.findContours(cropped_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Create SVG file
            svg_path = os.path.join(output_dir, f"{base_filename}_{timestamp}_{idx+1}.svg")
            dwg = svgwrite.Drawing(svg_path, size=(x2 - x1, y2 - y1), profile='tiny')

            # Add contours as paths
            for contour in contours:
                # Convert contour points to SVG path
                points = [(point[0][0], point[0][1]) for point in contour]
                path_data = f"M {points[0][0]},{points[0][1]} " + " ".join([f"L {p[0]},{p[1]}" for p in points[1:]]) + " Z"

                # Add the path to the SVG
                dwg.add(dwg.path(d=path_data, fill='black', stroke='none'))

            # Save the SVG file
            dwg.save()

        print(f"Extracted {len(boxes)} objects and saved as PNG and SVG files in '{output_dir}/'.")
