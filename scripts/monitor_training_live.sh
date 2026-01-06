#!/bin/bash
# Live monitoring script for training progress

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
PROJECT_DIR="results/yolov8n_rdd202215"

echo "=========================================="
echo "  TRAINING PROGRESS MONITOR"
echo "=========================================="
echo ""

while true; do
    clear
    echo "=========================================="
    echo "  TRAINING PROGRESS MONITOR"
    echo "=========================================="
    echo ""
    echo "Last update: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Check if training is running
    if ps aux | grep -v grep | grep -q "train_yolov8.py"; then
        echo "✓ Training is RUNNING"
        echo ""
        
        # Get current epoch from log
        CURRENT_EPOCH=$(tail -20 "$LOG_FILE" 2>/dev/null | grep -oP '\d+/100' | tail -1 | cut -d'/' -f1 || echo "?")
        TOTAL_EPOCHS="100"
        
        if [ ! -z "$CURRENT_EPOCH" ] && [ "$CURRENT_EPOCH" != "?" ]; then
            # Get progress percentage
            PROGRESS=$(tail -5 "$LOG_FILE" 2>/dev/null | grep -oP '\d+/19089' | tail -1 | cut -d'/' -f1 || echo "0")
            if [ ! -z "$PROGRESS" ]; then
                EPOCH_PROGRESS=$(awk "BEGIN {printf \"%.1f\", ($PROGRESS/19089)*100}")
            else
                EPOCH_PROGRESS="0"
            fi
            
            # Calculate remaining epochs
            REMAINING=$((100 - CURRENT_EPOCH))
            
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "  EPOCH PROGRESS"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "  Current Epoch:    $CURRENT_EPOCH/$TOTAL_EPOCHS"
            echo "  Epoch Progress:   ${EPOCH_PROGRESS}%"
            echo "  Remaining:        $REMAINING epochs"
            echo ""
            
            # Get latest metrics
            LATEST=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -E "^\s+[0-9]+/100" | tail -1)
            if [ ! -z "$LATEST" ]; then
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "  LATEST METRICS"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "$LATEST" | awk '{
                    if (match($0, /([0-9]+\/[0-9]+)/)) {print "  Epoch: " substr($0, RSTART, RLENGTH)}
                    if (match($0, /([0-9]+\.[0-9]+G)/)) {print "  GPU Memory: " substr($0, RSTART, RLENGTH)}
                    print "  Box Loss: " $3
                    print "  Class Loss: " $4
                    print "  DFL Loss: " $5
                    if (match($0, /([0-9]+%)/)) {print "  Progress: " substr($0, RSTART, RLENGTH)}
                    if (match($0, /([0-9]+\.[0-9]+it\/s)/)) {print "  Speed: " substr($0, RSTART, RLENGTH)}
                }'
                echo ""
            fi
            
            # Estimate time remaining
            if [ ! -z "$LATEST" ] && echo "$LATEST" | grep -q "<"; then
                ETA=$(echo "$LATEST" | grep -oP '<\d+:\d+' | head -1 || echo "")
                if [ ! -z "$ETA" ]; then
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "  ETA for Current Epoch: ${ETA}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                fi
            fi
            
        else
            echo "  Status: Starting up or initializing..."
        fi
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  PROCESS INFO"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ps aux | grep -v grep | grep "train_yolov8.py" | awk '{
            printf "  PID: %s\n", $2
            printf "  CPU: %s%%\n", $3
            printf "  Memory: %s%%\n", $4
            printf "  Runtime: %s\n", $10
        }'
        
    else
        echo "✗ Training is NOT running"
        echo ""
        
        # Check if training completed
        if [ -f "$PROJECT_DIR/weights/best.pt" ]; then
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "  TRAINING COMPLETED!"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "Best model saved at:"
            echo "  $PROJECT_DIR/weights/best.pt"
            echo ""
            
            # Check for evaluation reports
            if [ -f "$PROJECT_DIR/evaluation/evaluation_summary.txt" ]; then
                echo "Evaluation report available at:"
                echo "  $PROJECT_DIR/evaluation/evaluation_summary.txt"
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "  QUICK METRICS SUMMARY"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                head -30 "$PROJECT_DIR/evaluation/evaluation_summary.txt" 2>/dev/null | grep -E "mAP|Precision|Recall|F1|Accuracy" | head -10
            fi
        fi
    fi
    
    echo ""
    echo "Press Ctrl+C to exit monitor"
    echo "Updating every 10 seconds..."
    sleep 10
done

