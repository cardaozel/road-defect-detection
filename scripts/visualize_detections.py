#!/usr/bin/env python3
"""Visualize detection results with confidence percentages displayed under images."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize YOLOv8 detections with confidence percentages."
    )
    parser.add_argument(
        "--weights",
        default="results/yolov8n_rdd2022/weights/best.pt",
        help="Path to trained weights (best.pt).",
    )
    parser.add_argument(
        "--source",
        default="data/yolo/images/val",
        help="Image source (directory, single image, or glob pattern).",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="runs/detections",
        help="Directory to save annotated images.",
    )
    parser.add_argument(
        "--imgsz", type=int, default=640, help="Inference image size."
    )
    parser.add_argument(
        "--conf", type=float, default=0.25, help="Confidence threshold."
    )
    parser.add_argument(
        "--device",
        help="Device for inference (auto-detected if not set).",
    )
    parser.add_argument(
        "--num-images",
        dest="num_images",
        type=int,
        default=5,
        help="Number of images to process (if source is a directory).",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable debug logging."
    )
    return parser.parse_args()


def auto_detect_device() -> str:
    """Automatically detect the best available device for inference."""
    import torch

    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def get_image_paths(source: str, num_images: int) -> List[Path]:
    """Get list of image paths from source."""
    source_path = Path(source)
    
    if source_path.is_file():
        # Single image
        return [source_path]
    elif source_path.is_dir():
        # Directory - get all images
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
        image_paths = [
            p for p in source_path.rglob("*") 
            if p.suffix.lower() in image_extensions
        ]
        # Sort and limit
        image_paths.sort()
        return image_paths[:num_images]
    else:
        # Glob pattern
        image_paths = list(Path(".").glob(source))
        image_paths.sort()
        return image_paths[:num_images]


def draw_detections_with_percentages(
    image: np.ndarray,
    results,
    conf_threshold: float = 0.25,
) -> Tuple[np.ndarray, List[str]]:
    """Draw bounding boxes with labels and collect confidence percentages.
    
    Returns:
        Annotated image and list of confidence strings for display under image.
    """
    annotator = Annotator(image, line_width=2)
    confidence_info = []
    
    # Get class names
    class_names = results.names
    
    # Process detections
    boxes = results.boxes
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            # Get class and confidence
            cls = int(box.cls[0].cpu().numpy())
            conf = float(box.conf[0].cpu().numpy())
            
            # Only draw if confidence is above threshold
            if conf >= conf_threshold:
                class_name = class_names[cls]
                confidence_pct = conf * 100
                
                # Create label with class name and confidence
                label = f"{class_name} {confidence_pct:.1f}%"
                
                # Draw bounding box and label
                annotator.box_label(
                    [x1, y1, x2, y2],
                    label=label,
                    color=colors(cls, True),
                )
                
                # Add to confidence info list
                confidence_info.append(f"{class_name}: {confidence_pct:.1f}%")
    
    annotated_image = annotator.result()
    return annotated_image, confidence_info


def add_confidence_text_below_image(
    image: np.ndarray,
    confidence_info: List[str],
    font_scale: float = 0.6,
    thickness: int = 2,
) -> np.ndarray:
    """Add confidence percentages as text below the image.
    
    Creates additional space below the image and writes confidence info.
    """
    h, w = image.shape[:2]
    
    # Calculate text size to determine padding needed
    font = cv2.FONT_HERSHEY_SIMPLEX
    line_height = int(30 * font_scale)
    padding = 40  # Base padding
    
    if confidence_info:
        # Add padding for text (1 line per detection + title)
        padding = max(padding, (len(confidence_info) + 2) * line_height + 20)
    
    # Create new image with padding
    new_h = h + padding
    result_image = np.ones((new_h, w, 3), dtype=np.uint8) * 255  # White background
    result_image[:h, :w] = image
    
    # Draw text
    y_offset = h + line_height
    text_color = (0, 0, 0)  # Black text
    
    if confidence_info:
        # Title
        cv2.putText(
            result_image,
            "Detections:",
            (10, y_offset),
            font,
            font_scale,
            (50, 50, 50),
            thickness,
        )
        y_offset += int(line_height * 1.5)
        
        # Confidence percentages
        for conf_text in confidence_info:
            cv2.putText(
                result_image,
                f"  {conf_text}",
                (10, y_offset),
                font,
                font_scale,
                text_color,
                thickness,
            )
            y_offset += line_height
    else:
        # No detections
        cv2.putText(
            result_image,
            "No detections found",
            (10, y_offset),
            font,
            font_scale,
            (128, 128, 128),
            thickness,
        )
    
    return result_image


def process_image(
    model: YOLO,
    image_path: Path,
    output_path: Path,
    conf_threshold: float,
    imgsz: int,
    device: str,
) -> None:
    """Process a single image and save annotated result."""
    logging.info("Processing: %s", image_path.name)
    
    # Run inference
    results = model.predict(
        source=str(image_path),
        imgsz=imgsz,
        conf=conf_threshold,
        device=device,
        verbose=False,
    )[0]  # Get first (and only) result
    
    # Load original image
    image = cv2.imread(str(image_path))
    if image is None:
        logging.error("Failed to load image: %s", image_path)
        return
    
    # Draw detections
    annotated_image, confidence_info = draw_detections_with_percentages(
        image, results, conf_threshold
    )
    
    # Add confidence text below image
    final_image = add_confidence_text_below_image(annotated_image, confidence_info)
    
    # Save result
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), final_image)
    
    # Log summary
    if confidence_info:
        logging.info(
            "  Found %d detection(s): %s",
            len(confidence_info),
            ", ".join(confidence_info),
        )
    else:
        logging.info("  No detections found")


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)
    
    # Load model
    weights_path = Path(args.weights).expanduser().resolve()
    if not weights_path.exists():
        logging.error("Weights file not found: %s", weights_path)
        return 1
    
    logging.info("Loading model from: %s", weights_path)
    model = YOLO(str(weights_path))
    
    # Auto-detect device if not specified
    device = args.device or auto_detect_device()
    logging.info("Using device: %s", device)
    
    # Get image paths
    image_paths = get_image_paths(args.source, args.num_images)
    if not image_paths:
        logging.error("No images found in source: %s", args.source)
        return 1
    
    logging.info("Found %d image(s) to process", len(image_paths))
    
    # Process each image
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for image_path in image_paths:
        # Create output filename (preserve original name)
        output_filename = f"detected_{image_path.stem}.jpg"
        output_path = output_dir / output_filename
        
        process_image(
            model,
            image_path,
            output_path,
            args.conf,
            args.imgsz,
            device,
        )
    
    logging.info("=" * 80)
    logging.info("Detection visualization complete!")
    logging.info("Output directory: %s", output_dir)
    logging.info("Processed %d image(s)", len(image_paths))
    logging.info("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
