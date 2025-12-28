#!/bin/bash
# Monitor training and alert when epoch 1 completes

cd "$(dirname "$0")/.."

LOG_FILE="training_log.txt"
RESULTS_DIR="results/yolov8s_rdd2022_phase1_mps"

echo "Monitoring training progress..."
echo "Waiting for epoch 1 to complete..."
echo ""

# Function to check if epoch 1 is complete
check_epoch_complete() {
    # Check if results.csv exists (created after first epoch validation)
    if [ -f "$RESULTS_DIR/results.csv" ]; then
        # Check if we have at least 2 epochs worth of data (epoch 0 is initial, epoch 1 is first training epoch)
        local epoch_count=$(tail -n +2 "$RESULTS_DIR/results.csv" 2>/dev/null | wc -l)
        if [ "$epoch_count" -ge 1 ]; then
            return 0  # Epoch 1 complete
        fi
    fi
    
    # Also check if last.pt exists (checkpoint saved after each epoch)
    if [ -f "$RESULTS_DIR/weights/last.pt" ]; then
        # Check log for validation output which indicates epoch 1 completion
        if tail -100 "$LOG_FILE" 2>/dev/null | grep -qE "2/200|val.*map|Epoch.*2/200"; then
            return 0  # Epoch 1 complete
        fi
    fi
    
    return 1  # Not complete yet
}

# Function to get current progress
get_current_progress() {
    local current_batch=$(tail -1 "$LOG_FILE" 2>/dev/null | grep -oE "[0-9]+/9545" | cut -d'/' -f1)
    if [ -z "$current_batch" ]; then
        echo "0"
    else
        echo "$current_batch"
    fi
}

# Function to show progress
show_progress() {
    local current=$(get_current_progress)
    local total=9545
    local percent=$((current * 100 / total))
    
    echo -ne "\r\033[KCurrent progress: Batch $current/$total (${percent}%) - Epoch 1/200"
}

# Monitor loop
LAST_BATCH=0
while true; do
    # Check if training process is still running
    if ! pgrep -f "train_yolov8.py" > /dev/null; then
        echo ""
        echo "❌ Training process stopped!"
        exit 1
    fi
    
    # Show current progress
    show_progress
    
    # Check if epoch 1 is complete
    if check_epoch_complete; then
        echo ""
        echo ""
        echo "✅ ============================================"
        echo "✅  EPOCH 1 COMPLETED!"
        echo "✅ ============================================"
        echo ""
        
        # Show epoch 1 results
        if [ -f "$RESULTS_DIR/results.csv" ]; then
            echo "📊 Epoch 1 Results:"
            echo ""
            # Show header and first epoch result
            head -2 "$RESULTS_DIR/results.csv" | column -t -s, 2>/dev/null || head -2 "$RESULTS_DIR/results.csv"
            echo ""
        fi
        
        # Show checkpoint info
        if [ -f "$RESULTS_DIR/weights/last.pt" ]; then
            echo "💾 Checkpoint saved: $RESULTS_DIR/weights/last.pt"
            ls -lh "$RESULTS_DIR/weights/last.pt"
            echo ""
        fi
        
        if [ -f "$RESULTS_DIR/weights/best.pt" ]; then
            echo "⭐ Best model saved: $RESULTS_DIR/weights/best.pt"
            ls -lh "$RESULTS_DIR/weights/best.pt"
            echo ""
        fi
        
        echo "Training will continue to epoch 2..."
        echo ""
        echo "To monitor further progress:"
        echo "  tail -f $LOG_FILE"
        echo ""
        
        # Make a notification sound (macOS)
        if command -v say >/dev/null 2>&1; then
            say "Epoch one training completed" 2>/dev/null &
        fi
        
        exit 0
    fi
    
    sleep 10  # Check every 10 seconds
done
