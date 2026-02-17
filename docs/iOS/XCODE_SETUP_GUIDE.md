# Complete Xcode Setup Guide: Adding Swift Files + CoreML Model

## 📱 Step-by-Step Instructions

### Prerequisites

Before starting, make sure you have:
- ✅ Xcode installed (14.0 or later)
- ✅ CoreML model exported (run `python scripts/export_for_ios.py --weights weights/best.pt`)
- ✅ All Swift files ready in `iOS/` folder

---

## 🚀 Part 1: Create Xcode Project (If Not Already Created)

### Step 1.1: Create New Project

1. Open **Xcode**
2. Click **File → New → Project** (or press `Cmd+Shift+N`)
3. Select **iOS → App**
4. Click **Next**
5. Fill in the details:
   - **Product Name**: `RoadScan` (or `RoadDefectDetector`)
   - **Team**: Select your Apple Developer team (or leave blank for now)
   - **Organization Identifier**: `com.yourcompany` (or your domain)
   - **Bundle Identifier**: Will auto-fill as `com.yourcompany.RoadScan`
   - **Interface**: **SwiftUI** ✅
   - **Language**: **Swift** ✅
   - **Storage**: None (unless you want Core Data)
   - **Include Tests**: Optional
6. Click **Next**
7. Choose save location (e.g., Desktop or Documents)
8. Click **Create**

---

## 📝 Part 2: Add Swift Files to Xcode

### Step 2.1: Add Files to Project

You have two methods:

#### Method A: Drag and Drop (Easiest)

1. **Open Finder** and navigate to: `road_defect_detection/iOS/`
2. **Select these Swift files**:
   - `DetectionEngine.swift`
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `RoadDefectDetectorApp.swift` (this replaces the default App file)
3. **Drag all files** into Xcode's **Project Navigator** (left sidebar)
   - Drop them in the folder where you want them (usually the project root or a "Views" folder)
4. **Important dialog appears** - Check these options:
   - ✅ **Copy items if needed** (this copies files to project folder)
   - ✅ **Create groups** (organizes files in Xcode)
   - ✅ **Add to targets: RoadScan** (or your app name)
5. Click **Finish**

#### Method B: Add Files Menu

1. In Xcode, **right-click** on your project folder in Navigator
2. Select **Add Files to "RoadScan"...**
3. Navigate to `road_defect_detection/iOS/`
4. **Select all Swift files** (hold Cmd to multi-select):
   - `DetectionEngine.swift`
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `RoadDefectDetectorApp.swift`
5. **Important options**:
   - ✅ **Copy items if needed**
   - ✅ **Create groups**
   - ✅ **Add to targets: RoadScan**
6. Click **Add**

### Step 2.2: Replace Default App File (If Needed)

If you already have a default `RoadScanApp.swift` or `App.swift`:

1. **Right-click** on the old app file in Navigator
2. Select **Delete**
3. Choose **Move to Trash** (if you want to delete it)
4. Follow Step 2.1 to add `RoadDefectDetectorApp.swift`

---

## 🤖 Part 3: Add CoreML Model to Xcode

### Step 3.1: Export CoreML Model (If Not Done Yet)

First, export your trained model to CoreML format:

```bash
cd /Users/ardaozel/road_defect_detection
python scripts/export_for_ios.py --weights weights/best.pt --half --nms
```

This creates: `artifacts/ios/model/best.mlmodel`

### Step 3.2: Add CoreML Model to Xcode

#### Method A: Drag and Drop (Easiest)

1. **Open Finder** and navigate to:
   - `road_defect_detection/artifacts/ios/model/`
   - Or wherever your `best.mlmodel` file is located
2. **Find the file**: `best.mlmodel` (or `model.mlmodel`)
3. **Drag the `.mlmodel` file** into Xcode's **Project Navigator**
   - Drop it in the project root (same level as your Swift files)
4. **Important dialog appears** - Check these options:
   - ✅ **Copy items if needed** ✅ (IMPORTANT - copies model to project)
   - ✅ **Create groups** ✅
   - ✅ **Add to targets: RoadScan** ✅ (MUST be checked)
5. Click **Finish**

#### Method B: Add Files Menu

1. In Xcode, **right-click** on your project folder in Navigator
2. Select **Add Files to "RoadScan"...**
3. Navigate to `artifacts/ios/model/`
4. **Select** `best.mlmodel`
5. **Important options**:
   - ✅ **Copy items if needed** ✅ (IMPORTANT)
   - ✅ **Create groups** ✅
   - ✅ **Add to targets: RoadScan** ✅ (MUST be checked)
6. Click **Add**

### Step 3.3: Verify Model is Added

1. In Project Navigator, you should see `best.mlmodel` (or your model name)
2. **Click on it** to view model details
3. Xcode will show:
   - Model information
   - Input/Output details
   - Model metadata
4. Make sure it shows "Type: Core ML Model"

---

## ✅ Part 4: Verify Everything is Set Up

### Step 4.1: Check File Structure in Xcode

Your Project Navigator should look like this:

```
RoadScan/
├── RoadScan/
│   ├── RoadDefectDetectorApp.swift    ✅
│   ├── DetectionEngine.swift          ✅
│   ├── ImageProcessor.swift           ✅
│   ├── CameraView.swift               ✅
│   ├── ResultsView.swift              ✅
│   ├── best.mlmodel                   ✅ (CoreML model)
│   └── Assets.xcassets/
│       └── AppIcon
└── RoadScanTests/ (if created)
```

### Step 4.2: Build Project

1. Press **Cmd+B** (or Product → Build)
2. **Check for errors** in the Issue Navigator (⌘5)

**Common Issues:**

- ❌ **"Cannot find 'DetectionEngine' in scope"**
  - Solution: Make sure all Swift files are added to the target (Step 2.1, option 4)

- ❌ **"No such module 'CoreML'"**
  - Solution: This shouldn't happen, but if it does, make sure you're building for iOS

- ❌ **"best.mlmodel" not found**
  - Solution: Make sure model file is added to target (Step 3.2, option 4)

### Step 4.3: Update Model Name in Code (If Needed)

Check `DetectionEngine.swift` line ~47:

```swift
guard let modelURL = Bundle.main.url(forResource: "best", withExtension: "mlmodel") else {
```

If your model file has a different name (not "best.mlmodel"), update this line:

```swift
// If your model is named "model.mlmodel", change to:
guard let modelURL = Bundle.main.url(forResource: "model", withExtension: "mlmodel") else {
```

---

## 🎨 Part 5: Add App Icon (Optional but Recommended)

1. In Project Navigator, find **Assets.xcassets**
2. Click on **AppIcon**
3. Drag the `AppIcon.appiconset` folder from `iOS/AppIcon/` into Xcode
4. Xcode will automatically place images in correct slots

---

## 🔧 Part 6: Configure Info.plist (Permissions)

### Step 6.1: Add Camera Permission

1. In Project Navigator, find **Info.plist** (or your project's Info tab)
2. **Right-click** → **Open As → Source Code** (or use the visual editor)
3. Add these keys:

```xml
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to detect road defects in real-time.</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to analyze saved images.</string>
<key>NSPhotoLibraryAddUsageDescription</key>
<string>This app needs permission to save annotated detection results to your photo library.</string>
```

Or use the visual editor:
1. Click **+** next to any existing key
2. Select **Privacy - Camera Usage Description**
3. Enter: "This app needs camera access to detect road defects in real-time."
4. Repeat for Photo Library permissions

---

## 📱 Part 7: Configure Signing & Capabilities

### Step 7.1: Set Up Signing

1. Click on your **project name** in Navigator (top item)
2. Select your **target** (RoadScan)
3. Go to **Signing & Capabilities** tab
4. Check **Automatically manage signing**
5. Select your **Team** (Apple Developer account)
6. Xcode will auto-generate provisioning profile

---

## ✅ Part 8: Final Checklist

Before running, verify:

- [ ] All Swift files added to project
- [ ] All Swift files added to target
- [ ] CoreML model file added to project
- [ ] CoreML model file added to target
- [ ] Model name matches code (`best.mlmodel` or update code)
- [ ] Info.plist permissions added
- [ ] App icon added (optional)
- [ ] Project builds without errors (Cmd+B)
- [ ] Signing configured

---

## 🚀 Part 9: Run on Device

1. **Connect your iPhone** via USB
2. **Unlock iPhone** and trust computer if prompted
3. In Xcode, **select your device** from the device menu (top bar)
4. Press **Cmd+R** (or click Play button)
5. **First launch**: On iPhone, go to Settings → General → VPN & Device Management
   - Tap your developer account
   - Tap **Trust**
6. App will launch on your iPhone! 🎉

---

## 🐛 Troubleshooting

### Model Not Found Error

**Error**: `Model file not found in bundle`

**Solutions**:
1. Make sure `best.mlmodel` is in project
2. Make sure it's added to target (check in File Inspector → Target Membership)
3. Clean build folder: Product → Clean Build Folder (Cmd+Shift+K)
4. Rebuild: Cmd+B

### Build Errors with Swift Files

**Error**: `Cannot find 'DetectionEngine' in scope`

**Solutions**:
1. Check all Swift files are in the project
2. Check all files are added to target
3. Check for typos in class names
4. Clean and rebuild

### Model Compilation Issues

If Xcode shows model compilation errors:
1. Make sure model format is CoreML (.mlmodel)
2. Try re-exporting the model
3. Check model is valid: Click on model in Xcode and check details

---

## 📝 Quick Reference

### File Locations

```
Your Xcode Project/
└── RoadScan/
    ├── RoadDefectDetectorApp.swift    (from iOS/)
    ├── DetectionEngine.swift          (from iOS/)
    ├── ImageProcessor.swift           (from iOS/)
    ├── CameraView.swift               (from iOS/)
    ├── ResultsView.swift              (from iOS/)
    ├── best.mlmodel                   (from artifacts/ios/model/)
    └── Assets.xcassets/
        └── AppIcon                    (from iOS/AppIcon/)
```

### Key Settings

- **Target Membership**: All files must be checked for your target
- **Copy Items**: Always check "Copy items if needed" when adding files
- **Model Name**: Must match what's in `DetectionEngine.swift` code

---

## 🎉 Success!

Once everything is set up correctly:

1. ✅ Project builds successfully
2. ✅ App runs on device
3. ✅ Camera opens when you tap "Take Photo"
4. ✅ Model loads and detects defects
5. ✅ Results display correctly

**You're ready to use RoadScan!** 🚀
