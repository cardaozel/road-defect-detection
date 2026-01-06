#!/bin/bash
# Monitor training and alert on each epoch completion
# Usage: ./scripts/monitor_epochs.sh

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
PROJECT_DIR="results/yolov8n_rdd202215"
LAST_EPOCH=0

echo "╔════════════════════════════════════════════════════════╗"
echo "║     EPOCH-BY-EPOCH TRAINING MONITOR                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Monitoring training progress..."
echo "I'll notify you when each epoch completes!"
echo ""
echo "Press Ctrl+C to exit"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to extract current epoch from log
get_current_epoch() {
    tail -100 "$LOG_FILE" 2>/dev/null | grep -oE "^\s+[0-9]+/100" | tail -1 | grep -oE "[0-9]+" | head -1 || echo "0"
}

# Function to get epoch metrics
get_epoch_metrics() {
    local epoch=$1
    # Look for validation results after this epoch
    tail -200 "$LOG_FILE" 2>/dev/null | grep -A 5 "Epoch $epoch" | head -10
}

# Initial check
if ! ps aux | grep -v grep | grep -q "train_yolov8.py"; then
    echo "❌ Training process not found!"
    exit 1
fi

echo "✅ Training detected! Monitoring epochs..."
echo ""

# Monitor loop
while true; do
    if ! ps aux | grep -v grep | grep -q "train_yolov8.py"; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⚠️  Training process stopped!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        if [ -f "$PROJECT_DIR/weights/best.pt" ]; then
            echo ""
            echo "✅ Training appears to have completed!"
            echo "   Best model: $PROJECT_DIR/weights/best.pt"
            echo ""
            if [ -f "$PROJECT_DIR/evaluation/evaluation_summary.txt" ]; then
                echo "📊 Final Metrics:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                cat "$PROJECT_DIR/evaluation/evaluation_summary.txt" | grep -E "mAP@0.5|mAP@0.5:0.95|Precision|Recall|F1" | head -10
            fi
        fi
        break
    fi
    
    CURRENT_EPOCH=$(get_current_epoch)
    
    if [ ! -z "$CURRENT_EPOCH" ] && [ "$CURRENT_EPOCH" != "0" ]; then
        # Check if we moved to a new epoch
        if [ "$CURRENT_EPOCH" -gt "$LAST_EPOCH" ]; then
            if [ "$LAST_EPOCH" -gt 0 ]; then
                # Previous epoch completed!
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "🎉 EPOCH $LAST_EPOCH COMPLETED! 🎉"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                
                # Try to get validation metrics
                VAL_METRICS=$(tail -500 "$LOG_FILE" 2>/dev/null | grep -A 10 "Epoch.*$LAST_EPOCH.*val" | head -5)
                if [ ! -z "$VAL_METRICS" ]; then
                    echo "Validation Results:"
                    echo "$VAL_METRICS" | grep -E "train/|val/" | head -3
                    echo ""
                fi
                
                PROGRESS_PERCENT=$((LAST_EPOCH * 100 / 100))
                echo "Progress: $LAST_EPOCH/100 epochs ($PROGRESS_PERCENT%)"
                REMAINING=$((100 - LAST_EPOCH))
                echo "Remaining: $REMAINING epochs"
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            fi
            
            LAST_EPOCH=$CURRENT_EPOCH
            
            # Show current epoch status
            PROGRESS=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -oE "[0-9]+/19089" | tail -1 | cut -d'/' -f1 || echo "0")
            if [ ! -z "$PROGRESS" ] && [ "$PROGRESS" != "0" ]; then
                EPOCH_PERCENT=$(awk "BEGIN {printf \"%.1f\", ($PROGRESS/19089)*100}")
                echo "📊 Epoch $CURRENT_EPOCH/100: ${EPOCH_PERCENT}% complete"
                
                # Get latest metrics
                LATEST=$(tail -1 "$LOG_FILE" 2>/dev/null)
                if echo "$LATEST" | grep -q "$CURRENT_EPOCH/100"; then
                    BOX_LOSS=$(echo "$LATEST" | awk '{print $3}')
                    CLS_LOSS=$(echo "$LATEST" | awk '{print $4}')
                    DFL_LOSS=$(echo "$LATEST" | awk '{print $5}')
                    SPEED=$(echo "$LATEST" | grep -oE "[0-9]+\.[0-9]+it/s" | head -1)
                    
                    echo "   Box Loss: $BOX_LOSS | Class Loss: $CLS_LOSS | DFL Loss: $DFL_LOSS"
                    echo "   Speed: $SPEED"
                fi
            else
                echo "📊 Epoch $CURRENT_EPOCH/100: Starting..."
            fi
        elif [ "$CURRENT_EPOCH" -eq "$LAST_EPOCH" ]; then
            # Same epoch, update progress
            PROGRESS=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -oE "[0-9]+/19089" | tail -1 | cut -d'/' -f1 || echo "0")
            if [ ! -z "$PROGRESS" ] && [ "$PROGRESS" != "0" ]; then
                EPOCH_PERCENT=$(awk "BEGIN {printf \"%.1f\", ($PROGRESS/19089)*100}")
                # Only update if progress changed significantly (to reduce flicker)
                echo -ne "\r📊 Epoch $CURRENT_EPOCH/100: ${EPOCH_PERCENT}% complete... "
            fi
        fi
    fi
    
    sleep 5
done

