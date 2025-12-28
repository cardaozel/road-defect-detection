#!/usr/bin/env python3
"""Train a YOLOv8 model on the prepared RDD2022 dataset."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import torch
import yaml
from ultralytics import YOLO
import shutil


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def auto_detect_device() -> str:
    """Automatically detect the best available device for training."""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def load_config(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {}
    cfg_path = Path(path).expanduser().resolve()
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
        return loaded if isinstance(loaded, dict) else {}


def resolve(cfg: Optional[Dict[str, Any]], section: str, key: str, default: Any = None) -> Any:
    if cfg is None:
        return default
    section_dict = cfg.get(section)
    if section_dict is None or not isinstance(section_dict, dict):
        return default
    return section_dict.get(key, default)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train YOLOv8 on RDD2022.")
    parser.add_argument("--config", default="configs/training.yaml", help="Path to YAML config file.")
    parser.add_argument("--data-yaml", dest="data_yaml", help="Override dataset YAML path.")
    parser.add_argument("--weights", help="Initial weights (e.g., yolov8n.pt).")
    parser.add_argument("--imgsz", type=int, help="Image size for training.")
    parser.add_argument("--epochs", type=int, help="Number of training epochs.")
    parser.add_argument("--batch", type=int, help="Batch size.")
    parser.add_argument("--lr0", type=float, help="Initial learning rate.")
    parser.add_argument("--lrf", type=float, help="Final learning rate fraction.")
    parser.add_argument("--momentum", type=float, help="Optimizer momentum.")
    parser.add_argument("--weight-decay", dest="weight_decay", type=float, help="Weight decay.")
    parser.add_argument("--warmup-epochs", dest="warmup_epochs", type=float, help="Warmup epochs.")
    parser.add_argument("--device", help="Compute device (cuda, cpu, mps).")
    parser.add_argument("--workers", type=int, help="Number of dataloader workers.")
    parser.add_argument("--project", help="Ultralytics project directory.")
    parser.add_argument("--run-name", dest="run_name", help="Experiment/run name.")
    parser.add_argument("--seed", type=int, help="Random seed.")
    parser.add_argument("--exist-ok", dest="exist_ok", action="store_true", help="Overwrite existing run directory.")
    parser.add_argument("--resume", action="store_true", help="Resume the last training run.")
    parser.add_argument("--close-mosaic", dest="close_mosaic", type=int, help="Disable mosaic augmentation after N epochs.")

    # Augmentation overrides
    parser.add_argument("--hsv-h", dest="hsv_h", type=float)
    parser.add_argument("--hsv-s", dest="hsv_s", type=float)
    parser.add_argument("--hsv-v", dest="hsv_v", type=float)
    parser.add_argument("--degrees", type=float)
    parser.add_argument("--translate", type=float)
    parser.add_argument("--scale", type=float)
    parser.add_argument("--shear", type=float)
    parser.add_argument("--perspective", type=float)
    parser.add_argument("--flipud", type=float)
    parser.add_argument("--fliplr", type=float)
    parser.add_argument("--mosaic", type=float)
    parser.add_argument("--mixup", type=float)
    parser.add_argument("--copy-paste", dest="copy_paste", type=float)

    # Validation parameters
    parser.add_argument("--max-det", dest="max_det", type=int, help="Maximum detections per image for validation.")
    parser.add_argument("--conf", type=float, help="Confidence threshold for validation.")
    parser.add_argument("--iou", type=float, help="IoU threshold for NMS during validation.")

    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def merge_settings(args: argparse.Namespace, cfg: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    settings: Dict[str, Any] = {}
    extras: Dict[str, Any] = {}

    data_yaml = getattr(args, "data_yaml") or resolve(cfg, "paths", "data_yaml", "data/yolo/rdd2022.yaml")
    settings["data"] = str(Path(data_yaml).expanduser().resolve())

    weights = getattr(args, "weights") or resolve(cfg, "model", "weights", "yolov8n.pt")
    settings["model"] = str(weights)

    settings["imgsz"] = getattr(args, "imgsz") or resolve(cfg, "model", "imgsz", 640)
    settings["epochs"] = getattr(args, "epochs") or resolve(cfg, "optim", "epochs", 100)
    settings["batch"] = getattr(args, "batch") or resolve(cfg, "optim", "batch", 16)
    settings["lr0"] = getattr(args, "lr0") or resolve(cfg, "optim", "lr0", 0.01)
    settings["lrf"] = getattr(args, "lrf") or resolve(cfg, "optim", "lrf", 0.01)
    settings["momentum"] = getattr(args, "momentum") or resolve(cfg, "optim", "momentum", 0.937)
    settings["weight_decay"] = getattr(args, "weight_decay") or resolve(cfg, "optim", "weight_decay", 0.0005)
    settings["warmup_epochs"] = getattr(args, "warmup_epochs") or resolve(cfg, "optim", "warmup_epochs", 3.0)
    
    # Cosine learning rate schedule (for better convergence)
    cos_lr = resolve(cfg, "optim", "cos_lr")
    if cos_lr is not None:
        settings["cos_lr"] = cos_lr

    # Auto-detect device if not explicitly set, or validate requested device
    requested_device = getattr(args, "device") or resolve(cfg, "hardware", "device")
    if requested_device:
        # Validate that the requested device is available
        if requested_device.startswith("cuda") and not torch.cuda.is_available():
            logging.warning("CUDA requested but not available. Auto-detecting device...")
            requested_device = None
        elif requested_device == "mps" and (not hasattr(torch.backends, "mps") or not torch.backends.mps.is_available()):
            logging.warning("MPS requested but not available. Auto-detecting device...")
            requested_device = None
    
    if not requested_device:
        requested_device = auto_detect_device()
        logging.info("Auto-detected device: %s", requested_device)
    
    settings["device"] = requested_device
    
    # Adjust workers based on device (CPU and MPS need fewer workers due to memory constraints)
    default_workers = getattr(args, "workers") or resolve(cfg, "hardware", "workers")
    if not default_workers:
        if settings["device"] == "cpu":
            default_workers = 4  # Fewer workers for CPU
        elif settings["device"] == "mps":
            default_workers = 2  # MPS has limited unified memory, use fewer workers
        else:
            default_workers = 8  # CUDA can handle more workers
    settings["workers"] = default_workers

    settings["project"] = str(
        Path(getattr(args, "project") or resolve(cfg, "experiment", "project", "results")).expanduser().resolve()
    )
    settings["name"] = getattr(args, "run_name") or resolve(cfg, "experiment", "name", "yolov8n_rdd2022")
    settings["exist_ok"] = bool(getattr(args, "exist_ok") or resolve(cfg, "experiment", "exist_ok", False))
    settings["seed"] = getattr(args, "seed") or resolve(cfg, "experiment", "seed", 42)
    settings["resume"] = getattr(args, "resume")
    settings["close_mosaic"] = getattr(args, "close_mosaic") or resolve(cfg, "augmentation", "close_mosaic", 10)

    aug_keys = [
        "hsv_h",
        "hsv_s",
        "hsv_v",
        "degrees",
        "translate",
        "scale",
        "shear",
        "perspective",
        "flipud",
        "fliplr",
        "mosaic",
        "mixup",
        "copy_paste",
    ]
    for key in aug_keys:
        val = getattr(args, key)
        if val is None:
            val = resolve(cfg, "augmentation", key)
        if val is not None:
            settings[key] = val

    # Validation parameters (for reducing NMS time and memory usage)
    val_max_det = getattr(args, "max_det")
    if val_max_det is None:
        val_max_det = resolve(cfg, "validation", "max_det")
    if val_max_det is not None:
        settings["max_det"] = val_max_det

    val_conf = getattr(args, "conf")
    if val_conf is None:
        val_conf = resolve(cfg, "validation", "conf")
    if val_conf is not None:
        settings["conf"] = val_conf

    val_iou = getattr(args, "iou")
    if val_iou is None:
        val_iou = resolve(cfg, "validation", "iou")
    if val_iou is not None:
        settings["iou"] = val_iou

    extras["weights_dir"] = resolve(cfg, "paths", "weights_dir")

    return settings, extras


def compute_model_stats(model: YOLO) -> Dict[str, Any]:
    """Compute model statistics: size, parameters, FLOPs."""
    stats = {}
    
    # Model size (file size)
    if hasattr(model, "ckpt_path") and model.ckpt_path:
        model_path = Path(model.ckpt_path)
        if model_path.exists():
            stats["model_size_mb"] = model_path.stat().st_size / (1024 * 1024)
    
    # Number of parameters
    try:
        total_params = sum(p.numel() for p in model.model.parameters())
        trainable_params = sum(p.numel() for p in model.model.parameters() if p.requires_grad)
        stats["total_parameters"] = total_params
        stats["trainable_parameters"] = trainable_params
        stats["total_parameters_millions"] = round(total_params / 1e6, 2)
    except Exception as e:
        logging.warning("Could not compute parameters: %s", e)
    
    # FLOPs (approximate)
    try:
        # YOLOv8 models have a method to get FLOPs
        if hasattr(model.model, "info"):
            info = model.model.info(detailed=False, verbose=False)
            if isinstance(info, dict) and "FLOPs" in info:
                stats["flops"] = info["FLOPs"]
                stats["flops_g"] = round(info["FLOPs"] / 1e9, 2)
    except Exception as e:
        logging.debug("Could not compute FLOPs: %s", e)
    
    return stats


def compute_inference_metrics(model: YOLO, data_yaml: str, device: str, num_samples: int = 100) -> Dict[str, Any]:
    """Compute inference time and FPS."""
    metrics = {}
    
    try:
        # Load validation dataset
        from ultralytics.data import YOLODataset
        dataset = YOLODataset(data_yaml, task="detect", mode="val")
        
        if len(dataset) == 0:
            logging.warning("Validation dataset is empty")
            return metrics
        
        # Sample images for inference test
        num_test = min(num_samples, len(dataset))
        test_indices = np.random.choice(len(dataset), num_test, replace=False)
        
        inference_times = []
        for idx in test_indices:
            img_path = dataset.im_files[idx]
            
            # Warmup
            if idx == test_indices[0]:
                _ = model.predict(img_path, device=device, verbose=False)
            
            # Measure inference time
            start = time.time()
            _ = model.predict(img_path, device=device, verbose=False)
            inference_times.append(time.time() - start)
        
        if inference_times:
            avg_time = np.mean(inference_times)
            std_time = np.std(inference_times)
            fps = 1.0 / avg_time if avg_time > 0 else 0
            
            metrics["inference_time_ms"] = round(avg_time * 1000, 2)
            metrics["inference_time_std_ms"] = round(std_time * 1000, 2)
            metrics["fps"] = round(fps, 2)
            metrics["fps_min"] = round(1.0 / (avg_time + std_time) if (avg_time + std_time) > 0 else 0, 2)
            metrics["fps_max"] = round(1.0 / (avg_time - std_time) if (avg_time - std_time) > 0 else 0, 2)
            metrics["num_test_samples"] = num_test
    
    except Exception as e:
        logging.warning("Could not compute inference metrics: %s", e)
    
    return metrics


def extract_evaluation_metrics(trainer_results: Any, class_names: List[str]) -> Dict[str, Any]:
    """Extract evaluation metrics from training results.

    This function pulls scalar metrics (mAP, precision, recall, F1, accuracy) and
    optional per-class metrics from the Ultralytics trainer results.
    
    Args:
        trainer_results: Results object from YOLOv8 model.train() or trainer
        class_names: List of class names (e.g., ["D00", "D01", "D10", "D11", "D20", "D40"])
    
    Returns:
        Dictionary containing all extracted metrics:
        - map50: Mean Average Precision at IoU=0.5 (main accuracy metric)
        - map50_95: COCO-style mAP averaged over IoU 0.5-0.95 (stricter metric)
        - precision: TP/(TP+FP) - fraction of predictions that are correct
        - recall: TP/(TP+FN) - fraction of ground-truth objects found
        - f1_score: Harmonic mean of precision and recall
        - accuracy: Direct accuracy if available from Ultralytics
        - balanced_accuracy: (precision + recall) / 2 (approximation)
        - per_class_metrics: Optional dict with metrics per class
    """
    metrics: Dict[str, Any] = {}
    
    try:
        # Step 1: Extract the results dictionary from various possible formats
        # Ultralytics can return results in different formats, so we check multiple options
        if hasattr(trainer_results, "results_dict"):
            # Case 1: Trainer object with results_dict attribute
            results = trainer_results.results_dict
        elif isinstance(trainer_results, dict):
            # Case 2: Plain dictionary returned by model.train()
            results = trainer_results
        else:
            # Case 3: Try to access trainer attribute if it exists
            if hasattr(trainer_results, "trainer") and hasattr(trainer_results.trainer, "results_dict"):
                results = trainer_results.trainer.results_dict
            else:
                logging.warning("Could not extract results dictionary")
                return metrics
        
        # -----------------------------
        # Step 2: Extract global (overall) scalar metrics
        # These metrics summarize performance across ALL classes and ALL images
        # -----------------------------
        
        # mAP@0.5: Mean Average Precision at IoU threshold 0.5
        # This is the PRIMARY accuracy metric for object detection.
        # Higher is better. Range: 0.0 to 1.0
        # - 0.0-0.3: Poor
        # - 0.3-0.5: Fair
        # - 0.5-0.7: Good
        # - 0.7+: Excellent
        metrics["map50"] = results.get("metrics/mAP50(B)", results.get("metrics/mAP50", None))
        
        # mAP@0.5:0.95: COCO-style metric averaging mAP over IoU thresholds 0.5 to 0.95 (step 0.05)
        # This is a STRICTER metric that requires better localization.
        # Usually lower than mAP@0.5 but more realistic for real-world performance.
        metrics["map50_95"] = results.get("metrics/mAP50-95(B)", results.get("metrics/mAP50-95", None))
        
        # Precision: TP / (TP + FP)
        # Measures: "Of all the defects I predicted, how many were actually defects?"
        # High precision = few false positives (not many false alarms)
        # Range: 0.0 to 1.0, higher is better
        metrics["precision"] = results.get("metrics/precision(B)", results.get("metrics/precision", None))
        
        # Recall: TP / (TP + FN)
        # Measures: "Of all the actual defects, how many did I find?"
        # High recall = few false negatives (not missing many real defects)
        # Range: 0.0 to 1.0, higher is better
        metrics["recall"] = results.get("metrics/recall(B)", results.get("metrics/recall", None))
        
        # Accuracy: Direct accuracy metric if Ultralytics provides it
        # Some trainers may export this, but it's not always available for detection tasks.
        # If not available, we compute balanced_accuracy below as an approximation.
        metrics["accuracy"] = results.get(
            "metrics/accuracy(B)",  # primary key if provided
            results.get("metrics/accuracy", None),  # fallback key
        )
        
        # Step 3: Compute derived metrics from precision and recall
        if metrics["precision"] is not None and metrics["recall"] is not None:
            p = metrics["precision"]
            r = metrics["recall"]
            
            # F1 Score: Harmonic mean of precision and recall
            # Formula: F1 = 2 * (precision * recall) / (precision + recall)
            # This balances precision and recall into a single number.
            # Higher is better. Range: 0.0 to 1.0
            # Good when you need both high precision AND high recall.
            if p + r > 0:
                metrics["f1_score"] = round(2 * (p * r) / (p + r), 4)
            else:
                metrics["f1_score"] = 0.0
        
            # Balanced Accuracy: Simple average of precision and recall
            # Formula: balanced_accuracy = (precision + recall) / 2
            # This gives equal weight to precision and recall.
            # Useful as a single-number summary when you care about both metrics equally.
            # Range: 0.0 to 1.0, higher is better
            metrics["balanced_accuracy"] = round((p + r) / 2.0, 4)
        
        # -----------------------------
        # Step 4: Extract per-class metrics (optional)
        # These metrics show performance for EACH individual defect class
        # -----------------------------
        if "metrics" in str(type(results)):
            # Try to get per-class metrics from confusion matrix or results
            per_class_metrics: Dict[str, Any] = {}
            for i, class_name in enumerate(class_names):
                # Get metrics for each class by index
                class_map50 = results.get(f"metrics/mAP50(B)/{i}", None)
                class_map50_95 = results.get(f"metrics/mAP50-95(B)/{i}", None)
                class_precision = results.get(f"metrics/precision(B)/{i}", None)
                class_recall = results.get(f"metrics/recall(B)/{i}", None)
                
                # Only add if at least one metric is available
                if any(x is not None for x in [class_map50, class_map50_95, class_precision, class_recall]):
                    per_class_metrics[class_name] = {
                        "map50": class_map50,
                        "map50_95": class_map50_95,
                        "precision": class_precision,
                        "recall": class_recall,
                    }
            
            if per_class_metrics:
                metrics["per_class_metrics"] = per_class_metrics
        
    except Exception as e:
        logging.warning("Could not extract all evaluation metrics: %s", e)
    
    return metrics


def save_evaluation_report(
    all_metrics: Dict[str, Any],
    output_dir: Path,
    class_names: List[str],
    model: YOLO,
) -> None:
    """Save comprehensive evaluation report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON report
    report_path = output_dir / "evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2, default=str)
    logging.info("Saved evaluation report to %s", report_path)
    
    # Save YAML report (more human-readable)
    yaml_path = output_dir / "evaluation_report.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(all_metrics, f, default_flow_style=False, allow_unicode=True)
    logging.info("Saved evaluation report (YAML) to %s", yaml_path)
    
    # Save text summary
    summary_path = output_dir / "evaluation_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("ROAD DEFECT DETECTION - MODEL EVALUATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Overall metrics: these are global scores across the whole validation set
        f.write("OVERALL PERFORMANCE METRICS\n")
        f.write("-" * 80 + "\n")
        if "map50" in all_metrics and all_metrics["map50"] is not None:
            f.write(f"mAP@0.5:           {all_metrics['map50']:.4f}\n")
        if "map50_95" in all_metrics and all_metrics["map50_95"] is not None:
            f.write(f"mAP@0.5:0.95:      {all_metrics['map50_95']:.4f}\n")
        if "precision" in all_metrics and all_metrics["precision"] is not None:
            f.write(f"Precision:         {all_metrics['precision']:.4f}\n")
        if "recall" in all_metrics and all_metrics["recall"] is not None:
            f.write(f"Recall:             {all_metrics['recall']:.4f}\n")
        if "f1_score" in all_metrics:
            f.write(f"F1 Score:           {all_metrics['f1_score']:.4f}\n")
        # Accuracy: either provided directly by Ultralytics or approximated as balanced accuracy
        if "accuracy" in all_metrics and all_metrics["accuracy"] is not None:
            f.write(f"Accuracy:           {all_metrics['accuracy']:.4f}\n")
        if "balanced_accuracy" in all_metrics and all_metrics["balanced_accuracy"] is not None:
            f.write(f"Balanced Accuracy:   {all_metrics['balanced_accuracy']:.4f}\n")
        f.write("\n")
        
        # Model statistics
        if "model_stats" in all_metrics:
            f.write("MODEL STATISTICS\n")
            f.write("-" * 80 + "\n")
            stats = all_metrics["model_stats"]
            if "model_size_mb" in stats:
                f.write(f"Model Size:         {stats['model_size_mb']:.2f} MB\n")
            if "total_parameters_millions" in stats:
                f.write(f"Parameters:        {stats['total_parameters_millions']:.2f}M\n")
            if "flops_g" in stats:
                f.write(f"FLOPs:              {stats['flops_g']:.2f} G\n")
            f.write("\n")
        
        # Inference metrics
        if "inference_metrics" in all_metrics:
            f.write("INFERENCE PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            inf = all_metrics["inference_metrics"]
            if "inference_time_ms" in inf:
                f.write(f"Inference Time:     {inf['inference_time_ms']:.2f} ms\n")
            if "fps" in inf:
                f.write(f"FPS:                {inf['fps']:.2f}\n")
            f.write("\n")
        
        # Per-class metrics
        if "per_class_metrics" in all_metrics and all_metrics["per_class_metrics"]:
            f.write("PER-CLASS PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Class':<15} {'mAP@0.5':<12} {'mAP@0.5:0.95':<15} {'Precision':<12} {'Recall':<12}\n")
            f.write("-" * 80 + "\n")
            for class_name, class_metrics in all_metrics["per_class_metrics"].items():
                map50 = class_metrics.get("map50", "N/A")
                map50_95 = class_metrics.get("map50_95", "N/A")
                precision = class_metrics.get("precision", "N/A")
                recall = class_metrics.get("recall", "N/A")
                
                map50_str = f"{map50:.4f}" if isinstance(map50, (int, float)) else str(map50)
                map50_95_str = f"{map50_95:.4f}" if isinstance(map50_95, (int, float)) else str(map50_95)
                precision_str = f"{precision:.4f}" if isinstance(precision, (int, float)) else str(precision)
                recall_str = f"{recall:.4f}" if isinstance(recall, (int, float)) else str(recall)
                
                f.write(f"{class_name:<15} {map50_str:<12} {map50_95_str:<15} {precision_str:<12} {recall_str:<12}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
    
    logging.info("Saved evaluation summary to %s", summary_path)


def run_comprehensive_evaluation(
    model: YOLO,
    trainer_results: Any,
    data_yaml: str,
    device: str,
    output_dir: Path,
    class_names: List[str],
) -> Dict[str, Any]:
    """Run comprehensive evaluation and generate all metrics.
    
    This is the main evaluation function that:
    1. Extracts detection metrics (mAP, precision, recall, F1, accuracy)
    2. Computes model statistics (size, parameters, FLOPs)
    3. Measures inference performance (speed, FPS)
    4. Saves comprehensive reports (JSON, YAML, text)
    5. Logs summary to console
    
    Args:
        model: Trained YOLOv8 model
        trainer_results: Results from model.train() containing validation metrics
        data_yaml: Path to dataset YAML file
        device: Device used for inference ('mps', 'cuda', or 'cpu')
        output_dir: Directory to save evaluation reports
        class_names: List of class names (e.g., ["D00", "D01", "D10", "D11", "D20", "D40"])
    
    Returns:
        Dictionary containing all collected metrics and statistics
    """
    logging.info("Running comprehensive evaluation...")
    
    # Dictionary that will hold every metric and path we collect
    # This will be saved to JSON/YAML files and logged to console
    all_metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # when evaluation was run
        "class_names": class_names,  # list of class labels used in this experiment
    }
    
    # Step 1: Extract overall detection metrics (mAP, Precision, Recall, F1, Accuracy)
    # These are scalar metrics summarizing detector quality over the whole dataset.
    # This is the most important part - tells us how accurate the model is!
    eval_metrics = extract_evaluation_metrics(trainer_results, class_names)
    all_metrics.update(eval_metrics)
    
    # Step 2: Per-class performance metrics (already extracted in eval_metrics)
    # These show how well the model performs on each individual defect type
    
    # Step 3: Confusion Matrix path (generated by Ultralytics during validation)
    # The confusion matrix shows which classes are confused with each other
    # Useful for understanding which defect types are hardest to distinguish
    if hasattr(model, "trainer") and hasattr(model.trainer, "save_dir"):
        confusion_matrix_path = Path(model.trainer.save_dir) / "confusion_matrix.png"
        if confusion_matrix_path.exists():
            all_metrics["confusion_matrix_path"] = str(confusion_matrix_path)
    
    # Step 4: Precision-Recall Curve path (generated by Ultralytics)
    # The PR curve shows the tradeoff between precision and recall at different thresholds
    # Useful for choosing the optimal confidence threshold
    if hasattr(model, "trainer") and hasattr(model.trainer, "save_dir"):
        pr_curve_path = Path(model.trainer.save_dir) / "PR_curve.png"
        if pr_curve_path.exists():
            all_metrics["pr_curve_path"] = str(pr_curve_path)
    
    # Step 5: Measure inference performance (speed and throughput)
    # This tells us how fast the model can process images
    # Important for real-time applications
    logging.info("Computing inference metrics...")
    inference_metrics = compute_inference_metrics(model, data_yaml, device)
    all_metrics["inference_metrics"] = inference_metrics
    
    # Step 6: Compute model complexity statistics
    # This tells us the model size, number of parameters, and computational cost (FLOPs)
    # Useful for understanding model efficiency and deployment requirements
    logging.info("Computing model statistics...")
    model_stats = compute_model_stats(model)
    all_metrics["model_stats"] = model_stats
    
    # Step 7: Save comprehensive report to disk
    # Creates three files:
    # - evaluation_report.json: Machine-readable format
    # - evaluation_report.yaml: Human-readable format
    # - evaluation_summary.txt: Plain text summary
    save_evaluation_report(all_metrics, output_dir, class_names, model)
    
    # Step 8: Log a concise summary to the console
    # This prints the most important metrics so users can quickly see results
    logging.info("=" * 80)
    logging.info("EVALUATION SUMMARY")
    logging.info("=" * 80)
    if all_metrics.get("map50") is not None:
        logging.info("mAP@0.5:        %.4f", all_metrics["map50"])
    if all_metrics.get("map50_95") is not None:
        logging.info("mAP@0.5:0.95:   %.4f", all_metrics["map50_95"])
    if all_metrics.get("precision") is not None:
        logging.info("Precision:      %.4f", all_metrics["precision"])
    if all_metrics.get("recall") is not None:
        logging.info("Recall:         %.4f", all_metrics["recall"])
    if all_metrics.get("f1_score") is not None:
        logging.info("F1 Score:       %.4f", all_metrics["f1_score"])
    if all_metrics.get("accuracy") is not None:
        logging.info("Accuracy:       %.4f", all_metrics["accuracy"])
    if all_metrics.get("balanced_accuracy") is not None:
        logging.info("Balanced Acc:   %.4f", all_metrics["balanced_accuracy"])
    
    if "inference_metrics" in all_metrics and "fps" in all_metrics["inference_metrics"]:
        logging.info("FPS:             %.2f", all_metrics["inference_metrics"]["fps"])
    
    if "model_stats" in all_metrics:
        stats = all_metrics["model_stats"]
        if "total_parameters_millions" in stats:
            logging.info("Parameters:      %.2fM", stats["total_parameters_millions"])
        if "model_size_mb" in stats:
            logging.info("Model Size:      %.2f MB", stats["model_size_mb"])
    
    logging.info("=" * 80)
    
    return all_metrics


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)

    cfg = load_config(args.config)
    overrides, extras = merge_settings(args, cfg)

    logging.info("Training configuration:")
    for key, value in overrides.items():
        logging.info("  %s: %s", key, value)

    model_path = overrides.pop("model")
    model = YOLO(model_path)
    logging.info("Loaded model %s", model_path)

    # Memory management for MPS devices
    device = overrides.get("device", "cpu")
    if device == "mps":
        # Clear MPS cache before training to prevent OOM
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            torch.mps.empty_cache()
            logging.info("Cleared MPS cache before training")

    trainer_results = model.train(**overrides)

    best_path: Optional[Path] = None
    if hasattr(model, "trainer") and getattr(model.trainer, "best", None):
        best_path = Path(model.trainer.best)
    elif isinstance(trainer_results, dict) and trainer_results.get("best"):
        best_path = Path(trainer_results["best"])
    
    # Load best model for evaluation
    if best_path and best_path.exists():
        logging.info("Loading best model for evaluation: %s", best_path)
        eval_model = YOLO(str(best_path))
    else:
        logging.info("Using current model for evaluation")
        eval_model = model
    
    # Get class names from data config
    class_names = ["D00", "D01", "D10", "D11", "D20", "D40"]  # Default RDD2022 classes
    try:
        data_cfg_path = Path(overrides["data"])
        if data_cfg_path.exists():
            with open(data_cfg_path, "r", encoding="utf-8") as f:
                data_cfg = yaml.safe_load(f)
                if "names" in data_cfg:
                    class_names = data_cfg["names"]
    except Exception as e:
        logging.warning("Could not load class names from data config: %s", e)
    
    # Run comprehensive evaluation
    eval_output_dir = Path(overrides["project"]) / overrides["name"] / "evaluation"
    evaluation_metrics = run_comprehensive_evaluation(
        eval_model,
        trainer_results,
        overrides["data"],
        overrides["device"],
        eval_output_dir,
        class_names,
    )

    weights_dir = extras.get("weights_dir")
    if weights_dir and best_path and best_path.exists():
        target_dir = Path(weights_dir).expanduser().resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_path, target_dir / best_path.name)
        logging.info("Copied best weights to %s", target_dir)

    logging.info(
        "Training completed. Best weights: %s",
        str(best_path) if best_path else "see Ultralytics run directory",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
