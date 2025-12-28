# 📊 How to Monitor Training Progress

## Real-Time Monitoring

### Option 1: Continuous Log Viewing (Recommended)

Open a **new terminal window** and run:

```bash
cd /Users/ardaozel/road_defect_detection
tail -f training_log.txt
```

This will show you **live updates** as training progresses. You'll see:
- Validation batches updating every 2-3 seconds
- New log entries as they're written
- Press `Ctrl+C` to stop viewing (doesn't stop training)

---

### Option 2: Quick Status Check

Check the latest progress without continuous monitoring:

```bash
cd /Users/ardaozel/road_defect_detection
tail -10 training_log.txt
```

---

### Option 3: Watch Validation Progress

Monitor just the validation batch numbers:

```bash
cd /Users/ardaozel/road_defect_detection
tail -f training_log.txt | grep -E "[0-9]+/895"
```

This filters to show only validation progress lines.

---

## What You'll See

### During Validation (Current Phase):
```
Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 25% ━━────────── 224/895 2.8s/it 8:15<28:30
```

**Understanding the output:**
- `224/895` = Current batch / Total batches
- `25%` = Progress percentage
- `2.8s/it` = Seconds per iteration (batch)
- `8:15` = Time elapsed
- `<28:30` = Estimated time remaining

### After Validation Completes:
You'll see:
- Final validation metrics (mAP, Precision, Recall)
- Checkpoint saved messages
- Epoch 2 training starting

---

## Current Status Commands

### Check if training is running:
```bash
ps aux | grep train_yolov8.py | grep -v grep
```

### Check process CPU/Memory usage:
```bash
ps -p $(pgrep -f train_yolov8.py) -o pcpu=,pmem=,etime=
```

### Check if epoch 1 completed:
```bash
ls -lh results/yolov8s_rdd2022_phase1_mps/results.csv
```

If the file exists, epoch 1 validation is complete!

---

## Tips

1. **Keep `tail -f` running** in a separate terminal window for live monitoring
2. **Don't worry** if updates seem slow - validation takes 2-3 seconds per batch
3. **Training continues** even if you close the terminal (runs in background)
4. **Check periodically** - you don't need to watch continuously

---

## Quick Status Script

We also have a quick status script:

```bash
cd /Users/ardaozel/road_defect_detection
bash scripts/show_training_progress.sh
```

This shows a summary of current progress.
