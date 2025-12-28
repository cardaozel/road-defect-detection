#!/bin/bash
# Start PHASE1 training with maximum memory safety
# This version uses batch=2 and workers=0 to prevent OOM

set -e

echo "=========================================="
echo "PHASE1: Starting SAFE Training"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  - Model: YOLOv8-small (yolov8s)"
echo "  - Batch size: 2 (memory-safe)"
echo "  - Workers: 0 (single-threaded, safest)"
echo "  - Image size: 640"
echo "  - Epochs: 200"
echo ""
echo "✅ Automatic checkpointing enabled"
echo "✅ Can resume if interrupted (use --resume)"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start training with safe settings
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --batch 2 \
    --workers 0 \
    --epochs 200 \
    --imgsz 640

echo ""
echo "=========================================="
echo "Training completed successfully!"
echo "Check results in: results/yolov8s_rdd2022_phase1_mps/"
echo "=========================================="
