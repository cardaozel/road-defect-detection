#!/usr/bin/env python3
"""Comprehensive evaluation tool with detailed metrics, per-class analysis, and confidence threshold optimization."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import yaml
from ultralytics import YOLO


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Comprehensive evaluation with detailed metrics and analysis."
    )
    parser.add_argument("--weights", required=True, help="Path to trained weights (best.pt).")
    parser.add_argument("--data", default="data/yolo/rdd2022.yaml", help="Path to data YAML.")
    parser.add_argument("--split", choices=["train", "val", "test"], default="test", help="Split to evaluate.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size.")
    parser.add_argument("--device", help="Device (auto-detected if not set).")
    parser.add_argument("--output-dir", dest="output_dir", default="results/evaluation", help="Output directory.")
    parser.add_argument("--optimize-conf", dest="optimize_conf", action="store_true", help="Find optimal confidence threshold.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def auto_detect_device() -> str:
    """Auto-detect best available device."""
    import torch
    
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def optimize_confidence_threshold(
    model: YOLO,
    data_yaml: str,
    split: str,
    device: str,
    imgsz: int,
) -> Tuple[float, Dict[str, Any]]:
    """Find optimal confidence threshold that maximizes F1 score."""
    logging.info("Optimizing confidence threshold...")
    
    conf_thresholds = np.arange(0.1, 0.95, 0.05)
    best_f1 = 0.0
    best_conf = 0.5
    results = []
    
    for conf in conf_thresholds:
        metrics = model.val(
            data=data_yaml,
            split=split,
            batch=16,
            imgsz=imgsz,
            device=device,
            conf=conf,
            iou=0.7,
            verbose=False,
        )
        
        precision = float(metrics.box.mp)
        recall = float(metrics.box.mr)
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        results.append({
            "confidence": float(conf),
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "map50": float(metrics.box.map50),
        })
        
        if f1 > best_f1:
            best_f1 = f1
            best_conf = conf
        
        logging.info("  conf=%.2f: precision=%.4f, recall=%.4f, F1=%.4f", conf, precision, recall, f1)
    
    logging.info("Optimal confidence threshold: %.2f (F1=%.4f)", best_conf, best_f1)
    
    return best_conf, {"optimal_threshold": best_conf, "optimal_f1": best_f1, "all_results": results}


def compute_per_class_metrics(metrics_obj: Any, class_names: List[str]) -> Dict[str, Any]:
    """Extract per-class metrics."""
    per_class = {}
    
    try:
        # Try to get per-class metrics from results
        if hasattr(metrics_obj, "results_dict"):
            results_dict = metrics_obj.results_dict
            
            for i, class_name in enumerate(class_names):
                class_metrics = {}
                
                # Try different key formats
                keys_to_try = [
                    f"metrics/mAP50(B)/{i}",
                    f"metrics/mAP50-95(B)/{i}",
                    f"metrics/precision(B)/{i}",
                    f"metrics/recall(B)/{i}",
                ]
                
                for key in keys_to_try:
                    if key in results_dict:
                        metric_name = key.split("/")[-1].split("(")[0]
                        class_metrics[metric_name] = float(results_dict[key])
                
                if class_metrics:
                    per_class[class_name] = class_metrics
    except Exception as e:
        logging.warning("Could not extract per-class metrics: %s", e)
    
    return per_class


def analyze_class_distribution(data_yaml: str, split: str) -> Dict[str, Any]:
    """Analyze class distribution in the dataset."""
    from ultralytics.data import YOLODataset
    
    try:
        dataset = YOLODataset(data_yaml, task="detect", mode=split)
        
        class_counts = defaultdict(int)
        total_objects = 0
        
        for item in dataset.labels:
            if isinstance(item, dict) and "cls" in item:
                for cls_id in item["cls"]:
                    class_counts[int(cls_id)] += 1
                    total_objects += 1
        
        distribution = {
            "total_images": len(dataset),
            "total_objects": total_objects,
            "per_class": {f"class_{i}": class_counts[i] for i in range(6)},
            "class_balance": {f"class_{i}": class_counts[i] / total_objects if total_objects > 0 else 0 
                            for i in range(6)}
        }
        
        return distribution
    except Exception as e:
        logging.warning("Could not analyze class distribution: %s", e)
        return {}


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)
    
    # Load model
    weights_path = Path(args.weights).expanduser().resolve()
    if not weights_path.exists():
        logging.error("Weights file not found: %s", weights_path)
        return 1
    
    logging.info("Loading model: %s", weights_path)
    model = YOLO(str(weights_path))
    
    # Auto-detect device
    device = args.device or auto_detect_device()
    logging.info("Using device: %s", device)
    
    # Load class names
    data_yaml_path = Path(args.data).expanduser().resolve()
    class_names = ["D00", "D01", "D10", "D11", "D20", "D40"]
    try:
        with open(data_yaml_path, "r") as f:
            data_cfg = yaml.safe_load(f)
            if "names" in data_cfg:
                class_names = data_cfg["names"]
    except Exception as e:
        logging.warning("Could not load class names: %s", e)
    
    # Run evaluation
    logging.info("Evaluating on %s split...", args.split)
    metrics = model.val(
        data=str(data_yaml_path),
        split=args.split,
        batch=args.batch,
        imgsz=args.imgsz,
        device=device,
        conf=0.001,  # Low conf for comprehensive evaluation
        iou=0.7,
        plots=True,
        verbose=args.verbose,
    )
    
    # Extract metrics
    results = {
        "split": args.split,
        "model_path": str(weights_path),
        "image_size": args.imgsz,
        "overall_metrics": {
            "map50": float(metrics.box.map50),
            "map50_95": float(metrics.box.map),
            "precision": float(metrics.box.mp),
            "recall": float(metrics.box.mr),
        },
    }
    
    # Compute F1 score
    p = results["overall_metrics"]["precision"]
    r = results["overall_metrics"]["recall"]
    results["overall_metrics"]["f1_score"] = 2 * (p * r) / (p + r) if (p + r) > 0 else 0.0
    
    # Per-class metrics
    per_class = compute_per_class_metrics(metrics, class_names)
    if per_class:
        results["per_class_metrics"] = per_class
    
    # Class distribution
    distribution = analyze_class_distribution(str(data_yaml_path), args.split)
    if distribution:
        results["dataset_distribution"] = distribution
    
    # Confidence threshold optimization
    if args.optimize_conf:
        best_conf, conf_analysis = optimize_confidence_threshold(
            model, str(data_yaml_path), args.split, device, args.imgsz
        )
        results["confidence_optimization"] = conf_analysis
        results["recommended_confidence"] = best_conf
    
    # Save results
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON report
    json_path = output_dir / f"comprehensive_evaluation_{args.split}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    logging.info("Saved comprehensive evaluation to: %s", json_path)
    
    # Print summary
    logging.info("=" * 80)
    logging.info("COMPREHENSIVE EVALUATION RESULTS")
    logging.info("=" * 80)
    logging.info("Split: %s", args.split)
    logging.info("mAP@0.5: %.4f", results["overall_metrics"]["map50"])
    logging.info("mAP@0.5:0.95: %.4f", results["overall_metrics"]["map50_95"])
    logging.info("Precision: %.4f", results["overall_metrics"]["precision"])
    logging.info("Recall: %.4f", results["overall_metrics"]["recall"])
    logging.info("F1 Score: %.4f", results["overall_metrics"]["f1_score"])
    
    if "recommended_confidence" in results:
        logging.info("Recommended Confidence: %.2f", results["recommended_confidence"])
    
    logging.info("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
