#!/bin/bash
# Start high-performance training to achieve target metrics
# Target: Recall ≥70%, Precision ≥60%, mAP@0.5 ≥60%, mAP@0.5:0.95 ≥35%

cd "$(dirname "$0")"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  High-Performance Training for Target Metrics          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Target Metrics:"
echo "  - Recall ≥ 70%"
echo "  - Precision ≥ 60%"
echo "  - mAP@0.5 ≥ 60%"
echo "  - mAP@0.5:0.95 ≥ 35%"
echo ""
echo "Current Metrics (Epoch 93):"
echo "  - Recall: 24.0%"
echo "  - Precision: 43.4%"
echo "  - mAP@0.5: 19.3%"
echo "  - mAP@0.5:0.95: 7.6%"
echo ""

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Continuing anyway..."
fi

echo ""
echo "Starting training with optimized configuration..."
echo "  Model: YOLOv8s (small)"
echo "  Image Size: 640×640"
echo "  Batch Size: 4"
echo "  Epochs: 200"
echo "  Confidence: 0.15 (for higher recall)"
echo ""

python scripts/train_yolov8.py \
    --config configs/training_optimized_high_performance.yaml \
    --project results \
    --run-name yolov8s_rdd2022_high_perf \
    --epochs 200 \
    --batch 4 \
    --imgsz 640 \
    --conf 0.15 \
    --iou 0.6 \
    --max-det 300 \
    > training_log.txt 2>&1

echo ""
echo "Training started! Monitor progress with:"
echo "  tail -f training_log.txt"
echo "  ./scripts/monitor_epochs.sh"
echo ""

