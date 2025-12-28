#!/bin/bash
# Check current training epoch status

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
RESULTS_DIR="results/yolov8s_rdd2022_phase1_mps"

echo "=========================================="
echo "📊 Training Epoch Status"
echo "=========================================="
echo ""

# Check if training is running
if ! pgrep -f "train_yolov8.py" > /dev/null; then
    echo "❌ Training process is NOT running"
    exit 1
fi

echo "✅ Training process is RUNNING"
echo ""

# Check for results.csv to determine completed epochs
if [ -f "$RESULTS_DIR/results.csv" ]; then
    EPOCH_COUNT=$(tail -n +2 "$RESULTS_DIR/results.csv" 2>/dev/null | wc -l | tr -d ' ')
    CURRENT_EPOCH=$((EPOCH_COUNT + 1))
    
    echo "📈 Completed Epochs: $EPOCH_COUNT"
    echo "🔄 Current Epoch: $CURRENT_EPOCH / 200"
    echo ""
    
    # Check latest epoch result
    if [ "$EPOCH_COUNT" -gt 0 ]; then
        echo "📊 Latest Epoch ($EPOCH_COUNT) Results:"
        tail -1 "$RESULTS_DIR/results.csv" | awk -F',' '{printf "   Train/Box Loss: %s\n   Train/Cls Loss: %s\n   Train/DFL Loss: %s\n   Metrics/mAP50(B): %s\n   Metrics/mAP50-95(B): %s\n", $4, $5, $6, $7, $8}' 2>/dev/null || tail -1 "$RESULTS_DIR/results.csv"
        echo ""
    fi
else
    echo "🔄 Current Status: Epoch 1 - Validation in progress"
    echo ""
    
    # Try to get validation progress from log
    VAL_BATCH=$(tail -100 "$LOG_FILE" 2>/dev/null | grep -oE "[0-9]+/895" | tail -1 | cut -d'/' -f1)
    if [ -n "$VAL_BATCH" ]; then
        PERCENT=$((VAL_BATCH * 100 / 895))
        echo "   Validation: Batch $VAL_BATCH/895 ($PERCENT%)"
    fi
fi

# Check for checkpoints
if [ -f "$RESULTS_DIR/weights/last.pt" ]; then
    echo "💾 Checkpoint saved:"
    ls -lh "$RESULTS_DIR/weights/last.pt" | awk '{print "   " $9 " (" $5 ")"}'
    echo ""
fi

if [ -f "$RESULTS_DIR/weights/best.pt" ]; then
    echo "⭐ Best model saved:"
    ls -lh "$RESULTS_DIR/weights/best.pt" | awk '{print "   " $9 " (" $5 ")"}'
    echo ""
fi

# Get current activity from log
LATEST_ACTIVITY=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -oE "Epoch.*[0-9]+/200|val.*[0-9]+/895|Training.*epoch" | head -1)
if [ -n "$LATEST_ACTIVITY" ]; then
    echo "🔄 Current Activity: $LATEST_ACTIVITY"
fi

echo ""
echo "=========================================="
