# 🚀 Training Speed Optimization Guide

## Current Status
- **Current Config**: `training_optimized_high_performance.yaml`
- **Current Speed**: ~50 minutes per epoch
- **Estimated Total Time**: ~6.6 days for 200 epochs

## Speed Optimization Options

### ⚡ **Option 1: Fast Config (Recommended)**
**Speed Gain**: ~20-30% faster (40-45 min/epoch)
**Accuracy Impact**: Minimal (~2-5% mAP loss)
**Config File**: `configs/training_fast.yaml`

**Changes**:
- Image size: 640 → 512
- Batch size: 4 → 8 (if memory allows)
- Workers: 2 → 4
- Reduced augmentation (mosaic 1.0 → 0.8, mixup 0.15 → 0.1)
- Disabled copy_paste augmentation
- Earlier mosaic closing (15 → 10 epochs)
- Reduced validation detections (300 → 200)

**To use**:
```bash
python scripts/train_yolov8.py \
  --config configs/training_fast.yaml \
  --project results \
  --run-name yolov8s_rdd2022_fast \
  --epochs 200 \
  --batch 8 \
  --imgsz 512 \
  --resume
```

---

### ⚡⚡ **Option 2: Ultra-Fast Config (Aggressive)**
**Speed Gain**: ~40-50% faster (25-30 min/epoch)
**Accuracy Impact**: Moderate (~5-10% mAP loss)
**Best for**: Quick experiments, rapid iteration

**Changes**:
- Image size: 640 → 416
- Batch size: 4 → 8-12 (test memory first)
- Workers: 2 → 4-6
- Minimal augmentation (mosaic 0.5, mixup 0.05)
- Close mosaic at epoch 5
- Disable most augmentations

**Create ultra-fast config**:
```bash
cp configs/training_fast.yaml configs/training_ultra_fast.yaml
# Edit: imgsz: 416, batch: 8, mosaic: 0.5, mixup: 0.05, close_mosaic: 5
```

---

### 🔧 **Option 3: Incremental Optimizations (Current Run)**

You can apply these optimizations to your **currently running training** by modifying the config or restarting with new params:

#### A. Increase Batch Size (if memory allows)
```bash
# Stop current training (Ctrl+C), then resume with:
python scripts/train_yolov8.py \
  --config configs/training_optimized_high_performance.yaml \
  --batch 8 \  # Increase from 4 to 8
  --resume
```
**Speed Gain**: ~15-20% per epoch
**Risk**: OOM (Out of Memory) if system can't handle it

#### B. Increase Workers (data loading)
```yaml
# In config file, change:
hardware:
  workers: 4  # From 2 to 4
```
**Speed Gain**: ~10-15% per epoch (especially if data loading is bottleneck)
**Risk**: Higher memory usage

#### C. Reduce Image Size
```bash
python scripts/train_yolov8.py \
  --config configs/training_optimized_high_performance.yaml \
  --imgsz 512 \  # From 640 to 512
  --resume
```
**Speed Gain**: ~20-25% per epoch
**Accuracy Impact**: ~1-3% mAP loss

#### D. Reduce Augmentation (for later epochs)
```yaml
# In config file:
augmentation:
  mosaic: 0.8  # From 1.0
  mixup: 0.1   # From 0.15
  copy_paste: 0.0  # Disable (was 0.1)
  close_mosaic: 10  # From 15 (disable mosaic earlier)
```
**Speed Gain**: ~10-15% per epoch (especially after epoch 10)
**Accuracy Impact**: Minimal if applied only after warmup

---

### 📊 **Speed vs Accuracy Trade-offs**

| Optimization | Speed Gain | Accuracy Impact | Recommendation |
|-------------|------------|-----------------|----------------|
| Batch 4→8 | +15-20% | None | ✅ **Try if memory allows** |
| Workers 2→4 | +10-15% | None | ✅ **Recommended** |
| Image 640→512 | +20-25% | -1-3% mAP | ✅ **Good balance** |
| Image 640→416 | +40-50% | -5-10% mAP | ⚠️ **Only for quick tests** |
| Reduce mosaic | +10-15% | -1-2% mAP | ✅ **Safe optimization** |
| Disable copy_paste | +5-10% | -0.5-1% mAP | ✅ **Easy win** |
| Close mosaic early | +10-15% | -1-2% mAP | ✅ **After epoch 10** |
| Reduce max_det | +5-10% | None (validation only) | ✅ **Safe** |

---

### 🎯 **Recommended Approach**

**For best speed/accuracy balance:**

1. **Try the Fast Config** (`training_fast.yaml`)
   - 20-30% faster
   - Minimal accuracy loss
   - Safe to use

2. **If you need more speed**, try incremental changes:
   ```bash
   # Test batch size 8 first
   python scripts/train_yolov8.py \
     --config configs/training_fast.yaml \
     --batch 8 \
     --workers 4 \
     --resume
   ```

3. **Monitor memory usage** - if you get OOM errors, reduce batch size or workers

---

### ⚠️ **Important Notes**

1. **Memory Constraints**: 
   - MPS (Apple Silicon) has unified memory
   - Increasing batch/workers may cause OOM
   - Test incrementally (batch 4→6→8)

2. **Current Training**:
   - You can't change config mid-training
   - Need to stop and restart with new config
   - Use `--resume` to continue from checkpoint

3. **Validation Time**:
   - Validation happens after each epoch
   - Takes ~10-20 minutes per epoch
   - Can't skip (needed for metrics)
   - Reducing `max_det` helps slightly

4. **Best Practices**:
   - Always test batch size on 1-2 epochs first
   - Monitor GPU/CPU memory usage
   - Keep augmentation in early epochs (helps accuracy)
   - Can reduce augmentation in later epochs

---

### 🔍 **Checking Current Resource Usage**

```bash
# Check memory usage
top -pid $(pgrep -f train_yolov8.py)

# Or use Activity Monitor on macOS
# Look for Python process using GPU/MPS
```

---

### 📈 **Expected Results**

With **Fast Config**:
- **Before**: ~50 min/epoch × 200 = ~6.6 days
- **After**: ~40 min/epoch × 200 = ~5.5 days
- **Time Saved**: ~1.1 days (27 hours)

With **Ultra-Fast Config**:
- **Before**: ~50 min/epoch × 200 = ~6.6 days  
- **After**: ~30 min/epoch × 200 = ~4.2 days
- **Time Saved**: ~2.4 days (58 hours)
- **Accuracy Loss**: ~5-10% mAP

---

### 🚀 **Quick Start: Apply Fast Config**

If you want to switch to faster training now:

```bash
# 1. Stop current training (Ctrl+C in terminal running training)

# 2. Start with fast config
python scripts/train_yolov8.py \
  --config configs/training_fast.yaml \
  --project results \
  --run-name yolov8s_rdd2022_fast \
  --epochs 200 \
  --batch 8 \
  --imgsz 512 \
  --workers 4 \
  --resume
```

**Note**: This will start a new training run. To continue from your current checkpoint, you'd need to copy the weights or modify the script to resume from the previous run.

