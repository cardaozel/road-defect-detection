#!/bin/bash
# Show current training progress

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
RESULTS_DIR="results/yolov8s_rdd2022_phase1_mps"

echo "=========================================="
echo "📊 Training Progress Status"
echo "=========================================="
echo ""

# Check if training is running
if ! pgrep -f "train_yolov8.py" > /dev/null; then
    echo "❌ Training process is NOT running"
    exit 1
fi

echo "✅ Training process is RUNNING"
echo ""

# Get current batch
CURRENT_BATCH=$(grep -oE "\s+[0-9]+/9545" "$LOG_FILE" 2>/dev/null | tail -1 | grep -oE "[0-9]+" | head -1)
TOTAL_BATCHES=9545

if [ -z "$CURRENT_BATCH" ]; then
    echo "⚠️  Could not determine current batch"
else
    PERCENT=$((CURRENT_BATCH * 100 / TOTAL_BATCHES))
    REMAINING=$((TOTAL_BATCHES - CURRENT_BATCH))
    MINUTES_REMAINING=$((REMAINING / 4 / 60))
    
    echo "📈 Progress:"
    echo "   Batch: $CURRENT_BATCH / $TOTAL_BATCHES ($PERCENT%)"
    echo "   Epoch: 1/200"
    echo "   Estimated time remaining for epoch 1: ~$MINUTES_REMAINING minutes"
    echo ""
fi

# Check if epoch 1 completed
if [ -f "$RESULTS_DIR/results.csv" ]; then
    echo "✅ EPOCH 1 COMPLETED!"
    echo ""
    echo "📊 Epoch 1 Results:"
    head -2 "$RESULTS_DIR/results.csv" | column -t -s, 2>/dev/null || head -2 "$RESULTS_DIR/results.csv"
    echo ""
    
    if [ -f "$RESULTS_DIR/weights/last.pt" ]; then
        echo "💾 Checkpoint saved:"
        ls -lh "$RESULTS_DIR/weights/last.pt"
    fi
else
    echo "⏳ Epoch 1 still in progress..."
    echo ""
    echo "💡 To get notified when epoch 1 completes, run:"
    echo "   ./scripts/wait_for_epoch1.sh"
fi

echo ""
echo "=========================================="
