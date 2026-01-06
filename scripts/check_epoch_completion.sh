#!/bin/bash
# Check if a specific epoch has completed
# Usage: ./scripts/check_epoch_completion.sh [epoch_number]

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
EPOCH_TO_CHECK=${1:-94}

echo "Checking for epoch $EPOCH_TO_CHECK completion..."

# Check if we've moved past this epoch
CURRENT_EPOCH=$(tail -100 "$LOG_FILE" 2>/dev/null | grep -oE "^\s+[0-9]+/100" | tail -1 | grep -oE "[0-9]+" | head -1)

if [ ! -z "$CURRENT_EPOCH" ]; then
    if [ "$CURRENT_EPOCH" -gt "$EPOCH_TO_CHECK" ]; then
        echo "✅ Epoch $EPOCH_TO_CHECK has completed!"
        echo "   Current epoch: $CURRENT_EPOCH/100"
        
        # Try to show validation results
        echo ""
        echo "Validation metrics for epoch $EPOCH_TO_CHECK:"
        tail -500 "$LOG_FILE" 2>/dev/null | grep -A 5 "Epoch.*$EPOCH_TO_CHECK.*val" | head -8
    elif [ "$CURRENT_EPOCH" -eq "$EPOCH_TO_CHECK" ]; then
        PROGRESS=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -oE "[0-9]+/19089" | tail -1 | cut -d'/' -f1 || echo "0")
        if [ ! -z "$PROGRESS" ]; then
            EPOCH_PERCENT=$(awk "BEGIN {printf \"%.1f\", ($PROGRESS/19089)*100}")
            echo "⏳ Epoch $EPOCH_TO_CHECK is still running..."
            echo "   Progress: ${EPOCH_PERCENT}%"
        else
            echo "⏳ Epoch $EPOCH_TO_CHECK is starting..."
        fi
    else
        echo "⏳ Epoch $EPOCH_TO_CHECK has not started yet."
        echo "   Current epoch: $CURRENT_EPOCH/100"
    fi
else
    echo "⚠️  Could not determine current epoch from log."
fi

