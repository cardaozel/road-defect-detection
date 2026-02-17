# iOS Integration Guide: Road Defect Detection App

## Overview

This guide provides complete instructions for integrating the trained YOLOv8 model into an iOS app for real-time road defect detection from photographs.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Export Model to CoreML](#export-model-to-coreml)
3. [Project Setup](#project-setup)
4. [Code Implementation](#code-implementation)
5. [Testing](#testing)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Xcode 14.0 or later
- iOS 14.0+ deployment target
- Swift 5.7+
- macOS for model export
- Trained YOLOv8 model (mAP > 60%)

## Export Model to CoreML

After training completes:

```bash
# Export to CoreML with FP16 for smaller size
python scripts/optimize_model.py \
    --weights weights/best.pt \
    --format coreml \
    --imgsz 640 \
    --half

# Output: artifacts/exports/best.mlmodel
```

**Model Info:**
- Format: CoreML (.mlmodel)
- Input: Image (640x640x3)
- Output: MultiArray (detections)
- Size: ~11-15 MB (FP16)
- Inference: 20-50ms on iPhone 12+

## Project Setup

### Step 1: Create New Xcode Project

1. Open Xcode
2. File → New → Project
3. Choose "App" template
4. Product Name: `RoadDefectDetector`
5. Interface: SwiftUI
6. Language: Swift
7. Minimum Deployment: iOS 14.0

### Step 2: Add CoreML Model

1. Copy `best.mlmodel` to Xcode project
2. Check "Copy items if needed"
3. Add to target: `RoadDefectDetector`
4. Xcode will automatically generate Swift interface

### Step 3: Add Required Frameworks

In Project Settings → General → Frameworks:
- CoreML
- Vision
- AVFoundation (for camera)
- Photos (for photo library)

### Step 4: Update Info.plist

Add camera and photo library permissions:

```xml
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to detect road defects in real-time.</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to analyze saved images.</string>
```

## Code Implementation

See the Swift files in this directory for complete implementation:
- `DetectionEngine.swift` - CoreML inference engine
- `ImageProcessor.swift` - Image preprocessing
- `CameraView.swift` - Camera capture UI
- `ResultsView.swift` - Detection results display
- `RoadDefectDetectorApp.swift` - Main app entry point

## Quick Start

1. Export model to CoreML (see above)
2. Copy model file to Xcode project
3. Copy Swift files to Xcode project
4. Build and run on device (CoreML requires real device for Neural Engine)

## Performance Tips

- Use **Neural Engine** on A12+ devices for fastest inference
- Process images on **background queue** to avoid UI blocking
- Cache model after first load
- Use **conf threshold ~0.4-0.5** for good precision/recall balance
- Resize images to 640x640 before inference

## Expected Performance

**iPhone 13/14/15 (A15/A16/A17):**
- Inference: 20-30ms per image
- Memory: ~50MB
- Battery: Low impact

**iPhone 12 (A14):**
- Inference: 30-50ms per image
- Memory: ~50MB
- Battery: Moderate impact

**iPhone 11 and earlier:**
- Inference: 50-100ms per image (CPU inference)
- Memory: ~50MB
- Battery: Higher impact
