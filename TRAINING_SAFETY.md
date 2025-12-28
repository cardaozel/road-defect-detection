# Training Safety: Preventing OOM Kills

## ✅ Safety Features Enabled

### 1. Memory-Safe Configuration
- **Batch size: 2** (very conservative for MPS)
- **Workers: 0** (single-threaded, no multiprocessing overhead)
- **Image size: 640** (good balance of accuracy and memory)
- **Reduced augmentation** (less memory during training)

### 2. Automatic Checkpointing
YOLOv8 automatically saves:
- **`last.pt`** - Latest checkpoint (saved every epoch)
- **`best.pt`** - Best model based on validation mAP (saved when improved)

**Location**: `results/yolov8s_rdd2022_phase1_mps/weights/`

### 3. Resume Capability
If training is interrupted or killed, you can resume:
```bash
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --resume
```

This will:
- ✅ Load the last checkpoint
- ✅ Continue from the same epoch
- ✅ Preserve all training progress

## 🛡️ Why This Won't Be Killed

1. **Very Conservative Batch Size**: batch=2 uses minimal memory
2. **No Multiprocessing**: workers=0 eliminates memory overhead from parallel data loading
3. **MPS Memory Management**: Script clears MPS cache before training
4. **Gradient Accumulation**: With batch=2 and 200 epochs, still gets good training signal

## 📊 Memory Usage Estimate

- **Model**: ~500 MB (yolov8s)
- **Batch size 2**: ~2-3 GB
- **Data loading**: ~500 MB (single-threaded)
- **Total**: ~3-4 GB (well within MPS limits on Mac)

## ⚠️ If Training Still Gets Killed

1. **Reduce batch to 1**:
   ```bash
   python scripts/train_yolov8.py \
       --config configs/training_phase1_mps_safe.yaml \
       --batch 1
   ```

2. **Reduce image size** (less ideal, reduces accuracy):
   ```bash
   python scripts/train_yolov8.py \
       --config configs/training_phase1_mps_safe.yaml \
       --imgsz 512
   ```

3. **Resume training** (always works):
   ```bash
   python scripts/train_yolov8.py \
       --config configs/training_phase1_mps_safe.yaml \
       --resume
   ```

## 🚀 Starting Training

```bash
# Safe training script
./scripts/start_safe_training.sh

# OR manual command
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --batch 2 \
    --workers 0 \
    --epochs 200
```

## 📈 Monitoring Training

While training runs, you can monitor:
```bash
# Watch progress
tail -f results/yolov8s_rdd2022_phase1_mps/results.csv

# Check latest metrics
cat results/yolov8s_rdd2022_phase1_mps/results.csv | tail -1
```

**Expected training time**: 12-24 hours (200 epochs with batch=2)

---

**Bottom line**: With batch=2 and workers=0, this should NOT be killed. ✅
