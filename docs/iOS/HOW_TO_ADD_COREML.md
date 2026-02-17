# How to Add CoreML Model to Xcode Project

## 🎯 Simple Explanation

The CoreML model (`best.mlmodel`) is a **separate file** that you add to Xcode just like Swift files. The Swift code (`DetectionEngine.swift`) automatically finds and uses it.

---

## 📦 What Gets Added

### Files You Need to Add:

1. **Swift Files** (code):
   - `DetectionEngine.swift` ← Uses the model
   - `ImageProcessor.swift`
   - `CameraView.swift`
   - `ResultsView.swift`
   - `RoadDefectDetectorApp.swift`

2. **CoreML Model File** (AI model):
   - `best.mlmodel` ← The actual AI model

---

## 🔗 How They Work Together

```
┌─────────────────────────────────┐
│   DetectionEngine.swift         │
│                                 │
│   Loads: best.mlmodel          │
│   ↓                             │
│   Uses: Vision Framework       │
│   ↓                             │
│   Detects: Road defects        │
└─────────────────────────────────┘
            ↑
            │
            │ Finds automatically
            │
┌─────────────────────────────────┐
│   best.mlmodel                  │
│   (CoreML Model File)           │
│                                 │
│   - Added to Xcode project     │
│   - Included in app bundle     │
│   - Loaded at runtime          │
└─────────────────────────────────┘
```

---

## 📝 Step-by-Step: Adding CoreML Model

### Step 1: Export the Model (After Training Completes)

```bash
cd /Users/ardaozel/road_defect_detection
python scripts/export_for_ios.py --weights weights/best.pt --half --nms
```

This creates: `artifacts/ios/model/best.mlmodel`

### Step 2: Add Model File to Xcode

#### Easiest Method: Drag and Drop

1. **Find the file**:
   - Open Finder
   - Go to: `road_defect_detection/artifacts/ios/model/`
   - Find: `best.mlmodel`

2. **Add to Xcode**:
   - Drag `best.mlmodel` into Xcode's Project Navigator
   - Drop it in your project folder

3. **Important Dialog**:
   - ✅ **Copy items if needed** ← CHECK THIS!
   - ✅ **Create groups**
   - ✅ **Add to targets: RoadScan** ← CHECK THIS! (or your app name)
   - Click **Finish**

### Step 3: Verify It's Added

1. Look in Xcode's Project Navigator
2. You should see `best.mlmodel` listed
3. Click on it - Xcode shows model information
4. Make sure it says "Type: Core ML Model"

---

## 🔍 How DetectionEngine Finds the Model

In `DetectionEngine.swift`, this code automatically finds your model:

```swift
guard let modelURL = Bundle.main.url(forResource: "best", withExtension: "mlmodel") else {
    print("❌ Model file not found in bundle")
    return
}
```

**What this does:**
- Looks for file named `best.mlmodel` in your app bundle
- The app bundle = everything included in your app when you build
- If you added the file correctly (Step 2), it will be in the bundle!

---

## ✅ Checklist

Before building:

- [ ] Model exported: `artifacts/ios/model/best.mlmodel` exists
- [ ] Model added to Xcode project (visible in Navigator)
- [ ] Model added to target (check File Inspector → Target Membership)
- [ ] Model name matches code (`best.mlmodel`)
- [ ] Swift files added (especially `DetectionEngine.swift`)

---

## 🐛 Troubleshooting

### "Model file not found in bundle"

**Problem**: Model not included in app bundle

**Solution**:
1. Select `best.mlmodel` in Xcode Navigator
2. Open **File Inspector** (right panel, ⌘⌥1)
3. Check **Target Membership** section
4. Make sure your app target (RoadScan) is checked ✅
5. Clean build folder: Product → Clean Build Folder (⇧⌘K)
6. Rebuild: ⌘B

### Model File Not Visible

**Problem**: Don't see `best.mlmodel` in Xcode

**Solution**:
1. Make sure you exported the model first (Step 1)
2. Check the file exists: `artifacts/ios/model/best.mlmodel`
3. Try adding it again (Step 2)

### Wrong Model Name

**Problem**: Model file has different name

**Solution**:
- Option 1: Rename model file to `best.mlmodel`
- Option 2: Update `DetectionEngine.swift` line 47:
  ```swift
  // Change "best" to your model name
  guard let modelURL = Bundle.main.url(forResource: "your-model-name", withExtension: "mlmodel") else {
  ```

---

## 📊 File Structure in Xcode

After adding everything, your Xcode project should look like:

```
RoadScan (Project)
└── RoadScan (Target)
    ├── RoadDefectDetectorApp.swift    ← App entry point
    ├── DetectionEngine.swift          ← Uses best.mlmodel
    ├── ImageProcessor.swift
    ├── CameraView.swift
    ├── ResultsView.swift
    ├── best.mlmodel                   ← CoreML model (ADD THIS!)
    └── Assets.xcassets
        └── AppIcon
```

---

## 🎓 Understanding the Connection

### Why It's Simple:

1. **You add the file** → Xcode includes it in your app
2. **Swift code finds it** → Uses `Bundle.main.url(forResource:)`
3. **Model loads automatically** → CoreML handles everything
4. **No complex setup** → Just add the file!

### What Happens at Runtime:

1. App launches
2. `DetectionEngine` initializes
3. Code looks for `best.mlmodel` in app bundle
4. Model loads into memory
5. Ready to detect defects! 🎉

---

## 🚀 Quick Summary

**Adding CoreML to your Swift files = Just add the `.mlmodel` file to Xcode!**

That's it! The Swift code automatically finds and uses it. No complex integration needed - just:
1. Export model (`export_for_ios.py`)
2. Add `.mlmodel` file to Xcode
3. Make sure it's in the target
4. Done! ✅

---

**Need more details? See `XCODE_SETUP_GUIDE.md` for complete instructions!**
