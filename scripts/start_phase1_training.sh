#!/bin/bash
# Start PHASE1 optimized training for iOS deployment
# This script will train a high-accuracy model (target: mAP@0.5 > 60%)

set -e  # Exit on error

echo "=========================================="
echo "PHASE1: Starting Optimized Training"
echo "=========================================="
echo ""
echo "Target: mAP@0.5 > 60% for iOS deployment"
echo "Model: YOLOv8-small (yolov8s)"
echo ""

# Check if running on MPS (macOS)
DEVICE=""
if [[ "$OSTYPE" == "darwin"* ]]; then
    DEVICE="--device mps"
    echo "Detected macOS - using MPS"
    echo "Using MPS-safe configuration"
    CONFIG="configs/training_phase1_mps_safe.yaml"
else
    CONFIG="configs/training_phase1_optimized.yaml"
fi

echo "Configuration: $CONFIG"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start training
python scripts/train_yolov8.py \
    --config "$CONFIG" \
    $DEVICE \
    --epochs 200 \
    --imgsz 640

echo ""
echo "=========================================="
echo "Training started!"
echo "Monitor progress in: results/yolov8s_rdd2022_phase1/"
echo "=========================================="
