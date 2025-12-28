# Training Restart Guide

## ⚠️ Training Stopped

Your training stopped during epoch 1 (around batch 103/9545). Since no checkpoint was saved yet (checkpoints usually save after each epoch), you'll need to restart.

## 🔍 What Happened?

Looking at the logs, training was progressing normally but stopped. Possible reasons:
1. **Out of Memory (OOM)** - MPS ran out of memory
2. **System killed the process** - macOS killed it due to memory pressure
3. **Interruption** - Process was interrupted

## ✅ Solution: Restart Training

Since we're still in epoch 1, just restart the training. The app will automatically:
- Use the same configuration
- Start from the beginning
- Save checkpoints after each epoch (so you won't lose progress in the future)

---

## 🚀 How to Restart

### Option 1: Use the Safe Training Script (Recommended)

```bash
cd /Users/ardaozel/road_defect_detection
./scripts/start_safe_training.sh
```

This uses the safest settings (batch=2, workers=0).

### Option 2: Manual Restart

```bash
cd /Users/ardaozel/road_defect_detection
python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml
```

---

## 📝 To Resume Later (If Training Stops Again)

If training stops AFTER epoch 1 (when checkpoints exist), you can resume:

```bash
python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml --resume
```

**Note**: Resume only works if a checkpoint (`last.pt`) exists in the weights directory.

---

## 💡 Prevent Future Stops

### Current Safe Settings:
- Batch size: 2
- Workers: 0
- Image size: 640
- These are already optimized for MPS memory

### If It Keeps Stopping:

1. **Reduce batch size to 1**:
   Edit `configs/training_phase1_mps_safe.yaml`:
   ```yaml
   optim:
     batch: 1  # Reduce from 2 to 1
   ```

2. **Clear MPS cache before training** (already done in code)

3. **Close other applications** to free up memory

4. **Monitor memory usage**:
   ```bash
   # In another terminal
   watch -n 1 "vm_stat | head -20"
   ```

---

## 🎯 Quick Restart Command

Just run this to restart:

```bash
cd /Users/ardaozel/road_defect_detection && python scripts/train_yolov8.py --config configs/training_phase1_mps_safe.yaml
```

Or use the script:

```bash
./scripts/start_safe_training.sh
```

---

## ✅ Checkpoints Explained

YOLOv8 saves checkpoints:
- **`last.pt`**: Latest checkpoint (saved after each epoch)
- **`best.pt`**: Best model so far (saved when mAP improves)

Once epoch 1 completes, you'll have a checkpoint and can use `--resume` if it stops again.

---

## 🔄 Training Status

- **Current run**: `yolov8s_rdd2022_phase1_mps`
- **Progress**: Stopped at epoch 1, batch ~103/9545
- **Checkpoint**: None yet (too early)
- **Action**: Restart from beginning

---

**Just restart the training - it will continue from scratch and you won't lose anything since no checkpoint exists yet!** 🚀
