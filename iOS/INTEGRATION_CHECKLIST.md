# iOS Integration Checklist

Use this checklist to ensure everything is set up correctly for iOS deployment.

## Pre-Deployment Checklist

### 1. Model Requirements ✅

- [ ] Model trained to completion (200 epochs)
- [ ] mAP@0.5 > 60% achieved
- [ ] Model evaluated on test set
- [ ] Model exported to CoreML format
- [ ] CoreML model size < 25 MB (FP16)
- [ ] Model tested on sample images

### 2. Xcode Project Setup ✅

- [ ] Xcode project created
- [ ] Minimum iOS version: 14.0
- [ ] SwiftUI interface selected
- [ ] CoreML model added to project
- [ ] All Swift files copied to project:
  - [ ] DetectionEngine.swift
  - [ ] ImageProcessor.swift
  - [ ] CameraView.swift
  - [ ] ResultsView.swift
  - [ ] RoadDefectDetectorApp.swift

### 3. Permissions ✅

- [ ] Camera permission added to Info.plist
- [ ] Photo library permission added to Info.plist
- [ ] Permission descriptions are user-friendly

### 4. Code Configuration ✅

- [ ] Model file name matches in DetectionEngine.swift
- [ ] Confidence threshold adjusted (default: 0.4)
- [ ] Class names match training data
- [ ] Colors configured for each defect type

### 5. Testing ✅

- [ ] Build succeeds without errors
- [ ] App runs on simulator (basic test)
- [ ] App runs on real device (required for Neural Engine)
- [ ] Camera capture works
- [ ] Photo library selection works
- [ ] Detections display correctly
- [ ] Bounding boxes draw accurately
- [ ] Confidence percentages show correctly

### 6. Performance Testing ✅

- [ ] Inference time < 50ms (on iPhone 12+)
- [ ] Memory usage reasonable (< 100 MB)
- [ ] No UI freezing during inference
- [ ] Smooth animations and transitions

### 7. User Experience ✅

- [ ] UI is intuitive and clean
- [ ] Error messages are helpful
- [ ] Loading states are clear
- [ ] Results are easy to understand
- [ ] App handles edge cases (no detections, errors, etc.)

### 8. Optional Enhancements

- [ ] Save annotated images to photo library
- [ ] Share results functionality
- [ ] Settings screen for confidence threshold
- [ ] About/info screen
- [ ] Help/tutorial screen
- [ ] Dark mode support
- [ ] iPad layout optimization

## Deployment Checklist

### App Store Preparation

- [ ] App icon designed (1024x1024)
- [ ] Launch screen configured
- [ ] App Store screenshots prepared
- [ ] App description written
- [ ] Privacy policy (if collecting data)
- [ ] Version number set
- [ ] Build number incremented
- [ ] Code signing configured
- [ ] Provisioning profiles set up

### Testing

- [ ] TestFlight beta testing completed
- [ ] Feedback collected and addressed
- [ ] Performance verified on multiple devices
- [ ] Edge cases tested

## Quick Test Commands

```bash
# 1. Verify model export
python scripts/export_for_ios.py --weights weights/best.pt

# 2. Test model on sample images
python scripts/visualize_detections.py \
    --weights weights/best.pt \
    --source data/yolo/images/test \
    --num-images 10

# 3. Check model metrics
python scripts/comprehensive_evaluate.py \
    --weights weights/best.pt \
    --split test \
    --optimize-conf
```

## Common Issues & Solutions

### Model not loading
- Check model file is in bundle
- Verify model name matches code
- Check Xcode build phases (file is included)

### Slow inference
- Ensure using Neural Engine (real device, A12+)
- Use FP16 model (--half flag)
- Reduce image preprocessing overhead

### Inaccurate detections
- Adjust confidence threshold
- Check coordinate system conversion
- Verify input image size matches training (640x640)

### App crashes
- Check memory usage
- Verify all permissions granted
- Check for nil values in Swift code
