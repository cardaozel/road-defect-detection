# Quick Start: High-Performance Training

## 🎯 Goal: Achieve Target Metrics

- **Recall ≥ 70%** (Current: 24%)
- **Precision ≥ 60%** (Current: 43.4%)
- **mAP@0.5 ≥ 60%** (Current: 19.3%)
- **mAP@0.5:0.95 ≥ 35%** (Current: 7.6%)

## 🚀 Quick Start

### Step 1: Download YOLOv8s Model

```bash
cd /Users/ardaozel/road_defect_detection
source .venv/bin/activate

# Download yolov8s.pt if you don't have it
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt')"
```

### Step 2: Start Training with Optimized Config

```bash
python scripts/train_yolov8.py \
    --config configs/training_optimized_high_performance.yaml \
    --project results \
    --run-name yolov8s_rdd2022_high_perf \
    --epochs 200 \
    --batch 4 \
    --imgsz 640
```

### Step 3: Monitor Progress

```bash
# Watch training in real-time
tail -f training_log.txt

# Or use the epoch monitor
./scripts/monitor_epochs.sh
```

## 🔧 Key Changes from Current Setup

| Parameter | Current | Optimized | Impact |
|-----------|---------|-----------|--------|
| **Model** | yolov8n (3.2M) | **yolov8s (11.2M)** | +15-20% mAP |
| **Image Size** | 416×416 | **640×640** | +10-15% mAP, +20-30% recall |
| **Batch Size** | 1 | **4** | Better convergence |
| **Epochs** | 100 | **200** | +5-10% mAP |
| **Confidence** | 0.25 (default) | **0.15** | +30-40% recall |
| **NMS IoU** | 0.7 | **0.6** | +10-15% recall |
| **Max Detections** | 150 | **300** | Better recall |
| **Mosaic** | 0.75 | **1.0** | +3-5% generalization |
| **Mixup** | 0.05 | **0.15** | +2-3% generalization |
| **Copy-Paste** | 0.0 | **0.1** | +2-3% generalization |
| **Cosine LR** | false | **true** | Better convergence |

## 📊 Expected Timeline

- **Epoch 50**: Recall ~45%, mAP@0.5 ~35%
- **Epoch 100**: Recall ~60%, mAP@0.5 ~50%
- **Epoch 150**: Recall ~68%, mAP@0.5 ~58%
- **Epoch 200**: **Recall ≥70%, mAP@0.5 ≥60%** ✅

## ⚠️ Memory Considerations

If you get OOM (Out of Memory) errors:

**Option 1: Reduce Batch Size**
```bash
--batch 2  # Instead of 4
```

**Option 2: Use YOLOv8n with 640×640**
```bash
# Edit config to use yolov8n.pt instead of yolov8s.pt
# This gives you higher resolution but less model capacity
```

**Option 3: Reduce Image Size Slightly**
```bash
--imgsz 608  # Instead of 640
```

## 🔍 Troubleshooting

### If Recall Still Low (< 60% after 100 epochs):

1. **Lower confidence threshold further:**
   ```yaml
   validation:
     conf: 0.1  # Even lower
   ```

2. **Check class imbalance:**
   ```bash
   python scripts/analyze_dataset.py
   ```

3. **Review annotation quality** - poor labels hurt recall

### If Precision Drops Too Much:

1. **Increase confidence threshold:**
   ```yaml
   validation:
     conf: 0.2  # Higher threshold
   ```

2. **Increase NMS IoU:**
   ```yaml
   validation:
     iou: 0.65  # More aggressive NMS
   ```

### If mAP@0.5:0.95 Still Low (< 30%):

1. **Consider YOLOv8m** (medium model) - more capacity
2. **Increase epochs to 250-300**
3. **Check dataset quality** - localization issues

## 📈 Monitoring Commands

```bash
# Check current metrics
./scripts/show_training_status.sh

# Check specific epoch
./scripts/check_epoch_completion.sh 100

# View results CSV
tail -20 results/yolov8s_rdd2022_high_perf/results.csv
```

## ✅ Success Criteria

Training is successful when ALL targets are met:
- ✅ Recall ≥ 70%
- ✅ Precision ≥ 60%
- ✅ mAP@0.5 ≥ 60%
- ✅ mAP@0.5:0.95 ≥ 35%

Once training completes, the evaluation script will automatically generate a comprehensive report with all metrics!

