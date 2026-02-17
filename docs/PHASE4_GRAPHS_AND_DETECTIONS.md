# Phase 4: Graphs and Detection Samples for Thesis

## Summary

### 1. Model Selection for Thesis

**For iOS App (Deployment):**
- Use: `best.pt` (Epoch 119)
- **mAP@0.5: 49.19%**
- **Precision: 60.43%**
- **Recall: 47.22%**

**For Thesis Documentation:**
- Mention **BOTH** `best.pt` and `last.pt` appropriately
- See `PHASE4_MODEL_SELECTION.md` for detailed guidance

---

## 2. Creating Training Graphs

### Install Required Packages:
```bash
pip install matplotlib
```

### Run Graph Creation:
```bash
python3 scripts/create_graphs_simple.py \
    results/yolov8s_rdd2022_high_perf/results.csv \
    results/yolov8s_rdd2022_high_perf/graphs
```

### Graphs Created:
1. **training_map_metrics.png** - mAP@0.5 and mAP@0.5:0.95 over epochs
2. **training_precision_recall.png** - Precision and Recall curves
3. **training_loss_curves.png** - Training and validation loss

### Where to Use in Thesis:
- **Chapter 4 (Methodology)**: Show training strategy and loss curves
- **Chapter 5 (Results)**: Show mAP, Precision, Recall progression graphs

---

## 3. Creating Detection Samples

### Install Required Packages:
```bash
pip install opencv-python ultralytics
```

### Run Detection Test:
```bash
python3 scripts/visualize_detections.py \
    --weights results/yolov8s_rdd2022_high_perf/weights/best.pt \
    --source data/yolo/rdd2022/val/images \
    --output-dir results/yolov8s_rdd2022_high_perf/detection_samples \
    --imgsz 640 \
    --conf 0.25 \
    --max-images 10
```

### Alternative (Using YOLO directly):
```python
from ultralytics import YOLO

# Load best model
model = YOLO('results/yolov8s_rdd2022_high_perf/weights/best.pt')

# Run inference on validation images
results = model.predict(
    source='data/yolo/rdd2022/val/images',
    save=True,
    conf=0.25,
    imgsz=640,
    save_dir='results/yolov8s_rdd2022_high_perf/detection_samples'
)
```

### Detection Samples Will Show:
- Bounding boxes around detected defects
- Class labels (D00, D01, D10, D11, D20, D40)
- Confidence scores
- Color-coded by defect type

### Where to Use in Thesis:
- **Chapter 5 (Results)**: Include 3-5 detection sample images
- **Chapter 4 (Methodology)**: Show example of model output
- **Appendix**: Include more detection examples

---

## 4. What to Mention in Thesis

### In Methodology (Chapter 4):
> "The model was trained for 200 epochs. During training, performance was monitored at each epoch, and the best-performing checkpoint was automatically saved. The best checkpoint achieved 49.19% mAP@0.5 with 60.43% precision at Epoch 119. This checkpoint (`best.pt`) was selected for deployment to the iOS application."

### In Results (Chapter 5):
> "Training was completed over 200 epochs. Figure X.X shows the progression of mAP@0.5, precision, and recall metrics throughout training. The best performance was achieved at Epoch 119 with 49.19% mAP@0.5 and 60.43% precision. The final epoch (Epoch 200) achieved 42.03% mAP@0.5 and 48.69% precision. The model checkpoint from Epoch 119 (`best.pt`) was selected for deployment as it represents the optimal balance between accuracy and model stability."

### Table for Results Chapter:

| Checkpoint | Epoch | mAP@0.5 | Precision | Recall | Status |
|------------|-------|---------|-----------|--------|--------|
| **best.pt** | 119 | **49.19%** | **60.43%** | 47.22% | **Deployed** |
| last.pt | 200 | 42.03% | 48.69% | 41.15% | Final state |

---

## 5. Quick Commands Summary

```bash
# Create graphs
pip install matplotlib
python3 scripts/create_graphs_simple.py results/yolov8s_rdd2022_high_perf/results.csv results/yolov8s_rdd2022_high_perf/graphs

# Create detection samples
pip install opencv-python ultralytics
python3 scripts/visualize_detections.py --weights results/yolov8s_rdd2022_high_perf/weights/best.pt --source data/yolo/rdd2022/val/images --output-dir results/yolov8s_rdd2022_high_perf/detection_samples --max-images 10
```

---

## Files Created:

1. **PHASE4_MODEL_SELECTION.md** - Detailed guidance on mentioning models in thesis
2. **scripts/create_graphs_simple.py** - Graph creation script (no pandas needed)
3. **scripts/test_model_detections.py** - Detection testing script
4. **This file** - Complete instructions

---

**All graphs and detection samples will be saved in:**
- Graphs: `results/yolov8s_rdd2022_high_perf/graphs/`
- Detections: `results/yolov8s_rdd2022_high_perf/detection_samples/`

