# Training Strategy for Maximum Accuracy on MPS (macOS)

## Problem
Training gets killed due to MPS unified memory constraints, but we want maximum accuracy.

## Solution: Multi-Strategy Approach

### Strategy 1: Resume Training (Recommended First Step)
**YOLOv8 automatically saves checkpoints!** If training gets killed, you can resume:

```bash
# Resume from the last checkpoint
python scripts/train_yolov8.py --resume

# Or resume from a specific checkpoint
python scripts/train_yolov8.py --resume --weights results/yolov8n_rdd2022/weights/last.pt
```

**Benefits:**
- No progress lost
- Can complete full training even if killed multiple times
- Checkpoints saved after each epoch

### Strategy 2: Two-Stage Training (Maximum Accuracy)

#### Stage 1: Fast Training (Lower Memory)
Train with conservative settings to get a good baseline:

```yaml
# configs/training_stage1.yaml
model:
  imgsz: 384  # Smaller for stability
optim:
  batch: 2
  epochs: 20
augmentation:
  mosaic: 0.5
  mixup: 0.0
```

#### Stage 2: Fine-Tuning (Higher Quality)
Fine-tune from Stage 1 with better settings:

```yaml
# configs/training_stage2.yaml
model:
  weights: "results/yolov8n_rdd2022/weights/best.pt"  # From Stage 1
  imgsz: 416  # Larger for better accuracy
optim:
  batch: 2
  epochs: 20
  lr0: 0.001  # Lower LR for fine-tuning
augmentation:
  mosaic: 0.75
  mixup: 0.05
```

**Command:**
```bash
# Stage 1
python scripts/train_yolov8.py --config configs/training_stage1.yaml

# Stage 2 (after Stage 1 completes)
python scripts/train_yolov8.py --config configs/training_stage2.yaml
```

### Strategy 3: Progressive Image Size Training
Start small, gradually increase:

1. **Epochs 1-10**: `imgsz: 384`, `batch: 2`
2. **Epochs 11-20**: `imgsz: 416`, `batch: 2` (resume from epoch 10)
3. **Epochs 21-30**: `imgsz: 448`, `batch: 2` (if memory allows)
4. **Epochs 31-40**: `imgsz: 512`, `batch: 2` (if memory allows)

### Strategy 4: Gradient Accumulation (Simulate Larger Batch)
**Current limitation**: YOLOv8 doesn't natively support gradient accumulation, but you can:
- Use smaller batches (batch=2)
- Adjust learning rate proportionally: `lr0 = base_lr * (effective_batch / actual_batch)`
- Example: For effective batch=8 with actual batch=2, use `lr0: 0.04` (0.01 * 8/2)

### Strategy 5: Memory Optimization Tips

1. **Close other applications** - Free up unified memory
2. **Use `--resume`** - Always resume from checkpoints
3. **Monitor memory**: Check Activity Monitor during training
4. **Reduce validation frequency**: Edit code to validate every N epochs instead of every epoch
5. **Disable plots during training**: Set `plots: false` in config (saves memory)

### Strategy 6: Alternative Model Sizes
If YOLOv8n still causes issues, try:
- **YOLOv8s**: Slightly larger, but may work if you reduce batch to 1
- **YOLOv8m**: Much larger, likely won't work on MPS
- **YOLOv8n**: Current choice (smallest, best for MPS)

## Recommended Workflow

### Option A: Simple Resume (Easiest)
```bash
# Start training
python scripts/train_yolov8.py

# If killed, resume (repeat as needed)
python scripts/train_yolov8.py --resume
```

### Option B: Two-Stage (Best Accuracy)
```bash
# Stage 1: Fast training with lower memory
python scripts/train_yolov8.py \
  --imgsz 384 \
  --batch 2 \
  --epochs 20 \
  --mosaic 0.5 \
  --mixup 0.0 \
  --run-name yolov8n_stage1

# Stage 2: Fine-tune with better settings
python scripts/train_yolov8.py \
  --weights results/yolov8n_stage1/weights/best.pt \
  --imgsz 416 \
  --batch 2 \
  --epochs 20 \
  --lr0 0.001 \
  --mosaic 0.75 \
  --mixup 0.05 \
  --run-name yolov8n_stage2
```

### Option C: Progressive (Maximum Quality)
Manually adjust settings and resume after each stage.

## Accuracy vs Memory Tradeoffs

| Setting | Memory Impact | Accuracy Impact | Recommendation |
|---------|--------------|-----------------|----------------|
| `imgsz: 512` | High | Highest | Use if stable |
| `imgsz: 416` | Medium | High | **Recommended** |
| `imgsz: 384` | Low | Medium | Use if 416 fails |
| `batch: 2` | Low | Medium | **Required for MPS** |
| `batch: 4` | High | High | Use if memory allows |
| `mosaic: 1.0` | Very High | Highest | Avoid on MPS |
| `mosaic: 0.75` | Medium | High | **Recommended** |
| `mosaic: 0.5` | Low | Medium | Use if unstable |
| `mixup: 0.1` | Medium | High | Use if stable |
| `mixup: 0.05` | Low | Medium-High | **Recommended** |
| `mixup: 0.0` | Very Low | Medium | Use if unstable |

## Key Points for Maximum Accuracy

1. **Always use `--resume`** - Never lose progress
2. **Use two-stage training** - Get best of both worlds
3. **Keep image size as large as possible** - 416 is good balance
4. **Use some augmentation** - mosaic 0.75, mixup 0.05
5. **Train for enough epochs** - 40 epochs minimum
6. **Monitor validation metrics** - Stop if overfitting

## Current Configuration Analysis

The current `configs/training.yaml` is optimized for:
- ✅ Stability (won't get killed)
- ✅ Good accuracy (416px, 75% mosaic, 5% mixup)
- ✅ Resume capability (built-in)

**To maximize accuracy further:**
1. Try increasing `imgsz` to 448 or 512 if training is stable
2. Increase `mosaic` to 0.9 if memory allows
3. Use two-stage training for best results
