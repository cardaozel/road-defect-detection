#!/usr/bin/env python3
"""
Convert the raw RDD2022 dataset into YOLO-friendly train/val/test splits.

The script expects the dataset extracted with the same folder hierarchy as the
official release, where each region (e.g., India_Drone, Japan) contains an
`annotations/xmls` directory and an `images` directory.
"""

from __future__ import annotations

import argparse
import logging
import random
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

CLASS_NAMES = ["D00", "D01", "D10", "D11", "D20", "D40"]
CLASS_TO_ID: Dict[str, int] = {name: idx for idx, name in enumerate(CLASS_NAMES)}


@dataclass
class Annotation:
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def find_image(file_stem: str, search_dir: Path) -> Optional[Path]:
    """Try to locate the corresponding image file for a VOC annotation."""
    # Ensure search_dir is absolute
    search_dir = search_dir.resolve()
    
    extensions = [".jpg", ".jpeg", ".png"]
    
    # Try multiple search strategies based on common RDD2022 directory structures
    # Structure 1: annotations/xmls/ -> images/ (same level as annotations)
    # Structure 2: train/annotations/xmls/ -> train/images/
    # Structure 3: region/train/annotations/xmls/ -> region/train/images/
    
    search_paths = [
        search_dir,  # Same directory as XML
        search_dir / "images",  # images subdirectory
        search_dir.parent / "images",  # images sibling to annotations
        search_dir.parent.parent / "images",  # images at train level
        search_dir.parent.parent.parent / "images",  # images at region level
    ]
    
    # Also try going up to find train/ or similar split directories
    current = search_dir
    for _ in range(4):  # Go up max 4 levels
        if current.name in ["train", "val", "test"]:
            search_paths.append(current / "images")
        current = current.parent
    
    # Remove duplicates while preserving order
    seen = set()
    unique_paths = []
    for path in search_paths:
        path_resolved = path.resolve()
        if path_resolved not in seen:
            seen.add(path_resolved)
            unique_paths.append(path_resolved)
    
    for ext in extensions:
        for search_path in unique_paths:
            candidate = search_path / f"{file_stem}{ext}"
            if candidate.exists():
                return candidate

    return None


def voc_to_yolo(box: Dict[str, int], img_w: int, img_h: int) -> Annotation:
    x_min, y_min, x_max, y_max = box["xmin"], box["ymin"], box["xmax"], box["ymax"]
    x_center = ((x_min + x_max) / 2.0) / img_w
    y_center = ((y_min + y_max) / 2.0) / img_h
    width = (x_max - x_min) / img_w
    height = (y_max - y_min) / img_h
    return Annotation(
        class_id=box["class_id"],
        x_center=x_center,
        y_center=y_center,
        width=width,
        height=height,
    )


def parse_voc(xml_file: Path) -> Optional[Dict]:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find("size")
    if size is None:
        logging.warning("Missing size tag in %s", xml_file)
        return None

    width = int(size.findtext("width", default="0"))
    height = int(size.findtext("height", default="0"))
    filename = root.findtext("filename")
    if not filename:
        filename = xml_file.stem + ".jpg"

    boxes: List[Annotation] = []
    for obj in root.findall("object"):
        label = obj.findtext("name", default="").strip()
        if label not in CLASS_TO_ID:
            logging.debug("Skipping unknown class %s in %s", label, xml_file)
            continue
        bbox = obj.find("bndbox")
        if bbox is None:
            continue
        coords = {
            "xmin": int(float(bbox.findtext("xmin", default="0"))),
            "ymin": int(float(bbox.findtext("ymin", default="0"))),
            "xmax": int(float(bbox.findtext("xmax", default="0"))),
            "ymax": int(float(bbox.findtext("ymax", default="0"))),
            "class_id": CLASS_TO_ID[label],
        }
        boxes.append(voc_to_yolo(coords, width, height))

    if not boxes:
        return None

    return {"filename": filename, "annotations": boxes, "width": width, "height": height}


def extract_region_zips(raw_dir: Path, force: bool = False) -> Path:
    """Extract region ZIP files if they exist."""
    extracted_dir = raw_dir / "extracted"
    
    # Check if already extracted
    if extracted_dir.exists() and not force:
        logging.info("Region ZIPs already extracted to %s", extracted_dir)
        return extracted_dir
    
    # Find all ZIP files in the raw directory
    zip_files = list(raw_dir.rglob("*.zip"))
    if not zip_files:
        # Check if there's a nested RDD2022 directory
        nested_dir = raw_dir / "RDD2022"
        if nested_dir.exists():
            zip_files = list(nested_dir.glob("*.zip"))
            if zip_files:
                logging.info("Found %d region ZIP files in nested directory", len(zip_files))
    
    if not zip_files:
        logging.warning("No ZIP files found. Assuming dataset is already extracted.")
        return raw_dir
    
    extracted_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Extracting %d region ZIP files to %s", len(zip_files), extracted_dir)
    
    for zip_file in zip_files:
        logging.info("Extracting %s", zip_file.name)
        try:
            with zipfile.ZipFile(zip_file, "r") as zf:
                zf.extractall(extracted_dir)
        except Exception as e:
            logging.error("Failed to extract %s: %s", zip_file, e)
            continue
    
    logging.info("Extraction complete. Looking for annotations in %s", extracted_dir)
    return extracted_dir


def collect_annotations(annotation_dir: Path) -> List[Dict]:
    # Ensure annotation_dir is absolute
    annotation_dir = annotation_dir.resolve()
    xml_files = sorted(annotation_dir.rglob("*.xml"))
    logging.info("Found %d annotation files under %s", len(xml_files), annotation_dir)
    samples: List[Dict] = []
    missing_count = 0
    for xml_file in xml_files:
        # Ensure xml_file is absolute
        xml_file = xml_file.resolve()
        parsed = parse_voc(xml_file)
        if not parsed:
            continue
        file_stem = Path(parsed["filename"]).stem
        image_path = find_image(file_stem, xml_file.parent)
        if not image_path:
            missing_count += 1
            if missing_count <= 5:  # Only log first few for debugging
                logging.warning("Image for %s not found (stem: %s); skipping", xml_file, file_stem)
            elif missing_count == 6:
                logging.warning("... (suppressing further missing image warnings)")
            continue
        samples.append({"image": image_path, "annotations": parsed["annotations"]})
    if missing_count > 0:
        logging.warning("Total missing images: %d out of %d XML files", missing_count, len(xml_files))
    logging.info("Collected %d samples with bounding boxes", len(samples))
    return samples


def split_dataset(
    samples: Sequence[Dict],
    train_ratio: float,
    val_ratio: float,
    seed: int,
) -> Dict[str, List[Dict]]:
    if train_ratio + val_ratio >= 1.0:
        raise ValueError("train_ratio + val_ratio must be < 1.0 to leave room for test split.")

    samples = list(samples)
    random.Random(seed).shuffle(samples)

    total = len(samples)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    return {
        "train": samples[:train_end],
        "val": samples[train_end:val_end],
        "test": samples[val_end:],
    }


def write_split(split_name: str, records: Iterable[Dict], target_dir: Path) -> None:
    image_dir = target_dir / "images" / split_name
    label_dir = target_dir / "labels" / split_name
    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    for record in records:
        src_image = record["image"]
        dst_image = image_dir / src_image.name
        shutil.copy2(src_image, dst_image)

        label_path = label_dir / f"{src_image.stem}.txt"
        with open(label_path, "w", encoding="utf-8") as f:
            for ann in record["annotations"]:
                f.write(
                    f"{ann.class_id} {ann.x_center:.6f} {ann.y_center:.6f} "
                    f"{ann.width:.6f} {ann.height:.6f}\n"
                )


def write_data_yaml(target_dir: Path, dataset_root: Path) -> None:
    yaml_content = (
        f"path: {target_dir}\n"
        f"train: images/train\n"
        f"val: images/val\n"
        f"test: images/test\n"
        f"nc: {len(CLASS_NAMES)}\n"
        f"names: {CLASS_NAMES}\n"
    )
    data_yaml = dataset_root / "rdd2022.yaml"
    data_yaml.write_text(yaml_content, encoding="utf-8")
    logging.info("Saved YOLO data config to %s", data_yaml)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_raw = project_root / "data" / "raw" / "RDD2022"
    default_output = project_root / "data" / "yolo"

    parser = argparse.ArgumentParser(description="Prepare RDD2022 for YOLO training.")
    parser.add_argument("--raw-dir", default=str(default_raw), help="Path to extracted RDD2022 root directory.")
    parser.add_argument("--output-dir", default=str(default_output), help="Destination directory for YOLO files.")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train split ratio.")
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation split ratio.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling.")
    parser.add_argument("--extract-zips", action="store_true", help="Extract region ZIP files if found.")
    parser.add_argument("--force-extract", action="store_true", help="Force re-extraction of ZIP files.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    configure_logger(args.verbose)

    raw_dir = Path(args.raw_dir).expanduser().resolve()
    if not raw_dir.exists():
        logging.error("Raw dataset directory %s does not exist. Run download script first.", raw_dir)
        return 1

    # Extract ZIP files if needed
    if args.extract_zips or list(raw_dir.rglob("*.zip")):
        annotation_dir = extract_region_zips(raw_dir, force=args.force_extract)
    else:
        annotation_dir = raw_dir
    
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = collect_annotations(annotation_dir)
    if not samples:
        logging.error("No annotations found under %s", annotation_dir)
        return 1

    splits = split_dataset(samples, args.train_ratio, args.val_ratio, args.seed)
    for split_name, records in splits.items():
        logging.info("Writing %s split with %d samples", split_name, len(records))
        write_split(split_name, records, output_dir)

    write_data_yaml(output_dir, output_dir)
    logging.info("Dataset preparation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

