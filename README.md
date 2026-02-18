# 🛣️ Road Defect Detection System

YOLOv8-based Road Defect Detection System with iOS Mobile App - Thesis Project

## 📋 Project Overview

This project implements a comprehensive road defect detection system using YOLOv8 object detection model, optimized for iOS mobile deployment.

### Features

- **Deep Learning Model**: YOLOv8s (Small variant) trained on RDD2022 dataset
- **iOS Mobile App**: Native SwiftUI app with CoreML integration
- **Real-time Detection**: On-device inference using CoreML
- **GPS Location Tagging**: Automatic location tagging for detected defects
- **Detection History**: Save and manage detection records
- **Reporting System**: Location-based reporting to road maintenance authorities (25+ countries supported)
- **Photo Management**: Import from gallery, delete, and share functionality

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Dataset Preparation

```bash
# Download RDD2022 dataset
python scripts/download_rdd2022.py

# Prepare YOLO format
python scripts/prepare_rdd2022.py \
    --raw-dir data/raw/RDD2022 \
    --output-dir data/yolo
```

### 3. Training

```bash
# Start Phase 1 training (200 epochs, optimized for MPS)
python scripts/train_yolov8.py \
    --config configs/training_phase1_mps_safe.yaml \
    --batch 2 \
    --workers 0 \
    --epochs 200 \
    --imgsz 640
```

### 4. iOS App Setup

1. Open the project in Xcode (use `RoadDefectDetector` or create a new SwiftUI project and add `iOS/` source files)
2. Export the trained model to CoreML: `python scripts/export_to_coreml.py weights/best.pt`
3. Add `best.mlpackage` to your Xcode project target
4. Build and run on device or simulator

## 📁 Project Structure

```
road_defect_detection/
├── scripts/              # Python training and evaluation scripts
├── configs/              # Training and inference configurations
├── iOS/                  # iOS SwiftUI application source code
├── data/                 # Dataset files (not in repo - too large)
├── results/              # Training results (not in repo)
└── weights/              # Model weights (not in repo)
```

## 🎯 Model & Dataset

- **Model**: YOLOv8s (Small)
- **Dataset**: RDD2022 (19,089 training images, 3,579 validation images)
- **Target**: >60% mAP@0.5:0.95
- **Device**: MPS (Metal Performance Shaders on macOS) or CUDA

## 📱 iOS App Features

- ✅ Real-time defect detection using CoreML
- ✅ Camera integration
- ✅ Photo library import
- ✅ GPS location tagging
- ✅ Detection history with thumbnails
- ✅ Location-based reporting (25+ countries)
- ✅ Photo sharing and deletion
- ✅ Beautiful UI/UX with gradients and animations

## 🛠️ Tools & Scripts

- `scripts/train_yolov8.py` - Main training script
- `scripts/prepare_rdd2022.py` - Dataset preparation
- `scripts/evaluate_rdd2022.py` - Model evaluation
- `scripts/export_to_coreml.py` - Export trained model to CoreML
- `scripts/monitor_training.py` - Training monitoring
- `scripts/visualize_detections.py` - Visualization tools

## 📊 Supported Countries for Reporting

The iOS app includes location-based reporting for:
- 🇹🇷 Turkey
- 🇩🇪 Germany
- 🇫🇷 France, 🇪🇸 Spain, 🇮🇹 Italy, 🇳🇱 Netherlands
- 🇵🇱 Poland, 🇵🇹 Portugal, 🇬🇷 Greece, 🇨🇿 Czech Republic
- 🇷🇴 Romania, 🇭🇺 Hungary, 🇸🇪 Sweden, 🇳🇴 Norway
- 🇩🇰 Denmark, 🇫🇮 Finland, 🇦🇹 Austria, 🇨🇭 Switzerland
- 🇮🇪 Ireland, 🇺🇸 USA, 🇬🇧 UK, 🇨🇦 Canada, 🇦🇺 Australia
- And more...

## 📝 License

This project is developed as a thesis project. See LICENSE file for details.

## 👤 Author

Developed as part of thesis research on road defect detection using deep learning.

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- RDD2022 Dataset
- iOS CoreML Framework
