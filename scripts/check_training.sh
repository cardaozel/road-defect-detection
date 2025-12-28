#!/bin/bash
# Check training status

cd "$(dirname "$0")/.."

echo "Training Status Check"
echo "===================="
echo ""

# Check if process is running
if pgrep -f "train_yolov8.py" > /dev/null; then
    echo "✅ Training process IS RUNNING"
    echo ""
    ps aux | grep "train_yolov8.py" | grep -v grep | awk '{print "PID: " $2 " | CPU: " $3 "% | Memory: " $4 "% | Started: " $9}'
    echo ""
    
    # Check latest log entry
    if [ -f training_log.txt ]; then
        echo "Latest log entry:"
        tail -3 training_log.txt
        echo ""
    fi
    
    # Check for checkpoint
    if [ -f "results/yolov8s_rdd2022_phase1_mps/weights/last.pt" ]; then
        echo "✅ Checkpoint found: last.pt exists"
        ls -lh results/yolov8s_rdd2022_phase1_mps/weights/last.pt
    else
        echo "⚠️  No checkpoint yet (still in epoch 1)"
    fi
    
    echo ""
    echo "Training is running in the background."
    echo "To view live logs: tail -f training_log.txt"
else
    echo "❌ Training process is NOT running"
    echo ""
    echo "To restart:"
    echo "  ./scripts/start_safe_training.sh"
    echo ""
    echo "To resume (if checkpoint exists):"
    echo "  python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml --resume"
fi
