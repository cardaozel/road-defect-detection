# PHASE1 to PHASE2 Guide: Training for iOS Deployment

## Overview

**PHASE1**: Train a high-accuracy model (Target: mAP@0.5 > 65%)
**PHASE2**: Deploy to iOS mobile app for real-time detection from photographs

## Current Performance

- **mAP@0.5**: 29.4% ❌ (Too low for production)
- **Model**: YOLOv8-nano
- **Status**: Training incomplete (stopped at epoch 78/100)

## PHASE1 Optimization Strategy

### 1. Model Upgrade: Nano → Small

**Why upgrade from YOLOv8-nano to YOLOv8-small?**
- **Nano (current)**: 3M params, 6MB, mAP ~29% ❌
- **Small (recommended)**: 11M params, 22MB, expected mAP ~60-70% ✅
- **iOS Impact**: Still very fast on modern iPhones (iPhone 12+), CoreML optimized
- **Trade-off**: Slightly slower inference but dramatically better accuracy

### 2. Training Configuration Changes

**Key improvements in `training_phase1_optimized.yaml`:**

```yaml
model:
  weights: "yolov8s.pt"  # Upgraded from yolov8n.pt
  imgsz: 640              # Increased from 416 for better accuracy

optim:
  epochs: 200             # More epochs (200 vs 100)
  batch: 8                # Larger batch if memory allows
  cos_lr: true            # Cosine learning rate schedule

augmentation:
  mosaic: 1.0             # Full mosaic augmentation
  mixup: 0.15             # Increased mixup
  copy_paste: 0.3         # Copy-paste augmentation for rare classes
```

### 3. Training Commands

#### Option A: If you have enough GPU/MPS memory (Recommended)
```bash
python scripts/train_yolov8.py \
    --config configs/training_phase1_optimized.yaml \
    --epochs 200 \
    --batch 8 \
    --imgsz 640
```

#### Option B: If MPS memory is limited
```bash
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --epochs 200 \
    --batch 4 \
    --imgsz 640
```

#### Option C: Resume from checkpoint (if training interrupted)
```bash
python scripts/train_yolov8.py \
    --config configs/training_phase1_optimized.yaml \
    --resume
```

### 4. Expected Results

With optimized training, you should achieve:
- **mAP@0.5**: 60-75% ✅ (vs current 29.4%)
- **Precision**: 70-85%
- **Recall**: 60-75%
- **Model Size**: ~22 MB (acceptable for iOS)
- **Inference Speed**: 20-50ms per image on iPhone 12+

### 5. Training Monitoring

Monitor training progress:
```bash
# Check results in real-time
tail -f results/yolov8s_rdd2022_phase1/results.csv

# View training plots
open results/yolov8s_rdd2022_phase1/results.png
```

**Target metrics to watch:**
- `metrics/mAP50(B)` should reach > 0.60 (60%)
- `metrics/precision(B)` should reach > 0.70 (70%)
- `metrics/recall(B)` should reach > 0.60 (60%)
- Training should converge smoothly (no overfitting)

## PHASE2: iOS Deployment

### 1. Export to CoreML

Once PHASE1 training is complete and mAP > 60%:

```bash
python scripts/optimize_model.py \
    --weights weights/best.pt \
    --format coreml \
    --imgsz 640 \
    --half  # Use FP16 for smaller size and faster inference
```

This creates: `artifacts/exports/best.mlmodel`

### 2. iOS Integration

The exported `.mlmodel` file can be:
1. **Added directly to Xcode project**
2. **Used with Vision framework** or **CoreML directly**
3. **Optimized for Neural Engine** on modern iPhones

### 3. iOS Performance Expectations

**iPhone 13/14/15:**
- Inference: 20-30ms per image
- Memory: ~50MB (model + buffers)
- Battery: Low impact (Neural Engine optimized)

**iPhone 12:**
- Inference: 30-50ms per image
- Memory: ~50MB
- Battery: Moderate impact

**iPhone 11 and earlier:**
- Inference: 50-100ms per image
- Memory: ~50MB
- Battery: Higher impact (CPU inference)

### 4. iOS App Architecture Recommendations

```
iOS App Flow:
1. Camera/Photo Library → UIImage
2. Preprocessing: Resize to 640x640, normalize
3. CoreML Inference → YOLOv8 predictions
4. Post-processing: NMS, confidence filtering
5. Visualization: Draw bounding boxes on image
6. Display: Show results with confidence percentages
```

**Key considerations:**
- Use **Vision framework** for image preprocessing
- Run inference on **background queue** to avoid UI blocking
- Cache model in memory after first load
- Use **conf threshold** ~0.4-0.5 for good precision/recall balance

## Training Checklist

- [ ] Upgrade model from nano to small (yolov8s)
- [ ] Use optimized training config (training_phase1_optimized.yaml)
- [ ] Train for 200 epochs (or until convergence)
- [ ] Achieve mAP@0.5 > 60% on validation set
- [ ] Test on test set to verify generalization
- [ ] Export to CoreML format
- [ ] Test CoreML inference speed on target device
- [ ] Integrate into iOS app (PHASE2)

## Troubleshooting

### If mAP is still low after training:
1. **Check dataset quality**: Ensure annotations are correct
2. **Increase training time**: Try 300 epochs
3. **Consider larger model**: YOLOv8-medium (but slower on iOS)
4. **Data augmentation**: Ensure augmentation is working correctly
5. **Learning rate**: Try lower initial LR (0.005 instead of 0.01)

### If MPS runs out of memory:
1. Reduce batch size to 2 or 1
2. Set workers to 0
3. Reduce image size to 512 (but expect lower accuracy)
4. Use training_phase1_mps_safe.yaml config

### If training is too slow:
1. Reduce epochs but ensure convergence
2. Use mixed precision (automatic on MPS)
3. Reduce augmentation intensity
4. Consider cloud GPU (Google Colab, AWS, etc.)

## Next Steps

1. **Start optimized training** with yolov8s
2. **Monitor metrics** throughout training
3. **Evaluate on test set** when training completes
4. **Export to CoreML** once mAP > 60%
5. **Begin iOS app development** (PHASE2)
