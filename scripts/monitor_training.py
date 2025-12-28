#!/usr/bin/env python3
"""Monitor training progress with real-time metrics, alerts, and progress visualization."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor YOLOv8 training progress.")
    parser.add_argument(
        "--results-dir",
        dest="results_dir",
        help="Path to training results directory (e.g., results/yolov8s_rdd2022_phase1_mps).",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch mode - continuously monitor and update.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Update interval in seconds (for watch mode).",
    )
    parser.add_argument(
        "--target-map",
        dest="target_map",
        type=float,
        default=0.60,
        help="Target mAP@0.5 to achieve.",
    )
    parser.add_argument(
        "--alert-on-target",
        dest="alert_on_target",
        action="store_true",
        help="Alert when target mAP is reached.",
    )
    parser.add_argument(
        "--json-output",
        dest="json_output",
        help="Save latest metrics to JSON file.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def find_latest_results_dir() -> Optional[Path]:
    """Find the most recently modified results directory."""
    results_base = Path("results")
    if not results_base.exists():
        return None
    
    dirs = [d for d in results_base.iterdir() if d.is_dir() and (d / "results.csv").exists()]
    if not dirs:
        return None
    
    # Sort by modification time
    dirs.sort(key=lambda x: (x / "results.csv").stat().st_mtime, reverse=True)
    return dirs[0]


def load_latest_metrics(results_dir: Path) -> Dict:
    """Load latest metrics from results CSV."""
    results_csv = results_dir / "results.csv"
    
    if not results_csv.exists():
        return {}
    
    try:
        df = pd.read_csv(results_csv)
        if df.empty:
            return {}
        
        # Get latest row
        latest = df.iloc[-1]
        
        metrics = {
            "epoch": int(latest.get("epoch", 0)),
            "map50": float(latest.get("metrics/mAP50(B)", 0)),
            "map50_95": float(latest.get("metrics/mAP50-95(B)", 0)),
            "precision": float(latest.get("metrics/precision(B)", 0)),
            "recall": float(latest.get("metrics/recall(B)", 0)),
            "train_box_loss": float(latest.get("train/box_loss", 0)),
            "train_cls_loss": float(latest.get("train/cls_loss", 0)),
            "train_dfl_loss": float(latest.get("train/dfl_loss", 0)),
            "val_box_loss": float(latest.get("val/box_loss", 0)),
            "val_cls_loss": float(latest.get("val/cls_loss", 0)),
            "val_dfl_loss": float(latest.get("val/dfl_loss", 0)),
        }
        
        # Calculate F1
        p = metrics["precision"]
        r = metrics["recall"]
        metrics["f1_score"] = 2 * (p * r) / (p + r) if (p + r) > 0 else 0.0
        
        # Training progress
        if "epoch" in latest:
            total_epochs = 200  # Default, could be read from args.yaml
            metrics["progress_percent"] = (metrics["epoch"] / total_epochs) * 100
            metrics["remaining_epochs"] = total_epochs - metrics["epoch"]
        
        return metrics
    except Exception as e:
        logging.warning("Error reading metrics: %s", e)
        return {}


def print_status(metrics: Dict, target_map: float) -> None:
    """Print formatted training status."""
    print("\n" + "=" * 80)
    print("TRAINING STATUS")
    print("=" * 80)
    
    if not metrics:
        print("❌ No metrics available yet")
        return
    
    epoch = metrics.get("epoch", 0)
    map50 = metrics.get("map50", 0)
    precision = metrics.get("precision", 0)
    recall = metrics.get("recall", 0)
    f1 = metrics.get("f1_score", 0)
    progress = metrics.get("progress_percent", 0)
    
    print(f"Epoch: {epoch}")
    print(f"Progress: {progress:.1f}%")
    print(f"")
    print(f"Metrics:")
    print(f"  mAP@0.5:     {map50:.4f} {'✅' if map50 >= target_map else '❌'} (target: {target_map:.2f})")
    print(f"  mAP@0.5:0.95: {metrics.get('map50_95', 0):.4f}")
    print(f"  Precision:   {precision:.4f}")
    print(f"  Recall:      {recall:.4f}")
    print(f"  F1 Score:    {f1:.4f}")
    print(f"")
    print(f"Training Loss:")
    print(f"  Box:  {metrics.get('train_box_loss', 0):.4f}")
    print(f"  Cls:  {metrics.get('train_cls_loss', 0):.4f}")
    print(f"  DFL:  {metrics.get('train_dfl_loss', 0):.4f}")
    print(f"")
    print(f"Validation Loss:")
    print(f"  Box:  {metrics.get('val_box_loss', 0):.4f}")
    print(f"  Cls:  {metrics.get('val_cls_loss', 0):.4f}")
    print(f"  DFL:  {metrics.get('val_dfl_loss', 0):.4f}")
    
    if metrics.get("remaining_epochs", 0) > 0:
        print(f"")
        print(f"Remaining epochs: {metrics.get('remaining_epochs', 0)}")
    
    print("=" * 80 + "\n")


def check_target_reached(metrics: Dict, target_map: float) -> bool:
    """Check if target mAP has been reached."""
    map50 = metrics.get("map50", 0)
    return map50 >= target_map


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)
    
    # Find results directory
    if args.results_dir:
        results_dir = Path(args.results_dir).expanduser().resolve()
    else:
        results_dir = find_latest_results_dir()
        if results_dir:
            logging.info("Found latest results directory: %s", results_dir)
        else:
            logging.error("No results directory found. Specify --results-dir or ensure training has started.")
            return 1
    
    if not results_dir.exists():
        logging.error("Results directory not found: %s", results_dir)
        return 1
    
    if args.watch:
        logging.info("Watch mode: updating every %d seconds", args.interval)
        logging.info("Press Ctrl+C to stop")
        
        target_reached = False
        
        try:
            while True:
                metrics = load_latest_metrics(results_dir)
                print_status(metrics, args.target_map)
                
                if args.alert_on_target and not target_reached:
                    if check_target_reached(metrics, args.target_map):
                        print("\n🎉 TARGET mAP REACHED! 🎉\n")
                        target_reached = True
                
                if args.json_output:
                    json_path = Path(args.json_output).expanduser().resolve()
                    json_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(json_path, "w") as f:
                        json.dump(metrics, f, indent=2)
                
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
    else:
        # Single check
        metrics = load_latest_metrics(results_dir)
        print_status(metrics, args.target_map)
        
        if args.json_output:
            json_path = Path(args.json_output).expanduser().resolve()
            json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(json_path, "w") as f:
                json.dump(metrics, f, indent=2)
            logging.info("Saved metrics to: %s", json_path)
        
        if check_target_reached(metrics, args.target_map):
            print("\n✅ Target mAP achieved!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
