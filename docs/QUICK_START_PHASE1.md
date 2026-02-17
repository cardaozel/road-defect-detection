# Quick Start: Improve mAP for iOS Deployment (PHASE1)

## Current Status ❌
- **mAP@0.5**: 29.4% (TOO LOW for production)
- **Model**: YOLOv8-nano (too small)
- **Training**: Incomplete (stopped at epoch 78/100)

## Goal ✅
- **Target mAP@0.5**: > 60% (for production iOS app)
- **Model**: YOLOv8-small (better accuracy, still iOS-friendly)
- **Training**: Complete 200 epochs with optimized config

## Immediate Actions

### Step 1: Start Optimized Training

```bash
# Option A: Use the convenience script (recommended)
./scripts/start_phase1_training.sh

# Option B: Manual command (MPS-safe version)
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --epochs 200 \
    --batch 4 \
    --imgsz 640
```

### Step 2: Monitor Training Progress

```bash
# Watch metrics in real-time
tail -f results/yolov8s_rdd2022_phase1/results.csv

# Check training curves
open results/yolov8s_rdd2022_phase1/results.png
```

**Target metrics:**
- `metrics/mAP50(B)` > 0.60 ✅
- `metrics/precision(B)` > 0.70 ✅
- `metrics/recall(B)` > 0.60 ✅

### Step 3: Evaluate When Training Completes

```bash
# The training script automatically runs evaluation
# Check the evaluation report:
cat results/yolov8s_rdd2022_phase1/evaluation/evaluation_summary.txt
```

### Step 4: Export to CoreML for iOS (PHASE2)

Once mAP > 60%:
```bash
python scripts/optimize_model.py \
    --weights weights/best.pt \
    --format coreml \
    --imgsz 640 \
    --half  # FP16 for smaller size
```

This creates: `artifacts/exports/best.mlmodel` (ready for iOS)

## Key Changes from Previous Training

| Parameter | Old (nano) | New (small) | Impact |
|-----------|------------|-------------|--------|
| Model | yolov8n | yolov8s | +30-40% mAP |
| Image Size | 416 | 640 | +5-10% mAP |
| Epochs | 100 | 200 | Better convergence |
| Batch Size | 1 | 4 | More stable training |
| Augmentation | Moderate | Strong | Better generalization |
| LR Schedule | Linear | Cosine | Better convergence |

## Expected Timeline

- **Training Time**: ~12-24 hours (depending on hardware)
- **Expected mAP**: 60-75% (vs current 29.4%)
- **Model Size**: ~22 MB (acceptable for iOS)

## Troubleshooting

### Out of Memory (OOM)?
```bash
# Reduce batch size further
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --batch 2 \
    --workers 0
```

### Still low mAP after training?
1. Check dataset quality
2. Try more epochs (300)
3. Consider yolov8-medium (but slower on iOS)

### Need faster training?
- Use cloud GPU (Google Colab, AWS)
- Or accept slightly lower mAP with fewer epochs

## Next Steps After PHASE1

1. ✅ Achieve mAP > 60%
2. ✅ Export to CoreML
3. ✅ Begin iOS app development (PHASE2)
4. ✅ Integrate model into Xcode project
5. ✅ Test real-time detection on iPhone

---

**Remember**: Quality in PHASE1 = Success in PHASE2! 🚀
