#!/usr/bin/env python3
"""Export and quantize YOLOv8 weights for mobile/edge deployment."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from ultralytics import YOLO


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export YOLOv8 weights to mobile-friendly formats.")
    parser.add_argument("--weights", required=True, help="Path to trained weights (best.pt).")
    parser.add_argument(
        "--format",
        choices=["onnx", "torchscript", "tflite", "coreml", "ncnn"],
        default="onnx",
        help="Export format.",
    )
    parser.add_argument("--imgsz", type=int, nargs="*", default=[640], help="Export image size (int or H W).")
    parser.add_argument("--device", default="cpu", help="Device used during export.")
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic axes (ONNX).")
    parser.add_argument("--half", action="store_true", help="Use FP16 precision where supported.")
    parser.add_argument("--int8", action="store_true", help="Enable INT8 quantization (TFLite/NCNN).")
    parser.add_argument("--simplify", action="store_true", help="Simplify ONNX graph post-export.")
    parser.add_argument("--workspace", default="artifacts", help="Directory to store exported models.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)

    weights = Path(args.weights).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    logging.info("Loading weights from %s", weights)
    model = YOLO(str(weights))

    export_kwargs = {
        "format": args.format,
        "imgsz": args.imgsz if len(args.imgsz) > 1 else args.imgsz[0],
        "device": args.device,
        "dynamic": args.dynamic,
        "half": args.half,
        "int8": args.int8,
        "simplify": args.simplify,
        "project": str(workspace),
        "name": "exports",
        "exist_ok": True,
    }

    logging.info("Export settings: %s", export_kwargs)
    exported_path: Optional[str] = model.export(**export_kwargs)
    logging.info("Exported model artifact: %s", exported_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
