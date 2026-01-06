#!/bin/bash
# Real-time terminal display of high-performance training progress
# Shows metrics, progress bars, and comparisons with targets

cd "$(dirname "$0")/.."

RUN_NAME="yolov8s_rdd2022_high_perf"
RESULTS_CSV="results/${RUN_NAME}/results.csv"
TARGETS=(70 60 60 35)  # Recall, Precision, mAP@0.5, mAP@0.5:0.95 (as percentages)

# Colors for terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

while true; do
    clear
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║         HIGH-PERFORMANCE TRAINING MONITOR (200 Epochs)                   ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Check if training is running
    if ps aux | grep -v grep | grep -q "train_yolov8.py.*yolov8s_rdd2022_high_perf"; then
        echo -e "${GREEN}✅ Training Status: RUNNING${NC}"
        echo ""
        
        # Get latest epoch and metrics from CSV
        if [ -f "$RESULTS_CSV" ]; then
            LATEST_METRICS=$(tail -1 "$RESULTS_CSV" 2>/dev/null)
            if [ ! -z "$LATEST_METRICS" ]; then
                CURRENT_EPOCH=$(echo "$LATEST_METRICS" | awk -F',' '{print int($1)}')
                PRECISION=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.2f", $6*100}')
                RECALL=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.2f", $7*100}')
                MAP50=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.2f", $8*100}')
                MAP50_95=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.2f", $9*100}')
                BOX_LOSS=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.4f", $2}')
                CLS_LOSS=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.4f", $3}')
                DFL_LOSS=$(echo "$LATEST_METRICS" | awk -F',' '{printf "%.4f", $4}')
                
                # Calculate overall progress
                OVERALL_PROGRESS=$(awk "BEGIN {printf \"%.1f\", ($CURRENT_EPOCH/200)*100}")
                
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo -e "${CYAN}📊 EPOCH PROGRESS${NC}"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "  Current Epoch:    ${CURRENT_EPOCH}/200"
                echo "  Overall Progress: ${OVERALL_PROGRESS}%"
                echo ""
                
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo -e "${CYAN}📈 CURRENT METRICS (Epoch ${CURRENT_EPOCH})${NC}"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                
                # Precision
                if (( $(echo "$PRECISION >= ${TARGETS[1]}" | bc -l) )); then
                    COLOR=$GREEN
                    STATUS="✅"
                elif (( $(echo "$PRECISION >= $(echo "scale=0; ${TARGETS[1]} * 0.7" | bc)" | bc -l) )); then
                    COLOR=$YELLOW
                    STATUS="⚠️"
                else
                    COLOR=$RED
                    STATUS="❌"
                fi
                echo -e "  Precision:        ${COLOR}${PRECISION}%${NC} ${STATUS} (Target: ≥${TARGETS[1]}%)"
                
                # Recall
                if (( $(echo "$RECALL >= ${TARGETS[0]}" | bc -l) )); then
                    COLOR=$GREEN
                    STATUS="✅"
                elif (( $(echo "$RECALL >= $(echo "scale=0; ${TARGETS[0]} * 0.7" | bc)" | bc -l) )); then
                    COLOR=$YELLOW
                    STATUS="⚠️"
                else
                    COLOR=$RED
                    STATUS="❌"
                fi
                echo -e "  Recall:           ${COLOR}${RECALL}%${NC} ${STATUS} (Target: ≥${TARGETS[0]}%)"
                
                # mAP@0.5
                if (( $(echo "$MAP50 >= ${TARGETS[2]}" | bc -l) )); then
                    COLOR=$GREEN
                    STATUS="✅"
                elif (( $(echo "$MAP50 >= $(echo "scale=0; ${TARGETS[2]} * 0.7" | bc)" | bc -l) )); then
                    COLOR=$YELLOW
                    STATUS="⚠️"
                else
                    COLOR=$RED
                    STATUS="❌"
                fi
                echo -e "  mAP@0.5:          ${COLOR}${MAP50}%${NC} ${STATUS} (Target: ≥${TARGETS[2]}%)"
                
                # mAP@0.5:0.95
                if (( $(echo "$MAP50_95 >= ${TARGETS[3]}" | bc -l) )); then
                    COLOR=$GREEN
                    STATUS="✅"
                elif (( $(echo "$MAP50_95 >= $(echo "scale=0; ${TARGETS[3]} * 0.7" | bc)" | bc -l) )); then
                    COLOR=$YELLOW
                    STATUS="⚠️"
                else
                    COLOR=$RED
                    STATUS="❌"
                fi
                echo -e "  mAP@0.5:0.95:     ${COLOR}${MAP50_95}%${NC} ${STATUS} (Target: ≥${TARGETS[3]}%)"
                echo ""
                
                # Training losses
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo -e "${CYAN}📉 TRAINING LOSSES${NC}"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "  Box Loss:         ${BOX_LOSS}"
                echo "  Class Loss:       ${CLS_LOSS}"
                echo "  DFL Loss:         ${DFL_LOSS}"
                echo ""
                
                # Process info
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo -e "${CYAN}💻 PROCESS INFO${NC}"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                ps aux | grep -v grep | grep "train_yolov8.py.*yolov8s_rdd2022_high_perf" | awk '{
                    printf "  PID: %s | CPU: %s%% | Memory: %s%% | Runtime: %s\n", $2, $3, $4, $10
                }'
                
                # Remaining epochs
                REMAINING=$((200 - CURRENT_EPOCH))
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo -e "${CYAN}⏱️  ESTIMATED REMAINING${NC}"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "  Epochs Remaining: ${REMAINING}"
                echo ""
            else
                echo "  Training started, waiting for first epoch to complete..."
            fi
        else
            echo "  Training started, waiting for results..."
        fi
        
    else
        echo -e "${RED}❌ Training Status: NOT RUNNING${NC}"
        echo ""
        
        # Check if completed
        if [ -f "results/${RUN_NAME}/weights/best.pt" ]; then
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo -e "${GREEN}🎉 TRAINING COMPLETED!${NC}"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "Best model saved at: results/${RUN_NAME}/weights/best.pt"
            echo ""
            
            if [ -f "$RESULTS_CSV" ]; then
                FINAL_METRICS=$(tail -1 "$RESULTS_CSV" 2>/dev/null)
                if [ ! -z "$FINAL_METRICS" ]; then
                    PRECISION=$(echo "$FINAL_METRICS" | awk -F',' '{printf "%.2f", $6*100}')
                    RECALL=$(echo "$FINAL_METRICS" | awk -F',' '{printf "%.2f", $7*100}')
                    MAP50=$(echo "$FINAL_METRICS" | awk -F',' '{printf "%.2f", $8*100}')
                    MAP50_95=$(echo "$FINAL_METRICS" | awk -F',' '{printf "%.2f", $9*100}')
                    
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo -e "${CYAN}📊 FINAL METRICS${NC}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "  Precision:        ${PRECISION}% (Target: ≥${TARGETS[1]}%)"
                    echo "  Recall:           ${RECALL}% (Target: ≥${TARGETS[0]}%)"
                    echo "  mAP@0.5:          ${MAP50}% (Target: ≥${TARGETS[2]}%)"
                    echo "  mAP@0.5:0.95:     ${MAP50_95}% (Target: ≥${TARGETS[3]}%)"
                fi
            fi
        fi
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}Press Ctrl+C to exit${NC}"
    echo "Refreshing every 5 seconds..."
    
    sleep 5
done
