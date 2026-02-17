# Step-by-Step: Phase 2 Xcode Setup
**Where to run each command and what to do**

---

## 📍 Step 1: Export Model to CoreML

### **WHERE**: Terminal (macOS Terminal app)

### **WHAT TO DO**:

1. **Open Terminal** (Applications → Utilities → Terminal)

2. **Navigate to project directory**:
```bash
cd /Users/ardaozel/road_defect_detection
```

3. **Check if model exists**:
```bash
ls -lh results/yolov8s_rdd2022_high_perf/weights/best.pt
```
   - Should show: `best.pt` file (~21 MB)

4. **Install required packages** (if not already installed):
   ```bash
   pip3 install ultralytics coremltools
   ```

5. **Export to CoreML**:
   ```bash
   python3 scripts/export_to_coreml.py
   ```
   - This will create `best.mlpackage` (newer CoreML format, ~21 MB)
   - The model will be copied to `artifacts/ios/model/` automatically

6. **Verify export**:
```bash
ls -lh artifacts/ios/model/best.mlpackage
```
   - Should show: `best.mlpackage` directory (~21 MB)
   - ✅ **If you see this, Step 1 is complete!**
   - **Note**: `.mlpackage` is a directory (package), not a single file. This is the modern CoreML format.

---

## 📍 Step 2: Create Xcode Project

### **WHERE**: Xcode Application

### **WHAT TO DO**:

1. **Open Xcode** (Applications → Xcode)

2. **Create New Project**:
   - Menu: **File** → **New** → **Project**
   - Or: Press **⌘⇧N** (Command + Shift + N)

3. **Select Template**:
   - Choose: **iOS** (left sidebar)
   - Choose: **App** (main area)
   - Click **Next**

4. **Configure Project**:
   - **Product Name**: `RoadDefectDetector` (or your preferred name)
   - **Team**: Select your Apple Developer account (or "None" for now)
   - **Organization Identifier**: `com.yourname` (e.g., `com.ardaozel`)
   - **Interface**: **SwiftUI** ← IMPORTANT!
   - **Language**: **Swift**
   - **Storage**: **None** (or Core Data if you want)
   - **Include Tests**: ✅ (optional, but recommended)
   - Click **Next**

5. **Choose Save Location**:
   - Navigate to: `/Users/ardaozel/road_defect_detection/` (or wherever you want)
   - **Create folder**: `RoadDefectDetector` (or your project name)
   - Click **Create**

6. **Wait for Xcode to finish**:
   - Xcode will create the project
   - You'll see the project navigator on the left
   - ✅ **If you see your project in Xcode, Step 2 is complete!**

---

## 📍 Step 3: Add Swift Files to Xcode

### **WHERE**: Xcode Project Navigator

### **WHAT TO DO**:

1. **In Xcode**, look at the left sidebar (Project Navigator)

2. **Right-click** on your project folder (the blue icon at the top)
   - Example: Right-click on "RoadDefectDetector" (blue icon)

3. **Select**: "Add Files to 'RoadDefectDetector'..."

4. **Navigate to Swift files**:
   - In the file picker, go to: `/Users/ardaozel/road_defect_detection/iOS/`
   - You should see all the `.swift` files

5. **Select ALL Swift files**:
   - Click first file
   - Hold **⌘** (Command) and click each file to select multiple:
     - `RoadDefectDetectorApp.swift`
     - `DetectionEngine.swift`
     - `ImageProcessor.swift`
     - `CameraView.swift`
     - `ResultsView.swift`
     - `HistoryView.swift`
     - `DetectionRecord.swift`
     - `DetectionHistory.swift`
     - `LocationService.swift`
     - `ReportView.swift`
     - `ReportService.swift`

6. **Important Options** (at bottom of dialog):
   - ✅ **Copy items if needed** ← CHECK THIS!
   - ✅ **Create groups** (should be selected)
   - ✅ **Add to targets: RoadDefectDetector** ← CHECK THIS!
   - Click **Add**

7. **Verify files are added**:
   - Look in Xcode Project Navigator (left sidebar)
   - You should see all the Swift files listed
   - ✅ **If you see all Swift files, Step 3 is complete!**

---

## 📍 Step 4: Add CoreML Model to Xcode

### **WHERE**: Xcode Project Navigator + Finder

### **WHAT TO DO**:

1. **Open Finder** (Applications → Finder)

2. **Navigate to model file**:
   - Go to: `/Users/ardaozel/road_defect_detection/artifacts/ios/model/`
   - Find: `best.mlpackage` (it's a folder/package, not a single file)
   - **Keep Finder window open**

3. **In Xcode**:
   - Make sure Project Navigator is visible (left sidebar)
   - Click on your project folder (blue icon)

4. **Drag and Drop**:
   - **Drag** `best.mlpackage` from Finder (the entire folder/package)
   - **Drop** it into Xcode Project Navigator (on your project folder, same level as Swift files)

5. **Important Dialog** (when you drop):
   - ✅ **Copy items if needed** ← CHECK THIS!
   - ✅ **Create groups**
   - ✅ **Add to targets: RoadDefectDetector** ← CHECK THIS!
   - Click **Finish**

6. **Verify model is added**:
   - Look in Xcode Project Navigator
   - You should see `best.mlpackage` listed (or `best.mlmodel` if you have both)
   - Click on the model file
   - In the editor, you should see model information
   - It should say "Type: Core ML Model" or "Core ML Package"

7. **Double-check Target Membership**:
   - Click on `best.mlmodel` in Navigator
   - Look at right panel (File Inspector) - if not visible, press **⌘⌥1**
   - Under **Target Membership**, make sure **RoadDefectDetector** is checked ✅
   - ✅ **If model is added and in target, Step 4 is complete!**

---

## 📍 Step 5: Configure Info.plist (Permissions)

### **WHERE**: Xcode Project Settings

### **WHAT TO DO**:

1. **In Xcode**, click on your **project** (blue icon) in Navigator

2. **Select your Target**:
   - In the main area, click on your app target (e.g., "RoadDefectDetector")
   - It's under "TARGETS" (not "PROJECT")

3. **Go to Info Tab**:
   - Click **Info** tab at the top

4. **Add Permissions**:
   - Click the **+** button (bottom left of the list)
   - Add these three keys:

   **First Permission:**
   - Key: `Privacy - Camera Usage Description`
   - Value: `This app needs camera access to detect road defects in real-time.`
   - Press Enter

   **Second Permission:**
   - Click **+** again
   - Key: `Privacy - Photo Library Usage Description`
   - Value: `This app needs photo library access to import images for defect detection.`
   - Press Enter

   **Third Permission:**
   - Click **+** again
   - Key: `Privacy - Location When In Use Usage Description`
   - Value: `This app needs location access to tag detections with GPS coordinates and provide local authority contact information for reporting road defects.`
   - Press Enter

5. **Verify**:
   - You should see all three permissions in the list
   - ✅ **If all three are added, Step 5 is complete!**

---

## 📍 Step 6: Verify DetectionEngine.swift

### **WHERE**: Xcode Editor

### **WHAT TO DO**:

1. **In Xcode**, open `DetectionEngine.swift`:
   - Click on `DetectionEngine.swift` in Project Navigator

2. **Check the model loading code**:
   - The code now supports both `.mlpackage` (newer) and `.mlmodel` (older) formats
   - It will automatically try `.mlpackage` first, then `.mlmodel`
   - ✅ **No changes needed - the code is already updated!**
   - ✅ **Step 6 is complete!**

---

## 📍 Step 7: Build the Project

### **WHERE**: Xcode

### **WHAT TO DO**:

1. **Select Target Device**:
   - At the top of Xcode, next to the play button
   - Click the device selector
   - Choose: **Your iPhone** (if connected) or **iPhone Simulator**

2. **Build the Project**:
   - Press **⌘B** (Command + B)
   - Or: Menu → **Product** → **Build**

3. **Check for Errors**:
   - Look at the bottom panel (if not visible, press **⌘⇧Y**)
   - **If you see errors** (red X):
     - Read the error messages
     - Common fixes:
       - Missing files: Make sure all Swift files are added
       - Model not found: Check `best.mlmodel` is in target
       - Import errors: Clean build folder (⇧⌘K) and rebuild

4. **If build succeeds** (no errors):
   - You'll see "Build Succeeded" message
   - ✅ **Step 7 is complete!**

---

## 📍 Step 8: Run on iPhone

### **WHERE**: Xcode + iPhone

### **WHAT TO DO**:

1. **Connect iPhone**:
   - Use USB cable
   - Connect iPhone to Mac
   - **Unlock iPhone** (enter passcode)

2. **Trust Computer** (if prompted on iPhone):
   - iPhone will ask "Trust This Computer?"
   - Tap **Trust**
   - Enter iPhone passcode

3. **In Xcode**:
   - Select your **iPhone** as target device (top bar)
   - You should see your iPhone name appear

4. **Run the App**:
   - Press **⌘R** (Command + R)
   - Or: Click the **Play** button (▶️) at top left
   - Or: Menu → **Product** → **Run**

5. **First Launch on iPhone**:
   - App will install on iPhone
   - On iPhone, go to: **Settings** → **General** → **VPN & Device Management**
   - Find your developer profile
   - Tap **Trust [Your Name]**
   - Tap **Trust** again

6. **Grant Permissions**:
   - App will ask for Camera permission → Tap **Allow**
   - App will ask for Location permission → Tap **Allow While Using App**
   - App will ask for Photo Library permission → Tap **Allow Access to All Photos** (or selected)

7. **Test the App**:
   - App should open on iPhone
   - You should see the camera view or main screen
   - ✅ **If app runs, Step 8 is complete!**

---

## 📍 Step 9: Test Detection

### **WHERE**: iPhone App

### **WHAT TO DO**:

1. **Open app** on iPhone (should already be open from Step 8)

2. **Check Console** (in Xcode):
   - Look at bottom panel in Xcode
   - You should see: `✅ Model loaded successfully`
   - If you see this, model is working!

3. **Test Camera Detection**:
   - Point iPhone camera at a road surface (or any surface)
   - Or use a test image from photo library
   - Detections should appear with bounding boxes

4. **Verify Features**:
   - ✅ Camera works
   - ✅ Detections appear
   - ✅ GPS location is tagged
   - ✅ History saves detections
   - ✅ Reporting works

---

## ✅ Complete Checklist

- [ ] **Step 1**: Model exported (`best.mlpackage` exists in `artifacts/ios/model/`)
- [ ] **Step 2**: Xcode project created
- [ ] **Step 3**: All Swift files added to Xcode
- [ ] **Step 4**: `best.mlpackage` added to Xcode and in target
- [ ] **Step 5**: Info.plist permissions added
- [ ] **Step 6**: DetectionEngine.swift verified (supports both .mlpackage and .mlmodel)
- [ ] **Step 7**: Project builds without errors (⌘B)
- [ ] **Step 8**: App runs on iPhone (⌘R)
- [ ] **Step 9**: Detection works in app

---

## 🐛 Troubleshooting

### "Model file not found in bundle"
- **Fix**: Check `best.mlmodel` is in Target Membership (File Inspector → Target Membership)

### "No such module 'CoreML'"
- **Fix**: Clean build (⇧⌘K) and rebuild (⌘B)

### Build errors
- **Fix**: Make sure all Swift files are added to target
- Check File Inspector → Target Membership for each file

### App crashes on launch
- **Fix**: Check console for error messages
- Verify model file is correct size (~43 MB)

---

## 📝 Summary

**Terminal Commands** (run in Terminal):
- `cd /Users/ardaozel/road_defect_detection`
- `pip3 install ultralytics coremltools` (if not already installed)
- `python3 scripts/export_to_coreml.py`
- `ls -lh artifacts/ios/model/best.mlpackage` (to verify)

**Xcode Actions** (do in Xcode):
- Create project
- Add files (drag and drop)
- Configure settings
- Build and run

**Everything else is done in Xcode UI, not Terminal!**

