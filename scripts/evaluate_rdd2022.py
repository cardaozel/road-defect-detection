#!/usr/bin/env python3
"""Evaluate a trained YOLOv8 model on the RDD2022 dataset and log metrics."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from ultralytics import YOLO


METRIC_KEYS = {
    "map50_95": "box.map",
    "map50": "box.map50",
    "map75": "box.map75",
    "precision": "box.mp",
    "recall": "box.mr",
}


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate YOLO weights on RDD2022 splits.")
    parser.add_argument("--weights", required=True, help="Path to trained YOLO weights (e.g., best.pt).")
    parser.add_argument("--data", default="data/yolo/rdd2022.yaml", help="Path to YOLO data YAML.")
    parser.add_argument("--split", choices=["train", "val", "test"], default="val", help="Dataset split to use.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size for evaluation.")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size for evaluation.")
    parser.add_argument("--device", default="cuda", help="Device to run evaluation on.")
    parser.add_argument("--conf", type=float, default=0.001, help="Confidence threshold.")
    parser.add_argument("--iou", type=float, default=0.6, help="IoU threshold for NMS.")
    parser.add_argument("--plots", action="store_true", help="Save confusion matrix, PR curves, etc.")
    parser.add_argument("--json", dest="json_path", help="Optional path to save metrics JSON.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def extract_metrics(metrics_obj: Any) -> Dict[str, float]:
    summary: Dict[str, float] = {}
    for key, attr in METRIC_KEYS.items():
        current = metrics_obj
        for part in attr.split("."):
            current = getattr(current, part)
        summary[key] = float(current)
    return summary


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)

    weights = Path(args.weights).expanduser().resolve()
    data_yaml = Path(args.data).expanduser().resolve()
    logging.info("Loading model from %s", weights)
    model = YOLO(str(weights))

    logging.info("Evaluating on %s split", args.split)
    metrics = model.val(
        data=str(data_yaml),
        split=args.split,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        conf=args.conf,
        iou=args.iou,
        plots=args.plots,
    )

    summary = extract_metrics(metrics)
    for key, value in summary.items():
        logging.info("%s: %.4f", key, value)

    if args.json_path:
        output = Path(args.json_path).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        logging.info("Saved metrics JSON to %s", output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
