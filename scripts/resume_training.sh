#!/bin/bash
# Resume training from the last checkpoint

cd "$(dirname "$0")/.."

echo "Resuming YOLOv8 training from last checkpoint..."
echo "="

# Use the same config that was used before
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --resume

echo ""
echo "Training resumed! It will continue from where it stopped."
