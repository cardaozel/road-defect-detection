# Quick Xcode Setup - Adding Files

## 🎯 Quick Steps (5 Minutes)

### 1️⃣ Add Swift Files

1. Open Xcode project
2. Drag these files from `iOS/` folder into Xcode:
   - `DetectionEngine.swift`
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `RoadDefectDetectorApp.swift`
3. In the dialog, check:
   - ✅ Copy items if needed
   - ✅ Add to targets: [Your App Name]

### 2️⃣ Add CoreML Model

1. First, export the model (if not done):
   ```bash
   python scripts/export_for_ios.py --weights weights/best.pt
   ```
   This creates: `artifacts/ios/model/best.mlmodel`

2. In Xcode, drag `best.mlmodel` into the project
3. In the dialog, check:
   - ✅ Copy items if needed
   - ✅ Add to targets: [Your App Name]

### 3️⃣ Update Info.plist

Add camera and photo library permissions (see full guide for details)

### 4️⃣ Build & Run

1. Press Cmd+B to build
2. Connect iPhone
3. Press Cmd+R to run

---

## ✅ Verification

After adding files, check:

- [ ] All Swift files visible in Project Navigator
- [ ] `best.mlmodel` visible in Project Navigator
- [ ] Project builds without errors (Cmd+B)
- [ ] Model file shows details when clicked

---

## 📍 Where to Find Files

- **Swift files**: `road_defect_detection/iOS/*.swift`
- **CoreML model**: `road_defect_detection/artifacts/ios/model/best.mlmodel`
- **App icon**: `road_defect_detection/iOS/AppIcon/AppIcon.appiconset/`

---

## 🐛 Common Issue: Model Not Found

If you get "Model file not found":

1. Check `best.mlmodel` is in Xcode project
2. Select `best.mlmodel` in Navigator
3. Open File Inspector (right panel)
4. Check **Target Membership** - make sure your app target is checked ✅

---

**For detailed instructions, see `XCODE_SETUP_GUIDE.md`**
