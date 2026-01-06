# Automatic Training Monitor Guide

## Overview

The automatic training monitor will:
1. ✅ Wait for current training (100/100) to complete
2. ✅ Extract and evaluate final metrics
3. ✅ Compare against target metrics:
   - Recall ≥ 70%
   - Precision ≥ 60%
   - mAP@0.5 ≥ 60%
   - mAP@0.5:0.95 ≥ 35%
4. ✅ Auto-start high-performance training if targets not met
5. ✅ Auto-resume training if it gets killed (no user intervention needed)

## How It Works

### Decision Logic

The monitor checks if metrics are "very away" from targets (below 70% of target):
- If **ANY** metric is below 70% of target → Start high-performance training
- If all metrics are above 70% of target → Continue current training

Example:
- Target Recall: 70%
- Threshold: 70% × 0.7 = 49%
- If actual Recall < 49% → Start new training
- If actual Recall ≥ 49% → Keep current training

### Auto-Resume

When high-performance training starts:
- **Auto-resume enabled**: If training gets killed, it automatically restarts
- **No user intervention**: Runs completely autonomously
- **Checkpoint-based**: Resumes from last saved checkpoint

## Usage

### Start the Monitor (Recommended)

```bash
./scripts/start_auto_monitor.sh
```

This will:
1. Monitor current training until completion
2. Evaluate results automatically
3. Start new training if needed
4. Auto-resume if killed

### Run in Background (Optional)

```bash
nohup ./scripts/start_auto_monitor.sh > logs/monitor_output.log 2>&1 &
```

Then monitor with:
```bash
tail -f logs/monitor_output.log
tail -f logs/auto_train_monitor.log
```

## What Happens

### Scenario 1: Current Training Meets Targets (Unlikely)
```
Current training completes → Metrics evaluated → All targets met → Stop ✅
```

### Scenario 2: Current Training Below Targets (Expected)
```
Current training completes (100/100)
  ↓
Metrics evaluated
  ↓
Recall: 24% < 49% threshold ❌
  ↓
Start high-performance training automatically
  ↓
Monitor continuously
  ↓
If killed → Auto-resume immediately
  ↓
Continue until 200 epochs complete
```

## Monitoring

### View Monitor Logs

```bash
# Main monitor log
tail -f logs/auto_train_monitor.log

# Training log
tail -f training_log.txt

# Combined
tail -f logs/auto_train_monitor.log training_log.txt
```

### Check Current Status

```bash
# Check if monitor is running
ps aux | grep auto_monitor_and_train

# Check if training is running
ps aux | grep train_yolov8

# Check latest metrics
tail -5 results/yolov8s_rdd2022_high_perf/results.csv
```

## High-Performance Training Configuration

When auto-started, training uses:

- **Model**: YOLOv8s (small) - 11.2M parameters
- **Image Size**: 640×640 pixels
- **Batch Size**: 4
- **Epochs**: 200
- **Confidence**: 0.15 (optimized for recall)
- **NMS IoU**: 0.6 (less aggressive)
- **Max Detections**: 300
- **Auto-Resume**: Enabled

## Expected Timeline

### Current Training (in progress)
- **Status**: Epoch 94/100
- **ETA**: ~2-3 hours to complete
- **Expected Results**: Below targets (will trigger new training)

### High-Performance Training (auto-started)
- **Duration**: ~40-50 hours (200 epochs)
- **Expected Progress**:
  - Epoch 50: Recall ~45%, mAP@0.5 ~35%
  - Epoch 100: Recall ~60%, mAP@0.5 ~50%
  - Epoch 150: Recall ~68%, mAP@0.5 ~58%
  - Epoch 200: **Recall ≥70%, mAP@0.5 ≥60%** ✅

## Troubleshooting

### Monitor Not Starting

```bash
# Check Python path
which python3

# Check dependencies
python3 -c "import yaml; print('OK')"

# Run manually to see errors
python3 scripts/auto_monitor_and_train.py
```

### Training Not Resuming

Check logs:
```bash
tail -50 logs/auto_train_monitor.log
```

Manual resume if needed:
```bash
source .venv/bin/activate
python scripts/train_yolov8.py \
    --config configs/training_optimized_high_performance.yaml \
    --project results \
    --run-name yolov8s_rdd2022_high_perf \
    --epochs 200 \
    --resume
```

### Stop Monitor

```bash
# Find monitor process
ps aux | grep auto_monitor_and_train

# Kill monitor (training will continue independently)
kill <PID>
```

## Files Created

- `scripts/auto_monitor_and_train.py` - Main monitor script
- `scripts/start_auto_monitor.sh` - Startup script
- `logs/auto_train_monitor.log` - Monitor logs
- `logs/monitor_output.log` - Output logs (if run in background)

## Summary

Just run:
```bash
./scripts/start_auto_monitor.sh
```

Then:
- ✅ Monitor will handle everything automatically
- ✅ Training will auto-resume if killed
- ✅ No user intervention needed
- ✅ Will continue until targets are met or manually stopped

The system is fully autonomous! 🚀

