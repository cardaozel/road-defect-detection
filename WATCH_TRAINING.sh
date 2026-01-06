#!/bin/bash
# Simple script to watch training progress
# Usage: ./WATCH_TRAINING.sh

cd "$(dirname "$0")"

echo "=========================================="
echo "  TRAINING MONITOR (Press Ctrl+C to exit)"
echo "=========================================="
echo ""

while true; do
    clear
    echo "=========================================="
    echo "  TRAINING PROGRESS - $(date '+%H:%M:%S')"
    echo "=========================================="
    echo ""
    
    if ps aux | grep -v grep | grep -q "train_yolov8.py"; then
        echo "✅ Training: RUNNING"
        echo ""
        
        # Get latest status
        LATEST=$(tail -1 training_log.txt 2>/dev/null)
        if echo "$LATEST" | grep -q "94/100"; then
            EPOCH_PROGRESS=$(echo "$LATEST" | grep -oE "[0-9]+%")
            ITERATIONS=$(echo "$LATEST" | grep -oE "[0-9]+/19089" | head -1)
            SPEED=$(echo "$LATEST" | grep -oE "[0-9]+\.[0-9]+it/s" | head -1)
            
            echo "Epoch: 94/100"
            echo "Progress: $EPOCH_PROGRESS ($ITERATIONS)"
            echo "Speed: $SPEED"
        fi
        
        echo ""
        echo "Process Info:"
        ps aux | grep -v grep | grep "train_yolov8.py" | awk '{printf "  PID: %s | CPU: %s%% | Mem: %s%%\n", $2, $3, $4}'
    else
        echo "❌ Training: NOT RUNNING"
        if [ -f "results/yolov8n_rdd202215/weights/best.pt" ]; then
            echo ""
            echo "✅ Training appears complete!"
            echo "Best model: results/yolov8n_rdd202215/weights/best.pt"
        fi
    fi
    
    echo ""
    echo "Refreshing every 10 seconds..."
    sleep 10
done

