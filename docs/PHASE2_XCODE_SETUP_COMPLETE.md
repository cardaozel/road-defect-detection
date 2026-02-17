# Phase 2: Complete Xcode Project Setup & Model Integration

## 🎯 Overview

This guide will help you:
1. **Export your trained model** (`best.pt`) to CoreML format
2. **Create Xcode project** for iOS app
3. **Integrate the CoreML model** into your Swift code
4. **Test the app** on your iPhone

---

## Step 1: Export Trained Model to CoreML

### Export Script

```bash
cd /Users/ardaozel/road_defect_detection

# Export best.pt to CoreML format
python3 -c "
from ultralytics import YOLO
import os

# Load the best model
model = YOLO('results/yolov8s_rdd2022_high_perf/weights/best.pt')

# Export to CoreML
print('Exporting model to CoreML...')
exported_path = model.export(
    format='coreml',
    imgsz=640,
    half=False,  # Use FP32 for better accuracy
    nms=True,    # Include NMS in model
    project='artifacts/ios',
    name='model'
)

print(f'✅ Model exported to: {exported_path}')
print(f'📱 Ready to add to Xcode project!')
"
```

### Expected Output:
```
✅ Model exported to: artifacts/ios/model/best.mlmodel
```

### Verify Export:
```bash
ls -lh artifacts/ios/model/best.mlmodel
# Should show ~43MB file
```

---

## Step 2: Create Xcode Project

### Option A: Create New Project in Xcode

1. **Open Xcode** → File → New → Project
2. **Select**: iOS → App
3. **Configure**:
   - **Product Name**: `RoadDefectDetector` (or your preferred name)
   - **Interface**: SwiftUI
   - **Language**: Swift
   - **Storage**: None (or Core Data if you want)
   - **Include Tests**: ✅ (optional)
4. **Save Location**: Choose your preferred location
5. **Click**: Create

### Option B: Use Existing Project (if you have one)

Just open your existing `.xcodeproj` file.

---

## Step 3: Add Swift Files to Xcode

### Files to Add (from `iOS/` directory):

1. **Drag and drop** these files into Xcode Project Navigator:
   - `RoadDefectDetectorApp.swift` (main app file)
   - `DetectionEngine.swift` (CoreML integration)
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `HistoryView.swift`
   - `DetectionRecord.swift`
   - `DetectionHistory.swift`
   - `LocationService.swift`
   - `ReportView.swift`
   - `ReportService.swift`

### How to Add:
1. In Xcode, right-click your project folder
2. Select "Add Files to [Project Name]..."
3. Navigate to `road_defect_detection/iOS/`
4. Select all Swift files
5. **Important**: Check ✅ "Copy items if needed" and ✅ "Add to targets: [Your App]"
6. Click "Add"

---

## Step 4: Add CoreML Model to Xcode

### Method 1: Drag and Drop (Easiest)

1. **Find the model file**:
   - Location: `artifacts/ios/model/best.mlmodel`
   - Or: `results/yolov8s_rdd2022_high_perf/weights/best.mlmodel` (if you exported there)

2. **Add to Xcode**:
   - Drag `best.mlmodel` from Finder into Xcode Project Navigator
   - Drop it in your project folder (same level as Swift files)

3. **Important Dialog Options**:
   - ✅ **Copy items if needed** ← CHECK THIS!
   - ✅ **Create groups**
   - ✅ **Add to targets: [Your App Name]** ← CHECK THIS!
   - Click **Finish**

### Method 2: Add Files Menu

1. Right-click project folder in Xcode
2. "Add Files to [Project Name]..."
3. Navigate to `artifacts/ios/model/`
4. Select `best.mlmodel`
5. Check ✅ "Copy items if needed" and ✅ "Add to targets"
6. Click "Add"

### Verify Model is Added:

1. Click on `best.mlmodel` in Xcode Navigator
2. You should see model information in the editor
3. Check it says "Type: Core ML Model"
4. Verify in **File Inspector** (right panel) → **Target Membership** → Your app is checked ✅

---

## Step 5: Configure Info.plist

### Add Camera and Location Permissions:

1. In Xcode, find `Info.plist` (or create one if it doesn't exist)
2. Add these keys:

```xml
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to detect road defects in real-time.</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to import images for defect detection.</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>This app needs location access to tag detections with GPS coordinates and provide local authority contact information for reporting road defects.</string>
```

### Or in Xcode UI:
1. Click on your project in Navigator
2. Select your **Target** → **Info** tab
3. Click **+** to add new keys:
   - `Privacy - Camera Usage Description`
   - `Privacy - Photo Library Usage Description`
   - `Privacy - Location When In Use Usage Description`

---

## Step 6: Verify DetectionEngine.swift

### Check Model Name:

Open `DetectionEngine.swift` and verify line 47:

```swift
guard let modelURL = Bundle.main.url(forResource: "best", withExtension: "mlmodel") else {
```

**Important**: The model file name must be `best.mlmodel` (or update this line to match your model name).

---

## Step 7: Build and Test

### Build the Project:

1. **Select your iPhone** as target device (or Simulator)
2. Press **⌘B** (or Product → Build)
3. **Fix any errors** if they appear

### Common Issues:

**Issue**: "Model file not found in bundle"
- **Solution**: Check `best.mlmodel` is in Target Membership (File Inspector)

**Issue**: "No such module 'CoreML'" or "No such module 'Vision'"
- **Solution**: These are built-in frameworks, just clean build (⇧⌘K) and rebuild

**Issue**: Swift file errors
- **Solution**: Make sure all Swift files are added to the target

### Run on iPhone:

1. **Connect iPhone** via USB
2. **Unlock iPhone** and trust computer if prompted
3. **Select iPhone** as target device in Xcode
4. **Press ⌘R** (or Product → Run)
5. **First launch**: On iPhone, go to Settings → General → VPN & Device Management → Trust developer
6. **Grant permissions**: Allow camera and location access when prompted

---

## Step 8: Test Detection

### Test Steps:

1. **Open app** on iPhone
2. **Grant camera permission** when prompted
3. **Point camera** at a road surface (or use a test image)
4. **Tap capture** or use real-time detection
5. **Verify detections** appear with bounding boxes

### Expected Behavior:

- ✅ Model loads successfully (check console for "✅ Model loaded successfully")
- ✅ Camera view shows live preview
- ✅ Detections appear with bounding boxes and labels
- ✅ Confidence scores displayed
- ✅ GPS location tagged automatically

---

## 📁 Final Project Structure

Your Xcode project should look like:

```
RoadDefectDetector (Project)
└── RoadDefectDetector (Target)
    ├── RoadDefectDetectorApp.swift    ← App entry point
    ├── DetectionEngine.swift          ← CoreML integration
    ├── ImageProcessor.swift
    ├── CameraView.swift
    ├── ResultsView.swift
    ├── HistoryView.swift
    ├── DetectionRecord.swift
    ├── DetectionHistory.swift
    ├── LocationService.swift
    ├── ReportView.swift
    ├── ReportService.swift
    ├── best.mlmodel                   ← CoreML model (ADD THIS!)
    ├── Info.plist                     ← Permissions
    └── Assets.xcassets
        └── AppIcon
```

---

## 🔧 Quick Export Command (One-Liner)

If you want to export the model quickly:

```bash
cd /Users/ardaozel/road_defect_detection && python3 -c "from ultralytics import YOLO; model = YOLO('results/yolov8s_rdd2022_high_perf/weights/best.pt'); print('Exporting...'); model.export(format='coreml', imgsz=640, project='artifacts/ios', name='model'); print('✅ Done!')"
```

---

## ✅ Checklist

Before running the app:

- [ ] Model exported to CoreML (`best.mlmodel` exists)
- [ ] Xcode project created
- [ ] All Swift files added to project
- [ ] `best.mlmodel` added to Xcode project
- [ ] Model added to target (check Target Membership)
- [ ] Info.plist configured with permissions
- [ ] Project builds without errors (⌘B)
- [ ] iPhone connected and trusted
- [ ] App runs on iPhone (⌘R)

---

## 🎓 Understanding the Integration

### How It Works:

1. **Model Export**: `best.pt` (PyTorch) → `best.mlmodel` (CoreML)
2. **Xcode Integration**: `.mlmodel` file added to project bundle
3. **Swift Code**: `DetectionEngine.swift` loads model from bundle
4. **Vision Framework**: Wraps CoreML model for easy image processing
5. **Real-time Detection**: Camera feeds images → Model processes → Detections returned

### Key Files:

- **`DetectionEngine.swift`**: Handles CoreML model loading and inference
- **`best.mlmodel`**: Your trained YOLOv8s model in CoreML format
- **`CameraView.swift`**: Captures images and calls DetectionEngine

---

## 🚀 Next Steps

1. **Export model** (Step 1)
2. **Create Xcode project** (Step 2)
3. **Add files** (Steps 3-4)
4. **Build and test** (Steps 7-8)
5. **Start Phase 4** (Thesis documentation)

---

**Need help? See `iOS/XCODE_SETUP_GUIDE.md` for more detailed instructions!**

