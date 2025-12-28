#!/usr/bin/env python3
"""Export YOLOv8 model to CoreML format optimized for iOS deployment."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from ultralytics import YOLO


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export YOLOv8 model to CoreML for iOS.")
    parser.add_argument(
        "--weights",
        default="weights/best.pt",
        help="Path to trained weights (best.pt).",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="artifacts/ios",
        help="Output directory for CoreML model.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size (640 recommended for iOS).",
    )
    parser.add_argument(
        "--half",
        action="store_true",
        default=True,
        help="Use FP16 precision (smaller file, faster inference).",
    )
    parser.add_argument(
        "--nms",
        action="store_true",
        help="Include NMS in model (simplifies iOS code).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)
    
    # Load model
    weights_path = Path(args.weights).expanduser().resolve()
    if not weights_path.exists():
        logging.error("Weights file not found: %s", weights_path)
        logging.error("Please train a model first or specify correct path.")
        return 1
    
    logging.info("Loading model from: %s", weights_path)
    model = YOLO(str(weights_path))
    
    # Export settings
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    export_kwargs = {
        "format": "coreml",
        "imgsz": args.imgsz,
        "device": "cpu",  # CoreML export should use CPU
        "half": args.half,
        "nms": args.nms,  # Include NMS in model
        "project": str(output_dir),
        "name": "model",
        "exist_ok": True,
    }
    
    logging.info("Exporting to CoreML with settings:")
    logging.info("  Format: CoreML")
    logging.info("  Image size: %d", args.imgsz)
    logging.info("  FP16: %s", args.half)
    logging.info("  Include NMS: %s", args.nms)
    logging.info("  Output: %s", output_dir)
    logging.info("")
    
    try:
        exported_path = model.export(**export_kwargs)
        
        if exported_path:
            exported_file = Path(exported_path)
            file_size_mb = exported_file.stat().st_size / (1024 * 1024)
            
            logging.info("=" * 80)
            logging.info("✅ Export successful!")
            logging.info("=" * 80)
            logging.info("Model file: %s", exported_path)
            logging.info("File size: %.2f MB", file_size_mb)
            logging.info("")
            logging.info("Next steps:")
            logging.info("1. Copy the .mlmodel file to your Xcode project")
            logging.info("2. Add it to your app target")
            logging.info("3. Use DetectionEngine.swift for inference")
            logging.info("=" * 80)
            
            return 0
        else:
            logging.error("Export failed - no output file generated")
            return 1
    except Exception as e:
        logging.error("Export failed: %s", e)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
