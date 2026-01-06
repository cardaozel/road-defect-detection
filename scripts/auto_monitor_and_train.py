#!/usr/bin/env python3
"""
Automatic Training Monitor and Manager
- Monitors current training until completion
- Evaluates results against target metrics
- Auto-starts high-performance training if targets not met
- Auto-resumes if training gets killed
"""

import time
import subprocess
import sys
import logging
from pathlib import Path
import re

# Target metrics
TARGET_METRICS = {
    "recall": 0.70,      # ≥ 70%
    "precision": 0.60,   # ≥ 60%
    "map50": 0.60,       # mAP@0.5 ≥ 60%
    "map50_95": 0.35,    # mAP@0.5:0.95 ≥ 35%
}

# Threshold for "very away" - if any metric is below this, start new training
THRESHOLD_FACTOR = 0.7  # 70% of target = need improvement

def setup_logging():
    """Setup logging to file and console."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "auto_train_monitor.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_training_running():
    """Check if training process is running."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "train_yolov8.py"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except:
        return False

def get_current_run_name():
    """Get the current training run name from running process."""
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if 'train_yolov8.py' in line:
                match = re.search(r'--run-name\s+(\S+)', line)
                if match:
                    return match.group(1)
    except:
        pass
    return None

def wait_for_training_completion(run_name):
    """Wait until current training completes."""
    logging.info(f"Monitoring training run: {run_name}")
    
    while True:
        if not check_training_running():
            # Check if training actually completed (best.pt exists)
            results_dir = Path("results") / run_name
            if (results_dir / "weights" / "best.pt").exists():
                logging.info(f"Training completed: {run_name}")
                return True
            else:
                logging.warning(f"Training stopped but no best.pt found. Checking for checkpoints...")
                last_checkpoint = results_dir / "weights" / "last.pt"
                if last_checkpoint.exists():
                    logging.info(f"Found checkpoint at {last_checkpoint}. Training may have been interrupted.")
                    return False
        
        time.sleep(30)  # Check every 30 seconds

def extract_metrics_from_results(run_name):
    """Extract final metrics from results CSV."""
    results_csv = Path("results") / run_name / "results.csv"
    
    if not results_csv.exists():
        logging.error(f"Results CSV not found: {results_csv}")
        return None
    
    try:
        with open(results_csv, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return None
            
            # Parse header
            header = lines[0].strip().split(',')
            
            # Get last line (final epoch)
            last_line = lines[-1].strip().split(',')
            
            metrics = {}
            for i, col in enumerate(header):
                if i < len(last_line):
                    try:
                        metrics[col] = float(last_line[i])
                    except:
                        metrics[col] = last_line[i]
            
            # Extract key metrics
            result = {
                "precision": metrics.get("metrics/precision(B)", None),
                "recall": metrics.get("metrics/recall(B)", None),
                "map50": metrics.get("metrics/mAP50(B)", None),
                "map50_95": metrics.get("metrics/mAP50-95(B)", None),
            }
            
            logging.info(f"Extracted metrics from {run_name}:")
            for key, value in result.items():
                if value is not None:
                    logging.info(f"  {key}: {value:.4f} ({value*100:.2f}%)")
            
            return result
    except Exception as e:
        logging.error(f"Error reading results CSV: {e}")
        return None

def check_metrics_against_targets(metrics):
    """Check if metrics meet targets."""
    if metrics is None:
        return False, "No metrics available"
    
    issues = []
    all_met = True
    
    for metric_name, target_value in TARGET_METRICS.items():
        actual_value = metrics.get(metric_name)
        
        if actual_value is None:
            issues.append(f"{metric_name}: No data")
            all_met = False
        elif actual_value < target_value * THRESHOLD_FACTOR:
            # Very far from target (below 70% of target)
            issues.append(
                f"{metric_name}: {actual_value:.4f} ({actual_value*100:.2f}%) "
                f"< {target_value*THRESHOLD_FACTOR:.4f} (70% of target {target_value*100:.0f}%)"
            )
            all_met = False
        elif actual_value < target_value:
            # Below target but not "very away"
            issues.append(
                f"{metric_name}: {actual_value:.4f} ({actual_value*100:.2f}%) "
                f"< target {target_value*100:.0f}%"
            )
    
    return all_met, "; ".join(issues) if issues else "All targets met!"

def start_high_performance_training():
    """Start high-performance training with auto-resume capability."""
    run_name = "yolov8s_rdd2022_high_perf"
    config_file = "configs/training_optimized_high_performance.yaml"
    
    logging.info("=" * 80)
    logging.info("Starting High-Performance Training")
    logging.info("=" * 80)
    
    cmd = [
        sys.executable, "scripts/train_yolov8.py",
        "--config", config_file,
        "--project", "results",
        "--run-name", run_name,
        "--epochs", "200",
        "--batch", "4",
        "--imgsz", "640",
        "--conf", "0.15",
        "--iou", "0.6",
        "--max-det", "300",
        "--resume"  # Enable auto-resume
    ]
    
    logging.info(f"Command: {' '.join(cmd)}")
    
    # Start training in background with logging
    log_file = Path("training_log.txt")
    
    try:
        with open(log_file, "a") as log:
            log.write(f"\n{'='*80}\n")
            log.write(f"Started high-performance training at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"{'='*80}\n")
        
        process = subprocess.Popen(
            cmd,
            stdout=open(log_file, "a"),
            stderr=subprocess.STDOUT,
            cwd=Path.cwd()
        )
        
        logging.info(f"Training started with PID: {process.pid}")
        logging.info(f"Monitor with: tail -f {log_file}")
        return process.pid
    except Exception as e:
        logging.error(f"Failed to start training: {e}")
        return None

def monitor_and_auto_resume(run_name):
    """Monitor training and auto-resume if killed."""
    logging.info(f"Starting auto-resume monitor for: {run_name}")
    
    while True:
        if not check_training_running():
            # Check if training completed successfully
            results_dir = Path("results") / run_name
            if (results_dir / "weights" / "best.pt").exists():
                # Check results CSV to see if we reached final epoch
                results_csv = results_dir / "results.csv"
                if results_csv.exists():
                    with open(results_csv, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 1:
                            last_line = lines[-1].strip().split(',')
                            try:
                                epoch = int(last_line[0])
                                if epoch >= 200:  # Target epochs reached
                                    logging.info("Training completed all 200 epochs!")
                                    return True
                            except:
                                pass
            
            # Training was killed, resume it
            logging.warning("Training process not running. Attempting to resume...")
            time.sleep(5)  # Wait a bit before resuming
            
            cmd = [
                sys.executable, "scripts/train_yolov8.py",
                "--config", "configs/training_optimized_high_performance.yaml",
                "--project", "results",
                "--run-name", run_name,
                "--epochs", "200",
                "--batch", "4",
                "--imgsz", "640",
                "--conf", "0.15",
                "--iou", "0.6",
                "--max-det", "300",
                "--resume"
            ]
            
            log_file = Path("training_log.txt")
            try:
                with open(log_file, "a") as log:
                    log.write(f"\n{'='*80}\n")
                    log.write(f"Auto-resuming training at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log.write(f"{'='*80}\n")
                
                subprocess.Popen(
                    cmd,
                    stdout=open(log_file, "a"),
                    stderr=subprocess.STDOUT,
                    cwd=Path.cwd()
                )
                logging.info("Training resumed successfully")
            except Exception as e:
                logging.error(f"Failed to resume training: {e}")
                time.sleep(60)  # Wait longer before retry
        
        time.sleep(30)  # Check every 30 seconds

def main():
    """Main monitoring loop."""
    setup_logging()
    
    logging.info("=" * 80)
    logging.info("Automatic Training Monitor Started")
    logging.info("=" * 80)
    logging.info(f"Target Metrics:")
    for metric, target in TARGET_METRICS.items():
        logging.info(f"  {metric}: ≥ {target*100:.0f}%")
    logging.info("=" * 80)
    
    # Step 1: Wait for current training to complete
    current_run = get_current_run_name() or "yolov8n_rdd202215"
    logging.info(f"Current training run: {current_run}")
    
    logging.info("Waiting for current training to complete...")
    completed_successfully = wait_for_training_completion(current_run)
    
    if not completed_successfully:
        logging.warning("Training did not complete successfully. Checking if we should start new training...")
    
    # Step 2: Extract and evaluate metrics
    logging.info("\n" + "=" * 80)
    logging.info("Evaluating Training Results")
    logging.info("=" * 80)
    
    metrics = extract_metrics_from_results(current_run)
    all_targets_met, message = check_metrics_against_targets(metrics)
    
    logging.info(f"\nResults: {message}")
    
    # Step 3: Decide if we need high-performance training
    if not all_targets_met:
        logging.info("\n" + "=" * 80)
        logging.info("Metrics below targets. Starting high-performance training...")
        logging.info("=" * 80)
        
        pid = start_high_performance_training()
        if pid:
            # Step 4: Monitor and auto-resume
            new_run_name = "yolov8s_rdd2022_high_perf"
            logging.info(f"\nMonitoring new training: {new_run_name}")
            logging.info("Auto-resume enabled - training will restart if killed")
            logging.info("=" * 80)
            
            monitor_and_auto_resume(new_run_name)
        else:
            logging.error("Failed to start high-performance training")
            sys.exit(1)
    else:
        logging.info("\n" + "=" * 80)
        logging.info("✅ All target metrics achieved! No new training needed.")
        logging.info("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nMonitor stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

