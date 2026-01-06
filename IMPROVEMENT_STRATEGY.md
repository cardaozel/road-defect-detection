# Strategy to Achieve Target Metrics

## Target Metrics
- **Recall ≥ 70%** (Current: 24.0% → Need +46%)
- **Precision ≥ 60%** (Current: 43.4% → Need +16.6%)
- **mAP@0.5 ≥ 60%** (Current: 19.3% → Need +40.7%)
- **mAP@0.5:0.95 ≥ 35%** (Current: 7.6% → Need +27.4%)

## Critical Issues Identified

### 1. **Model Capacity Too Small** 🔴 HIGH PRIORITY
- **Current**: YOLOv8n (nano) - 3.2M parameters
- **Problem**: Limited capacity for 6-class defect detection
- **Solution**: Switch to **YOLOv8s** (small) - 11.2M parameters
- **Expected Impact**: +15-20% mAP improvement

### 2. **Image Size Too Small** 🔴 HIGH PRIORITY
- **Current**: 416×416 pixels
- **Problem**: Small defects get lost at low resolution
- **Solution**: Increase to **640×640** (or 800×800 if memory allows)
- **Expected Impact**: +10-15% mAP improvement, +20-30% recall improvement

### 3. **Recall Too Low** 🔴 HIGH PRIORITY
- **Current**: 24% (missing 76% of defects!)
- **Root Causes**:
  - Confidence threshold too high
  - NMS IoU threshold too high (0.7)
  - Model capacity insufficient
- **Solutions**:
  - Lower confidence threshold: 0.25 → 0.1-0.15
  - Lower NMS IoU: 0.7 → 0.6
  - Increase max_det: 150 → 300
  - Increase classification loss weight: 0.5 → 1.0
- **Expected Impact**: +40-50% recall improvement

### 4. **Training Duration** 🟡 MEDIUM PRIORITY
- **Current**: 100 epochs
- **Problem**: Model may not have converged
- **Solution**: Increase to **150-200 epochs**
- **Expected Impact**: +5-10% mAP improvement

### 5. **Batch Size Too Small** 🟡 MEDIUM PRIORITY
- **Current**: Batch size 1
- **Problem**: Unstable gradients, slower convergence
- **Solution**: Increase to **4-8** (memory permitting)
- **Expected Impact**: Better convergence, +3-5% mAP

### 6. **Augmentation Insufficient** 🟡 MEDIUM PRIORITY
- **Current**: Reduced augmentation for memory
- **Solutions**:
  - Increase mosaic: 0.75 → 1.0
  - Increase mixup: 0.05 → 0.15
  - Enable copy-paste: 0.0 → 0.1
  - More aggressive scale/rotation
- **Expected Impact**: +5-8% generalization

### 7. **Learning Rate Schedule** 🟢 LOW PRIORITY
- **Current**: Fixed LR decay
- **Solution**: Use **cosine annealing** (cos_lr: true)
- **Expected Impact**: Better final convergence, +2-3% mAP

## Implementation Plan

### Phase 1: Immediate Improvements (High Impact, Low Risk)

1. **Switch to YOLOv8s Model**
   ```bash
   # Download yolov8s.pt if not available
   # Update config: weights: "yolov8s.pt"
   ```

2. **Increase Image Size to 640**
   ```yaml
   imgsz: 640
   ```

3. **Adjust Confidence and NMS for Better Recall**
   ```yaml
   validation:
     conf: 0.15  # Lower threshold
     iou: 0.6    # Less aggressive NMS
     max_det: 300
   ```

4. **Increase Classification Loss Weight**
   ```yaml
   loss_weights:
     cls: 1.0  # Was 0.5
   ```

**Expected Combined Impact**: +25-35% mAP, +35-45% recall

### Phase 2: Training Enhancements

1. **Increase Epochs to 200**
2. **Enable Cosine LR Schedule**
3. **Improve Augmentation**
4. **Increase Batch Size** (if memory allows)

**Expected Additional Impact**: +10-15% mAP

### Phase 3: Advanced Optimizations

1. **Test YOLOv8m** (medium) if YOLOv8s doesn't reach targets
2. **Multi-scale Training**
3. **Ensemble Methods**
4. **Test-Time Augmentation (TTA)**

## Memory Management

Since you're on MPS with 16GB RAM:

### Option A: YOLOv8s with 640×640
- Batch size: 4
- Workers: 2
- Should fit in ~12-14GB RAM

### Option B: YOLOv8n with 640×640 (if Option A OOM)
- Batch size: 2-4
- Workers: 2
- Lower capacity but higher resolution

### Option C: Cloud Training
- Use GPU instances (AWS/GCP)
- Can use YOLOv8m or even YOLOv8l
- Batch size 16-32

## Training Command

```bash
source .venv/bin/activate

python scripts/train_yolov8.py \
    --config configs/training_optimized_high_performance.yaml \
    --project results \
    --run-name yolov8s_rdd2022_high_perf \
    --epochs 200
```

## Monitoring Progress

Track these metrics during training:
1. **Recall** - Target: ≥ 70% (critical!)
2. **Precision** - Target: ≥ 60%
3. **mAP@0.5** - Target: ≥ 60%
4. **mAP@0.5:0.95** - Target: ≥ 35%

If recall < 60% after epoch 100:
- Lower confidence threshold further (0.1)
- Lower NMS IoU (0.5)
- Consider class imbalance (check dataset)

If mAP@0.5 < 50% after epoch 150:
- Consider switching to YOLOv8m
- Check dataset quality and annotations
- Consider data augmentation or synthetic data

## Expected Timeline

- **Epoch 50**: Should see recall > 40%, mAP@0.5 > 30%
- **Epoch 100**: Should see recall > 55%, mAP@0.5 > 45%
- **Epoch 150**: Should see recall > 65%, mAP@0.5 > 55%
- **Epoch 200**: Should reach targets or close

## Alternative: Two-Stage Training

If single model doesn't reach targets:

1. **Stage 1**: Train for high recall (lower confidence, aggressive augmentation)
2. **Stage 2**: Fine-tune for precision (higher confidence, refined augmentation)

Or use ensemble of models trained with different configurations.

