#!/usr/bin/env python3
"""
Create training graphs for thesis documentation.
Generates: mAP@0.5, Precision, Recall, Loss curves
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_training_graphs(results_csv, output_dir):
    """Create all training graphs for thesis."""
    
    # Read results
    df = pd.read_csv(results_csv)
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Figure 1: mAP@0.5 and mAP@0.5:0.95 over epochs
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['epoch'], df['metrics/mAP50(B)'] * 100, 'b-', linewidth=2, label='mAP@0.5')
    ax.plot(df['epoch'], df['metrics/mAP50-95(B)'] * 100, 'r-', linewidth=2, label='mAP@0.5:0.95')
    
    # Mark best points
    best_map50_idx = df['metrics/mAP50(B)'].idxmax()
    best_map50_95_idx = df['metrics/mAP50-95(B)'].idxmax()
    
    ax.plot(df.loc[best_map50_idx, 'epoch'], df.loc[best_map50_idx, 'metrics/mAP50(B)'] * 100, 
            'bo', markersize=10, label=f'Best mAP@0.5: {df.loc[best_map50_idx, "metrics/mAP50(B)"]*100:.2f}% (Epoch {int(df.loc[best_map50_idx, "epoch"])})')
    ax.plot(df.loc[best_map50_95_idx, 'epoch'], df.loc[best_map50_95_idx, 'metrics/mAP50-95(B)'] * 100, 
            'ro', markersize=10, label=f'Best mAP@0.5:0.95: {df.loc[best_map50_95_idx, "metrics/mAP50-95(B)"]*100:.2f}% (Epoch {int(df.loc[best_map50_95_idx, "epoch"])})')
    
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('mAP (%)', fontsize=12, fontweight='bold')
    ax.set_title('Training Progress: mAP Metrics', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 200)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'training_map_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 2: Precision and Recall over epochs
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['epoch'], df['metrics/precision(B)'] * 100, 'g-', linewidth=2, label='Precision')
    ax.plot(df['epoch'], df['metrics/recall(B)'] * 100, 'm-', linewidth=2, label='Recall')
    
    # Mark best points
    best_prec_idx = df['metrics/precision(B)'].idxmax()
    best_rec_idx = df['metrics/recall(B)'].idxmax()
    
    ax.plot(df.loc[best_prec_idx, 'epoch'], df.loc[best_prec_idx, 'metrics/precision(B)'] * 100, 
            'go', markersize=10, label=f'Best Precision: {df.loc[best_prec_idx, "metrics/precision(B)"]*100:.2f}% (Epoch {int(df.loc[best_prec_idx, "epoch"])})')
    ax.plot(df.loc[best_rec_idx, 'epoch'], df.loc[best_rec_idx, 'metrics/recall(B)'] * 100, 
            'mo', markersize=10, label=f'Best Recall: {df.loc[best_rec_idx, "metrics/recall(B)"]*100:.2f}% (Epoch {int(df.loc[best_rec_idx, "epoch"])})')
    
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Training Progress: Precision and Recall', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 200)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'training_precision_recall.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 3: Loss curves
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['epoch'], df['train/box_loss'], 'b-', linewidth=1.5, label='Box Loss (Train)', alpha=0.7)
    ax.plot(df['epoch'], df['train/cls_loss'], 'g-', linewidth=1.5, label='Classification Loss (Train)', alpha=0.7)
    ax.plot(df['epoch'], df['val/box_loss'], 'r--', linewidth=1.5, label='Box Loss (Val)', alpha=0.7)
    ax.plot(df['epoch'], df['val/cls_loss'], 'm--', linewidth=1.5, label='Classification Loss (Val)', alpha=0.7)
    
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Loss', fontsize=12, fontweight='bold')
    ax.set_title('Training and Validation Loss Curves', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 200)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'training_loss_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 4: Combined metrics overview
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # mAP@0.5
    ax1.plot(df['epoch'], df['metrics/mAP50(B)'] * 100, 'b-', linewidth=2)
    best_map50_idx = df['metrics/mAP50(B)'].idxmax()
    ax1.plot(df.loc[best_map50_idx, 'epoch'], df.loc[best_map50_idx, 'metrics/mAP50(B)'] * 100, 'ro', markersize=8)
    ax1.set_xlabel('Epoch', fontweight='bold')
    ax1.set_ylabel('mAP@0.5 (%)', fontweight='bold')
    ax1.set_title(f'mAP@0.5 (Best: {df.loc[best_map50_idx, "metrics/mAP50(B)"]*100:.2f}%)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Precision
    ax2.plot(df['epoch'], df['metrics/precision(B)'] * 100, 'g-', linewidth=2)
    best_prec_idx = df['metrics/precision(B)'].idxmax()
    ax2.plot(df.loc[best_prec_idx, 'epoch'], df.loc[best_prec_idx, 'metrics/precision(B)'] * 100, 'ro', markersize=8)
    ax2.set_xlabel('Epoch', fontweight='bold')
    ax2.set_ylabel('Precision (%)', fontweight='bold')
    ax2.set_title(f'Precision (Best: {df.loc[best_prec_idx, "metrics/precision(B)"]*100:.2f}%)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Recall
    ax3.plot(df['epoch'], df['metrics/recall(B)'] * 100, 'm-', linewidth=2)
    best_rec_idx = df['metrics/recall(B)'].idxmax()
    ax3.plot(df.loc[best_rec_idx, 'epoch'], df.loc[best_rec_idx, 'metrics/recall(B)'] * 100, 'ro', markersize=8)
    ax3.set_xlabel('Epoch', fontweight='bold')
    ax3.set_ylabel('Recall (%)', fontweight='bold')
    ax3.set_title(f'Recall (Best: {df.loc[best_rec_idx, "metrics/recall(B)"]*100:.2f}%)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # mAP@0.5:0.95
    ax4.plot(df['epoch'], df['metrics/mAP50-95(B)'] * 100, 'r-', linewidth=2)
    best_map50_95_idx = df['metrics/mAP50-95(B)'].idxmax()
    ax4.plot(df.loc[best_map50_95_idx, 'epoch'], df.loc[best_map50_95_idx, 'metrics/mAP50-95(B)'] * 100, 'ro', markersize=8)
    ax4.set_xlabel('Epoch', fontweight='bold')
    ax4.set_ylabel('mAP@0.5:0.95 (%)', fontweight='bold')
    ax4.set_title(f'mAP@0.5:0.95 (Best: {df.loc[best_map50_95_idx, "metrics/mAP50-95(B)"]*100:.2f}%)', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'training_metrics_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Graphs created in {output_dir}/")
    print(f"  - training_map_metrics.png")
    print(f"  - training_precision_recall.png")
    print(f"  - training_loss_curves.png")
    print(f"  - training_metrics_overview.png")

if __name__ == "__main__":
    import sys
    results_csv = sys.argv[1] if len(sys.argv) > 1 else "results/yolov8s_rdd2022_high_perf/results.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "results/yolov8s_rdd2022_high_perf/graphs"
    
    try:
        create_training_graphs(results_csv, output_dir)
    except ImportError:
        print("❌ Error: pandas and matplotlib required.")
        print("   Install with: pip install pandas matplotlib")
        sys.exit(1)

