#!/usr/bin/env python3
"""
Test the trained model on validation images and save detection results.
"""

import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

def test_model_detections(model_path, image_dir, output_dir, num_images=5, conf_threshold=0.25):
    """Test model on images and save detection results."""
    
    # Load model
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)
    
    # Get image files
    image_dir = Path(image_dir)
    image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
    
    if not image_files:
        print(f"❌ No images found in {image_dir}")
        return
    
    # Select random images
    import random
    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Class names
    class_names = ['D00', 'D01', 'D10', 'D11', 'D20', 'D40']
    colors = [
        (255, 0, 0),    # Red - D00
        (0, 255, 0),    # Green - D01
        (0, 0, 255),    # Blue - D10
        (255, 255, 0),  # Yellow - D11
        (255, 0, 255),  # Magenta - D20
        (0, 255, 255),  # Cyan - D40
    ]
    
    print(f"\nTesting on {len(selected_images)} images...")
    
    for i, img_path in enumerate(selected_images, 1):
        print(f"Processing {i}/{len(selected_images)}: {img_path.name}")
        
        # Run inference
        results = model.predict(str(img_path), conf=conf_threshold, imgsz=640)
        
        # Load image
        img = cv2.imread(str(img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Draw detections
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # Get class and confidence
                cls = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                
                # Get color
                color = colors[cls % len(colors)]
                
                # Draw bounding box
                cv2.rectangle(img_rgb, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_names[cls]}: {conf:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(img_rgb, (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), color, -1)
                cv2.putText(img_rgb, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Save result
        output_path = output_dir / f"detection_{img_path.stem}.png"
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), img_bgr)
        print(f"  ✅ Saved: {output_path}")
    
    print(f"\n✅ Detection results saved to {output_dir}/")

if __name__ == "__main__":
    model_path = sys.argv[1] if len(sys.argv) > 1 else "results/yolov8s_rdd2022_high_perf/weights/best.pt"
    image_dir = sys.argv[2] if len(sys.argv) > 2 else "data/yolo/rdd2022/val/images"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "results/yolov8s_rdd2022_high_perf/detection_samples"
    num_images = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    
    test_model_detections(model_path, image_dir, output_dir, num_images)

