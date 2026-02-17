# Quick Start: Phase 2 (Xcode) & Phase 4 (Thesis)

## 🚀 Phase 2: Xcode Project Setup (5 Steps)

### Step 1: Export Model to CoreML

```bash
cd /Users/ardaozel/road_defect_detection
python3 scripts/export_to_coreml.py
```

**Output**: `artifacts/ios/model/best.mlmodel` (~43 MB)

### Step 2: Create Xcode Project

1. Open **Xcode** → File → New → Project
2. Select **iOS** → **App**
3. Name: `RoadDefectDetector`
4. Interface: **SwiftUI**
5. Click **Create**

### Step 3: Add Swift Files

1. In Xcode, right-click project → **Add Files to [Project]...**
2. Navigate to: `road_defect_detection/iOS/`
3. Select **ALL** `.swift` files
4. Check ✅ **Copy items** and ✅ **Add to targets**
5. Click **Add**

### Step 4: Add CoreML Model

1. Drag `artifacts/ios/model/best.mlmodel` into Xcode
2. Check ✅ **Copy items** and ✅ **Add to targets**
3. Verify: Click model → Should show "Core ML Model" info

### Step 5: Add Permissions (Info.plist)

Add these keys:
- `Privacy - Camera Usage Description`: "Camera access for road defect detection"
- `Privacy - Location When In Use Usage Description`: "Location for GPS tagging"
- `Privacy - Photo Library Usage Description`: "Photo library for image import"

### Step 6: Build & Run

1. Connect iPhone via USB
2. Select iPhone as target
3. Press **⌘R** to run
4. Trust developer on iPhone if prompted

---

## 📱 How Model Integration Works

### The Flow:

```
best.pt (PyTorch)
    ↓
[Export Script]
    ↓
best.mlmodel (CoreML)
    ↓
[Add to Xcode Project]
    ↓
[Included in App Bundle]
    ↓
DetectionEngine.swift loads it
    ↓
Vision Framework processes images
    ↓
Detections returned to UI
```

### Key Code (Already in DetectionEngine.swift):

```swift
// 1. Load model from bundle
guard let modelURL = Bundle.main.url(forResource: "best", withExtension: "mlmodel") else {
    print("❌ Model not found")
    return
}

// 2. Compile and load
let compiledURL = try MLModel.compileModel(at: modelURL)
let mlModel = try MLModel(contentsOf: compiledURL)
let vnModel = try VNCoreMLModel(for: mlModel)

// 3. Run inference
let request = VNCoreMLRequest(model: vnModel) { request, error in
    // Process results
    let detections = processResults(request.results)
    completion(detections)
}

// 4. Execute on image
let handler = VNImageRequestHandler(ciImage: ciImage)
try handler.perform([request])
```

**This code is already in `DetectionEngine.swift`!** You just need to:
1. Export the model
2. Add it to Xcode
3. Make sure the filename matches ("best.mlmodel")

---

## 📝 Phase 4: Thesis Documentation

### Quick Start:

1. **Open Overleaf**: https://www.overleaf.com
2. **Create new project** (or use supervisor's template)
3. **Copy content from Phase 3** slides into chapters
4. **Add graphs**: Include `results.png` and detection images
5. **Add citations**: Use Harvard style
6. **Format**: Follow requirements (page numbers, headings, etc.)

### Content Sources:

- **Chapter 1**: `PHASE3_POWERPOINT_PRESENTATION.md` Slides 1-3
- **Chapter 3**: `PHASE3_POWERPOINT_PRESENTATION.md` Slides 4-5
- **Chapter 4**: `PHASE3_POWERPOINT_PRESENTATION.md` Slide 6
- **Chapter 5**: `PHASE3_POWERPOINT_PRESENTATION.md` Slides 7-9
- **Chapter 6**: `PHASE3_POWERPOINT_PRESENTATION.md` Slide 10

### Figures Location:

- **Training Graph**: `results/yolov8s_rdd2022_high_perf/results.png`
- **Detection Examples**: `results/yolov8s_rdd2022_high_perf/val_batch0_pred.jpg`
- **Confusion Matrix**: `results/yolov8s_rdd2022_high_perf/confusion_matrix.png`

---

## ✅ Complete Checklist

### Phase 2 (iOS App):
- [ ] Model exported: `python3 scripts/export_to_coreml.py`
- [ ] Xcode project created
- [ ] Swift files added
- [ ] `best.mlmodel` added to Xcode
- [ ] Permissions added to Info.plist
- [ ] Project builds (⌘B)
- [ ] App runs on iPhone (⌘R)

### Phase 4 (Thesis):
- [ ] Overleaf project created
- [ ] Title page added
- [ ] Abstract written
- [ ] Chapter 1 started (from Phase 3)
- [ ] Graphs added to thesis
- [ ] Citations added
- [ ] Formatting checked

---

## 📚 Detailed Guides

- **Phase 2 Complete Setup**: See `PHASE2_XCODE_SETUP_COMPLETE.md`
- **Phase 4 Thesis Start**: See `PHASE4_THESIS_START.md`
- **Model Export**: `scripts/export_to_coreml.py`
- **iOS Integration**: `iOS/HOW_TO_ADD_COREML.md`

---

**You're ready to go! Start with exporting the model, then create the Xcode project.**

