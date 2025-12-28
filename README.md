# Road Defect Detection (RDD2022)

Lightweight end-to-end pipeline for detecting road surface defects (cracks, potholes, etc.) using YOLOv8-nano on the Road Damage Dataset 2022. The project covers dataset acquisition, preprocessing, training, evaluation, optimization for mobile devices, and real-time inference.

## Project Structure

```
road_defect_detection/
├── configs/
│   └── training.yaml          # Centralized hyperparameters & paths
├── data/
│   ├── raw/                   # Downloaded archives & extracted RDD2022
│   └── yolo/                  # Train/val/test splits + rdd2022.yaml
├── scripts/
│   ├── download_rdd2022.py    # Stream + extract raw dataset
│   ├── prepare_rdd2022.py     # Convert to YOLO format splits
│   ├── train_yolov8.py        # Config-driven training script
│   ├── evaluate_rdd2022.py    # Validation metrics and reports
│   ├── optimize_model.py      # Export & quantize for deployment
│   └── infer_realtime.py      # Webcam/video inference utility
└── README.md
```

## Setup

1. **Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install ultralytics torch torchvision opencv-python pandas pyyaml tqdm matplotlib seaborn onnx onnxruntime
   ```
   Adjust packages for your hardware (CUDA/MPS wheels, etc.).

2. **Configuration**
   - Edit `configs/training.yaml` to match your hardware, dataset path, and experiment naming.

## Dataset Pipeline

1. **Download** (saves to `data/raw` by default):
   ```bash
   python scripts/download_rdd2022.py --output-dir /Users/ardaozel/road_defect_detection/data/raw
   ```
2. **Prepare YOLO splits**:
   ```bash
   python scripts/prepare_rdd2022.py \
       --raw-dir /Users/ardaozel/road_defect_detection/data/raw/RDD2022 \
       --output-dir /Users/ardaozel/road_defect_detection/data/yolo
   ```
   This command creates `images/{train,val,test}` and `labels/{train,val,test}` plus `rdd2022.yaml`.

## Training

```bash
python scripts/train_yolov8.py \
    --config configs/training.yaml \
    --device cuda \
    --batch 16 \
    --epochs 100
```

- Override any hyperparameter from the CLI (e.g., `--imgsz 512`, `--lr0 0.005`).
- Best weights are duplicated into the `weights/` directory for downstream steps.

## Evaluation & Metrics

Validate on any split and optionally capture metrics as JSON:
```bash
python scripts/evaluate_rdd2022.py \
    --weights weights/best.pt \
    --data data/yolo/rdd2022.yaml \
    --split test \
    --json results/test_metrics.json \
    --plots
```

## Model Optimization / Export

Export to ONNX (default) with optional quantization flags:
```bash
python scripts/optimize_model.py \
    --weights weights/best.pt \
    --format onnx \
    --imgsz 640 \
    --simplify
```
Other formats: `torchscript`, `tflite`, `coreml`, `ncnn`. Use `--int8` for INT8-compatible exports, `--half` for FP16, and `--dynamic` for dynamic ONNX axes. Artifacts land in the `artifacts/exports/` directory by default.

## Real-Time Inference

```bash
python scripts/infer_realtime.py \
    --weights weights/best.pt \
    --source 0 \
    --conf 0.25 \
    --save \
    --output runs/inference/webcam.mp4
```

- `--source` accepts webcam indices (`0`), video files, image paths, or globs.
- Use `--headless` on servers without display. ESC closes the preview window.

## Tips & Next Steps

- Track experiments with the Ultralytics UI (`results/`), Weights & Biases, or TensorBoard.
- Consider further compression (pruning, knowledge distillation) before deploying on very low-power devices.
- Add unit tests around annotation parsing and data integrity checks if you extend the preprocessing pipeline.
