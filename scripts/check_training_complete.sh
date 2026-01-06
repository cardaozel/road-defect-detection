#!/bin/bash
# Check if training is complete and show metrics

RESULTS_DIR="results/yolov8n_rdd202215"
EVAL_DIR="$RESULTS_DIR/evaluation"

# Check if training process is still running
if ps aux | grep -v grep | grep -q "train_yolov8.py"; then
    echo "Training is still running..."
    exit 0
fi

# Check if evaluation reports exist
if [ -f "$EVAL_DIR/evaluation_summary.txt" ]; then
    echo "=" 
    echo "TRAINING COMPLETED - METRICS SUMMARY"
    echo "="
    cat "$EVAL_DIR/evaluation_summary.txt"
    echo ""
    echo "Full reports available at:"
    echo "  - $EVAL_DIR/evaluation_summary.txt"
    echo "  - $EVAL_DIR/evaluation_report.json"
    echo "  - $EVAL_DIR/evaluation_report.yaml"
elif [ -f "$RESULTS_DIR/weights/best.pt" ]; then
    echo "Training appears complete but evaluation not yet done."
    echo "Best model saved at: $RESULTS_DIR/weights/best.pt"
else
    echo "Training status unclear. Check training_log.txt"
fi

