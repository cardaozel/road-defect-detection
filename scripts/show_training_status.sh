#!/bin/bash
# Quick training status display

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
PROJECT_DIR="results/yolov8n_rdd202215"

clear
echo "╔════════════════════════════════════════════════════════╗"
echo "║        TRAINING STATUS UPDATE                          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check if training is running
if ps aux | grep -v grep | grep -q "train_yolov8.py"; then
    echo "✅ Status: TRAINING IS RUNNING"
    echo ""
    
    # Get latest epoch and progress
    LATEST=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -E "^\s+[0-9]+/100" | tail -1)
    
    if [ ! -z "$LATEST" ]; then
        EPOCH=$(echo "$LATEST" | grep -oP '\d+/100' | head -1)
        PROGRESS=$(echo "$LATEST" | grep -oP '\d+%' | head -1)
        BOX_LOSS=$(echo "$LATEST" | awk '{print $3}')
        CLS_LOSS=$(echo "$LATEST" | awk '{print $4}')
        DFL_LOSS=$(echo "$LATEST" | awk '{print $5}')
        SPEED=$(echo "$LATEST" | grep -oP '\d+\.\d+it/s' | head -1)
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📊 CURRENT PROGRESS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  Epoch:         $EPOCH"
        echo "  Progress:      $PROGRESS of current epoch"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📈 TRAINING METRICS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  Box Loss:      $BOX_LOSS"
        echo "  Class Loss:    $CLS_LOSS"
        echo "  DFL Loss:      $DFL_LOSS"
        echo "  Speed:         $SPEED"
        echo ""
        
        # Calculate remaining epochs
        CURRENT=$(echo "$EPOCH" | cut -d'/' -f1)
        REMAINING=$((100 - CURRENT))
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⏱️  ESTIMATED"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  Remaining:     ~$REMAINING epochs"
        
        # Show process info
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "💻 PROCESS INFO"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ps aux | grep -v grep | grep "train_yolov8.py" | awk '{
            printf "  PID: %s | CPU: %s%% | Mem: %s%% | Runtime: %s\n", $2, $3, $4, $10
        }'
    else
        echo "  Initializing or waiting for data..."
    fi
else
    echo "❌ Status: TRAINING IS NOT RUNNING"
    echo ""
    
    # Check if completed
    if [ -f "$PROJECT_DIR/weights/best.pt" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🎉 TRAINING COMPLETED!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Best model: $PROJECT_DIR/weights/best.pt"
        
        if [ -f "$PROJECT_DIR/evaluation/evaluation_summary.txt" ]; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📊 FINAL METRICS"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            grep -E "mAP@0.5|mAP@0.5:0.95|Precision|Recall|F1|Accuracy" "$PROJECT_DIR/evaluation/evaluation_summary.txt" 2>/dev/null | head -8
        fi
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Tip: Run this script again for latest updates"
echo "   Command: ./scripts/show_training_status.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

