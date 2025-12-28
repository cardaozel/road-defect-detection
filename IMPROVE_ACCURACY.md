# How to Improve Accuracy - Step by Step Guide

## Current Results Analysis
Your current model shows:
- **mAP@0.5**: 0.2940 (29.4%) - This is your main accuracy metric
- **Precision**: 0.4918 (49.2%) - Half of predictions are correct
- **Recall**: 0.3034 (30.3%) - Finding about 30% of defects
- **F1 Score**: 0.3753 (37.5%) - Balanced metric
- **Balanced Accuracy**: 0.3976 (39.8%)

## What I've Updated

### 1. **Increased Training Epochs: 60 → 100**
   - More training time = better learning
   - No memory cost, just time

### 2. **Increased Image Size: 416 → 448**
   - Larger images = more detail = better accuracy
   - Still memory-safe for MPS

### 3. **Increased Augmentation:**
   - Mosaic: 0.75 → 0.9 (stronger data augmentation)
   - Mixup: 0.05 → 0.1 (better generalization)

### 4. **Adjusted Learning Rate Schedule:**
   - lrf: 0.1 → 0.01 (better fine-tuning in later epochs)

## How to Use the Updated Config

### Step 1: Train with New Config
```bash
python scripts/train_yolov8.py --config configs/training.yaml
```

**Expected improvements:**
- mAP@0.5 should reach **0.35-0.40** (35-40%)
- Precision should improve to **0.55-0.60**
- Recall should improve to **0.35-0.40**

### Step 2: If Training Gets Killed
```bash
# Resume from checkpoint (no progress lost!)
python scripts/train_yolov8.py --config configs/training.yaml --resume
```

### Step 3: Fine-Tune for Maximum Accuracy (Optional)
After initial training completes, fine-tune with even better settings:

```bash
# First, update the weights path in configs/training_finetune.yaml
# Then run fine-tuning:
python scripts/train_yolov8.py --config configs/training_finetune.yaml
```

**Fine-tuning benefits:**
- Uses your best model as starting point
- Lower learning rate (0.001) for precise adjustments
- Larger image size (512) if memory allows
- Can push mAP@0.5 to **0.40-0.50** (40-50%)

## Understanding the Metrics

### mAP@0.5 (Mean Average Precision)
- **Your target**: >0.40 (40%) for good performance
- **Excellent**: >0.50 (50%)
- This is the **most important** metric for object detection

### Precision
- **Your target**: >0.60 (60%)
- Measures: "How many of my predictions are correct?"
- High precision = fewer false alarms

### Recall
- **Your target**: >0.40 (40%)
- Measures: "How many defects did I find?"
- High recall = fewer missed defects

### F1 Score
- **Your target**: >0.45 (45%)
- Balances precision and recall
- Good single-number summary

### Balanced Accuracy
- **Your target**: >0.50 (50%)
- Simple average of precision and recall
- Easy to understand summary metric

## Additional Tips to Improve Accuracy

### 1. **Check Your Dataset**
- Ensure annotations are accurate
- Check for class imbalance (some defect types may be rare)
- Verify train/val split is good (80/20 or 70/30)

### 2. **Monitor Training**
- Watch validation metrics during training
- If mAP stops improving, model may be overfitting
- Early stopping can help prevent overfitting

### 3. **Try Different Models** (if memory allows)
- `yolov8s.pt` - Slightly larger, better accuracy
- `yolov8m.pt` - Much larger, best accuracy (may not fit on MPS)

### 4. **Post-Processing**
- Adjust confidence threshold (default 0.25)
- Adjust IoU threshold for NMS (default 0.7)
- Lower confidence = more detections (higher recall, lower precision)
- Higher confidence = fewer detections (higher precision, lower recall)

## Expected Timeline

- **Initial training (100 epochs)**: ~10-15 hours on MPS
- **Fine-tuning (30 epochs)**: ~3-5 hours on MPS
- **Total**: ~15-20 hours for maximum accuracy

## Quick Reference Commands

```bash
# Start training
python scripts/train_yolov8.py --config configs/training.yaml

# Resume if killed
python scripts/train_yolov8.py --config configs/training.yaml --resume

# Fine-tune after initial training
python scripts/train_yolov8.py --config configs/training_finetune.yaml

# Check results
cat results/yolov8n_rdd2022/evaluation/evaluation_summary.txt
```

## Troubleshooting

### If mAP is still low (<0.30):
1. Check dataset quality and annotations
2. Increase epochs to 150-200
3. Try different augmentation settings
4. Consider using a larger model (yolov8s)

### If training keeps getting killed:
1. Reduce image size to 384
2. Reduce mosaic to 0.5
3. Disable mixup (set to 0.0)
4. Close other applications

### If overfitting (val mAP decreases while train mAP increases):
1. Increase augmentation (mosaic, mixup)
2. Add more data if possible
3. Reduce epochs
4. Increase weight_decay
