# Where to Find Example Images and Graph Results

## 📊 Existing Graphs (Already Created by YOLO)

### Location:
```
results/yolov8s_rdd2022_high_perf/
```

### Available Graphs:
1. **`results.png`** ⭐ **MAIN TRAINING GRAPH**
   - Shows mAP@0.5, mAP@0.5:0.95, Precision, Recall curves
   - **This is the main graph you need for your thesis!**

2. **`BoxR_curve.png`**
   - Precision-Recall curve
   - Shows detection quality across confidence thresholds

3. **`confusion_matrix.png`**
   - Confusion matrix showing per-class performance
   - Useful for understanding which defect types are detected well

### View These Files:
```bash
# Open in Finder (macOS)
open results/yolov8s_rdd2022_high_perf/results.png
open results/yolov8s_rdd2022_high_perf/BoxR_curve.png
open results/yolov8s_rdd2022_high_perf/confusion_matrix.png
```

---

## 🖼️ Existing Detection Example Images

### Location:
```
results/yolov8s_rdd2022_high_perf/
```

### Available Images:
1. **`val_batch0_pred.jpg`** ⭐ **VALIDATION PREDICTIONS**
   - Shows detections on validation images
   - Has bounding boxes and labels

2. **`val_batch1_labels.jpg`**
   - Ground truth labels for comparison

3. **`val_batch2_pred.jpg`**
   - More validation predictions

4. **`train_batch*.jpg`**
   - Training batch images with augmentations

### View These Files:
```bash
# Open in Finder (macOS)
open results/yolov8s_rdd2022_high_perf/val_batch0_pred.jpg
open results/yolov8s_rdd2022_high_perf/val_batch2_pred.jpg
```

---

## 📈 To Create Additional Graphs

### Step 1: Install matplotlib
```bash
pip install matplotlib
```

### Step 2: Run graph creation script
```bash
python3 scripts/create_graphs_simple.py \
    results/yolov8s_rdd2022_high_perf/results.csv \
    results/yolov8s_rdd2022_high_perf/graphs
```

### Step 3: Find graphs here:
```
results/yolov8s_rdd2022_high_perf/graphs/
├── training_map_metrics.png      # mAP curves
├── training_precision_recall.png  # Precision/Recall curves
└── training_loss_curves.png      # Loss curves
```

---

## 🎯 To Create More Detection Samples

### Step 1: Install packages
```bash
pip install opencv-python ultralytics
```

### Step 2: Run detection script
```bash
python3 scripts/visualize_detections.py \
    --weights results/yolov8s_rdd2022_high_perf/weights/best.pt \
    --source data/yolo/rdd2022/val/images \
    --output-dir results/yolov8s_rdd2022_high_perf/detection_samples \
    --max-images 10
```

### Step 3: Find detection samples here:
```
results/yolov8s_rdd2022_high_perf/detection_samples/
├── detection_*.png  # Images with bounding boxes and labels
```

---

## 📁 Quick Reference

### For Thesis Graphs:
- **Main graph**: `results/yolov8s_rdd2022_high_perf/results.png` ✅ (Already exists!)
- **PR Curve**: `results/yolov8s_rdd2022_high_perf/BoxR_curve.png` ✅ (Already exists!)
- **Confusion Matrix**: `results/yolov8s_rdd2022_high_perf/confusion_matrix.png` ✅ (Already exists!)

### For Thesis Detection Examples:
- **Validation predictions**: `results/yolov8s_rdd2022_high_perf/val_batch0_pred.jpg` ✅ (Already exists!)
- **More examples**: `results/yolov8s_rdd2022_high_perf/val_batch2_pred.jpg` ✅ (Already exists!)

### To Create More:
- Run the scripts above to generate additional graphs and detection samples

---

## 🎨 Recommended Images for Thesis

### Chapter 5 (Results):
1. **`results.png`** - Main training progress graph
2. **`val_batch0_pred.jpg`** - Example detections (shows bounding boxes)
3. **`confusion_matrix.png`** - Per-class performance
4. **`BoxR_curve.png`** - Precision-Recall curve

### Chapter 4 (Methodology):
1. **`train_batch0.jpg`** - Example of data augmentation
2. **`val_batch1_labels.jpg`** - Ground truth labels

---

**All existing files are ready to use! You can open them directly from:**
```
/Users/ardaozel/road_defect_detection/results/yolov8s_rdd2022_high_perf/
```

