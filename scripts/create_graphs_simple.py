#!/usr/bin/env python3
"""
Create training graphs using only matplotlib (no pandas required).
"""

import csv
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

def create_graphs(results_csv, output_dir):
    """Create training graphs."""
    
    # Read CSV
    epochs = []
    map50 = []
    map50_95 = []
    precision = []
    recall = []
    train_box_loss = []
    val_box_loss = []
    
    with open(results_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            epochs.append(int(row['epoch']))
            map50.append(float(row['metrics/mAP50(B)']))
            map50_95.append(float(row['metrics/mAP50-95(B)']))
            precision.append(float(row['metrics/precision(B)']))
            recall.append(float(row['metrics/recall(B)']))
            train_box_loss.append(float(row['train/box_loss']))
            val_box_loss.append(float(row['val/box_loss']))
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find best epochs
    best_map50_idx = map50.index(max(map50))
    best_prec_idx = precision.index(max(precision))
    best_rec_idx = recall.index(max(recall))
    
    # Graph 1: mAP metrics
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(epochs, [m*100 for m in map50], 'b-', linewidth=2, label='mAP@0.5')
    ax.plot(epochs, [m*100 for m in map50_95], 'r-', linewidth=2, label='mAP@0.5:0.95')
    ax.plot(epochs[best_map50_idx], map50[best_map50_idx]*100, 'bo', markersize=10, 
            label=f'Best mAP@0.5: {map50[best_map50_idx]*100:.2f}% (Epoch {epochs[best_map50_idx]})')
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('mAP (%)', fontsize=12, fontweight='bold')
    ax.set_title('Training Progress: mAP Metrics', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'training_map_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Graph 2: Precision and Recall
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(epochs, [p*100 for p in precision], 'g-', linewidth=2, label='Precision')
    ax.plot(epochs, [r*100 for r in recall], 'm-', linewidth=2, label='Recall')
    ax.plot(epochs[best_prec_idx], precision[best_prec_idx]*100, 'go', markersize=10,
            label=f'Best Precision: {precision[best_prec_idx]*100:.2f}% (Epoch {epochs[best_prec_idx]})')
    ax.plot(epochs[best_rec_idx], recall[best_rec_idx]*100, 'mo', markersize=10,
            label=f'Best Recall: {recall[best_rec_idx]*100:.2f}% (Epoch {epochs[best_rec_idx]})')
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Training Progress: Precision and Recall', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'training_precision_recall.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Graph 3: Loss curves
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(epochs, train_box_loss, 'b-', linewidth=1.5, label='Box Loss (Train)', alpha=0.7)
    ax.plot(epochs, val_box_loss, 'r--', linewidth=1.5, label='Box Loss (Val)', alpha=0.7)
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Loss', fontsize=12, fontweight='bold')
    ax.set_title('Training and Validation Loss Curves', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'training_loss_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Graphs created in {output_dir}/")
    print(f"  - training_map_metrics.png")
    print(f"  - training_precision_recall.png")
    print(f"  - training_loss_curves.png")

if __name__ == "__main__":
    import sys
    results_csv = sys.argv[1] if len(sys.argv) > 1 else "results/yolov8s_rdd2022_high_perf/results.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "results/yolov8s_rdd2022_high_perf/graphs"
    create_graphs(results_csv, output_dir)

