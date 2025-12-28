# Complete Guide: PHASE1 Training → PHASE2 iOS App

## Overview

This guide covers the complete workflow from training a high-accuracy model (PHASE1) to deploying it in an iOS app (PHASE2).

## Table of Contents

1. [PHASE1: Model Training](#phase1-model-training)
2. [PHASE2: iOS Integration](#phase2-ios-integration)
3. [Tools & Scripts](#tools--scripts)
4. [Configuration Files](#configuration-files)
5. [Troubleshooting](#troubleshooting)

---

## PHASE1: Model Training

### Current Status

✅ **Training Started**: YOLOv8-small model training in progress
- **Configuration**: `configs/training_phase1_mps_safe.yaml`
- **Model**: yolov8s (better accuracy than nano)
- **Target**: mAP@0.5 > 60%

### Monitor Training

```bash
# Watch training progress (updates every 30 seconds)
python scripts/monitor_training.py --watch --target-map 0.60

# Check current status
python scripts/monitor_training.py

# Save metrics to JSON
python scripts/monitor_training.py --json-output results/current_metrics.json
```

### Expected Timeline

- **Total time**: ~12-16 hours for 200 epochs
- **Epoch 1-50**: Initial learning (3-4 hours)
- **Epoch 50-100**: Rapid improvement (3-4 hours)
- **Epoch 100-200**: Fine-tuning (6-8 hours)

### After Training Completes

1. **Check final metrics**:
   ```bash
   cat results/yolov8s_rdd2022_phase1_mps/evaluation/evaluation_summary.txt
   ```

2. **Comprehensive evaluation**:
   ```bash
   python scripts/comprehensive_evaluate.py \
       --weights weights/best.pt \
       --split test \
       --optimize-conf \
       --output-dir results/comprehensive_eval
   ```

3. **Analyze dataset** (if needed):
   ```bash
   python scripts/analyze_dataset.py \
       --data-yaml data/yolo/rdd2022.yaml \
       --check-images \
       --check-annotations
   ```

---

## PHASE2: iOS Integration

### Step 1: Export Model to CoreML

After training completes and mAP > 60%:

```bash
python scripts/export_for_ios.py \
    --weights weights/best.pt \
    --imgsz 640 \
    --half \
    --nms
```

**Output**: `artifacts/ios/model/best.mlmodel`

### Step 2: Create Xcode Project

1. Open Xcode
2. File → New → Project
3. Choose "App" template
4. Product Name: `RoadDefectDetector`
5. Interface: SwiftUI
6. Language: Swift
7. Minimum Deployment: iOS 14.0

### Step 3: Add Files to Xcode

1. **Copy CoreML model**:
   - Drag `best.mlmodel` into Xcode project
   - Check "Copy items if needed"
   - Add to target

2. **Copy Swift files** from `iOS/` directory:
   - `DetectionEngine.swift`
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `RoadDefectDetectorApp.swift` (main app file)

3. **Update Info.plist**:
   - Add camera and photo library permissions (see `iOS/Info.plist.template`)

### Step 4: Build and Test

1. **Build project**: Cmd+B
2. **Run on device**: Connect iPhone and run (Cmd+R)
   - ⚠️ CoreML requires real device for Neural Engine
   - Simulator works but is slower

### Step 5: Customize (Optional)

- Adjust confidence threshold in `DetectionEngine.swift`
- Modify UI in SwiftUI views
- Add features (save results, share, etc.)

---

## Tools & Scripts

### Training Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `train_yolov8.py` | Main training script | `python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml` |
| `monitor_training.py` | Monitor training progress | `python scripts/monitor_training.py --watch` |
| `analyze_dataset.py` | Check dataset quality | `python scripts/analyze_dataset.py --check-images` |

### Evaluation Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `evaluate_rdd2022.py` | Basic evaluation | `python scripts/evaluate_rdd2022.py --weights weights/best.pt` |
| `comprehensive_evaluate.py` | Detailed analysis | `python scripts/comprehensive_evaluate.py --weights weights/best.pt --optimize-conf` |
| `visualize_detections.py` | Visualize results | `python scripts/visualize_detections.py --weights weights/best.pt --source data/yolo/images/val` |

### iOS Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `export_for_ios.py` | Export to CoreML | `python scripts/export_for_ios.py --weights weights/best.pt` |

---

## Configuration Files

### Training Configs

- **`configs/training_phase1_mps_safe.yaml`**: Memory-safe training (currently in use)
- **`configs/training_phase1_optimized.yaml`**: Full optimization (if you have more GPU memory)

### Inference Configs

- **`configs/inference_config.yaml`**: Detection settings for iOS app
- **`configs/ios_app_config.json`**: App configuration (can be loaded in iOS app)

---

## Project Structure

```
road_defect_detection/
├── iOS/                          # iOS app files
│   ├── README.md                # iOS integration guide
│   ├── DetectionEngine.swift    # CoreML inference engine
│   ├── ImageProcessor.swift     # Image preprocessing
│   ├── CameraView.swift         # Camera UI
│   ├── ResultsView.swift        # Results display
│   ├── RoadDefectDetectorApp.swift  # Main app
│   └── Info.plist.template      # Permissions template
│
├── scripts/                      # Python scripts
│   ├── train_yolov8.py          # Training
│   ├── monitor_training.py      # Training monitoring
│   ├── comprehensive_evaluate.py # Detailed evaluation
│   ├── analyze_dataset.py       # Dataset analysis
│   ├── export_for_ios.py        # CoreML export
│   └── visualize_detections.py  # Visualization
│
├── configs/                      # Configuration files
│   ├── training_phase1_mps_safe.yaml
│   ├── inference_config.yaml
│   └── ios_app_config.json
│
├── results/                      # Training results
│   └── yolov8s_rdd2022_phase1_mps/
│
└── artifacts/                    # Exported models
    └── ios/
        └── model/
            └── best.mlmodel     # CoreML model (after export)
```

---

## Quick Reference Commands

### Training

```bash
# Start training
python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml

# Monitor training
python scripts/monitor_training.py --watch

# Resume if interrupted
python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml --resume
```

### Evaluation

```bash
# Basic evaluation
python scripts/evaluate_rdd2022.py --weights weights/best.pt --split test

# Comprehensive evaluation with confidence optimization
python scripts/comprehensive_evaluate.py --weights weights/best.pt --optimize-conf

# Visualize detections
python scripts/visualize_detections.py --weights weights/best.pt --num-images 10
```

### iOS Export

```bash
# Export to CoreML
python scripts/export_for_ios.py --weights weights/best.pt --half --nms
```

---

## Performance Targets

### PHASE1 Targets

- ✅ **mAP@0.5**: > 60% (target: 60-75%)
- ✅ **Precision**: > 70%
- ✅ **Recall**: > 60%
- ✅ **F1 Score**: > 65%

### PHASE2 Targets (iOS)

- ✅ **Inference time**: < 50ms per image (iPhone 12+)
- ✅ **Model size**: < 25 MB
- ✅ **Memory usage**: < 100 MB
- ✅ **Battery impact**: Low (Neural Engine optimized)

---

## Troubleshooting

### Training Issues

**Problem**: Training gets killed (OOM)
- **Solution**: Reduce batch size to 1, set workers to 0

**Problem**: Low mAP after training
- **Solution**: Train longer, check dataset quality, consider larger model

**Problem**: Training is slow
- **Solution**: Use GPU if available, or reduce image size (trade-off accuracy)

### iOS Issues

**Problem**: Model not loading in Xcode
- **Solution**: Check model file is added to target, verify CoreML format

**Problem**: Slow inference on device
- **Solution**: Ensure using Neural Engine (A12+ devices), use FP16 model

**Problem**: Detections not accurate
- **Solution**: Adjust confidence threshold, check coordinate conversion

---

## Next Steps

1. ✅ Monitor training until completion
2. ✅ Evaluate model on test set
3. ✅ Export to CoreML
4. ✅ Create Xcode project
5. ✅ Test on iPhone device
6. ✅ Deploy to App Store (when ready)

---

**Status**: Training in progress... 🚀

Check training status: `python scripts/monitor_training.py --watch`
