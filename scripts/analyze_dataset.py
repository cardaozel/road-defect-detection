#!/usr/bin/env python3
"""Analyze RDD2022 dataset for quality issues, class imbalance, and annotation problems."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
import yaml
from PIL import Image


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze RDD2022 dataset for issues.")
    parser.add_argument("--data-yaml", dest="data_yaml", default="data/yolo/rdd2022.yaml", help="Path to data YAML.")
    parser.add_argument("--output", default="results/dataset_analysis.json", help="Output JSON file.")
    parser.add_argument("--split", choices=["train", "val", "test", "all"], default="all", help="Split to analyze.")
    parser.add_argument("--check-images", dest="check_images", action="store_true", help="Verify image files exist.")
    parser.add_argument("--check-annotations", dest="check_annotations", action="store_true", help="Verify annotation files.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def parse_yolo_label(label_path: Path) -> List[Dict]:
    """Parse YOLO format label file."""
    annotations = []
    
    if not label_path.exists():
        return annotations
    
    try:
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                    
                    # Convert normalized coords to pixel coords (need image size)
                    annotations.append({
                        "class_id": class_id,
                        "x_center": x_center,
                        "y_center": y_center,
                        "width": width,
                        "height": height,
                    })
    except Exception as e:
        logging.warning("Error parsing label file %s: %s", label_path, e)
    
    return annotations


def analyze_split(
    images_dir: Path,
    labels_dir: Path,
    check_images: bool,
    check_annotations: bool,
) -> Dict:
    """Analyze a dataset split."""
    stats = {
        "total_images": 0,
        "total_annotations": 0,
        "images_with_annotations": 0,
        "images_without_annotations": 0,
        "class_distribution": Counter(),
        "bbox_statistics": {
            "areas": [],
            "widths": [],
            "heights": [],
            "aspect_ratios": [],
        },
        "issues": {
            "missing_images": [],
            "missing_labels": [],
            "invalid_annotations": [],
            "empty_images": [],
        },
        "image_statistics": {
            "widths": [],
            "heights": [],
            "aspect_ratios": [],
        },
    }
    
    # Get all image files
    image_extensions = {".jpg", ".jpeg", ".png"}
    image_files = [f for f in images_dir.iterdir() if f.suffix.lower() in image_extensions]
    stats["total_images"] = len(image_files)
    
    logging.info("Analyzing %d images...", len(image_files))
    
    for img_file in image_files:
        label_file = labels_dir / f"{img_file.stem}.txt"
        
        # Check if image exists and is valid
        if check_images:
            try:
                img = Image.open(img_file)
                width, height = img.size
                stats["image_statistics"]["widths"].append(width)
                stats["image_statistics"]["heights"].append(height)
                stats["image_statistics"]["aspect_ratios"].append(width / height if height > 0 else 0)
            except Exception as e:
                stats["issues"]["missing_images"].append(str(img_file))
                logging.warning("Invalid image: %s - %s", img_file, e)
                continue
        
        # Check if label file exists
        annotations = []
        if label_file.exists():
            annotations = parse_yolo_label(label_file)
            
            if annotations:
                stats["images_with_annotations"] += 1
                stats["total_annotations"] += len(annotations)
                
                # Analyze annotations
                for ann in annotations:
                    stats["class_distribution"][ann["class_id"]] += 1
                    
                    # Calculate bbox statistics (normalized)
                    area = ann["width"] * ann["height"]
                    stats["bbox_statistics"]["areas"].append(area)
                    stats["bbox_statistics"]["widths"].append(ann["width"])
                    stats["bbox_statistics"]["heights"].append(ann["height"])
                    stats["bbox_statistics"]["aspect_ratios"].append(
                        ann["width"] / ann["height"] if ann["height"] > 0 else 0
                    )
            else:
                stats["images_without_annotations"] += 1
        else:
            stats["images_without_annotations"] += 1
            if check_annotations:
                stats["issues"]["missing_labels"].append(str(img_file))
    
    # Calculate statistics
    def calc_stats(values: List[float]) -> Dict:
        if not values:
            return {}
        arr = np.array(values)
        return {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "median": float(np.median(arr)),
        }
    
    stats["bbox_statistics"] = {
        k: calc_stats(v) for k, v in stats["bbox_statistics"].items()
    }
    stats["image_statistics"] = {
        k: calc_stats(v) for k, v in stats["image_statistics"].items()
    }
    
    # Convert Counter to dict
    stats["class_distribution"] = dict(stats["class_distribution"])
    
    return stats


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)
    
    # Load data config
    data_yaml_path = Path(args.data_yaml).expanduser().resolve()
    if not data_yaml_path.exists():
        logging.error("Data YAML not found: %s", data_yaml_path)
        return 1
    
    with open(data_yaml_path, "r") as f:
        data_cfg = yaml.safe_load(f)
    
    base_dir = data_yaml_path.parent
    class_names = data_cfg.get("names", ["D00", "D01", "D10", "D11", "D20", "D40"])
    
    # Analyze splits
    results = {
        "data_yaml": str(data_yaml_path),
        "class_names": class_names,
        "splits": {},
    }
    
    splits_to_analyze = ["train", "val", "test"] if args.split == "all" else [args.split]
    
    for split in splits_to_analyze:
        images_dir = base_dir / "images" / split
        labels_dir = base_dir / "labels" / split
        
        if not images_dir.exists():
            logging.warning("Images directory not found: %s", images_dir)
            continue
        
        if not labels_dir.exists():
            logging.warning("Labels directory not found: %s", labels_dir)
            continue
        
        logging.info("Analyzing %s split...", split)
        split_stats = analyze_split(images_dir, labels_dir, args.check_images, args.check_annotations)
        results["splits"][split] = split_stats
    
    # Overall statistics
    total_images = sum(s["total_images"] for s in results["splits"].values())
    total_annotations = sum(s["total_annotations"] for s in results["splits"].values())
    
    results["summary"] = {
        "total_images": total_images,
        "total_annotations": total_annotations,
        "average_annotations_per_image": total_annotations / total_images if total_images > 0 else 0,
    }
    
    # Save results
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    
    logging.info("=" * 80)
    logging.info("DATASET ANALYSIS RESULTS")
    logging.info("=" * 80)
    logging.info("Total images: %d", total_images)
    logging.info("Total annotations: %d", total_annotations)
    logging.info("Avg annotations per image: %.2f", results["summary"]["average_annotations_per_image"])
    
    for split_name, split_data in results["splits"].items():
        logging.info("\n%s split:", split_name.upper())
        logging.info("  Images: %d", split_data["total_images"])
        logging.info("  Annotations: %d", split_data["total_annotations"])
        logging.info("  Class distribution: %s", dict(split_data["class_distribution"]))
        if split_data["issues"]["missing_images"]:
            logging.warning("  Missing images: %d", len(split_data["issues"]["missing_images"]))
        if split_data["issues"]["missing_labels"]:
            logging.warning("  Missing labels: %d", len(split_data["issues"]["missing_labels"]))
    
    logging.info("=" * 80)
    logging.info("Saved analysis to: %s", output_path)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
