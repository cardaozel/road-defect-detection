# How to Use Road Defect Detector App

## 📱 Getting Started

### Step 1: Connect Your iPhone

1. **Connect iPhone to Mac** using USB cable
2. **Unlock your iPhone** (enter passcode if prompted)
3. **Trust this computer** if asked on iPhone
4. **Open Xcode** on your Mac

### Step 2: Open Project

1. In Xcode, click **File → Open**
2. Navigate to the `iOS` folder in the project
3. Note: You'll need to create a new Xcode project first (see below)

### Step 3: Create Xcode Project (First Time)

1. Open Xcode
2. Click **File → New → Project**
3. Choose **iOS → App**
4. Fill in:
   - **Product Name**: `RoadDefectDetector`
   - **Team**: Your Apple Developer account
   - **Organization Identifier**: `com.yourcompany` (or your domain)
   - **Interface**: **SwiftUI**
   - **Language**: **Swift**
   - **Storage**: None (or Core Data if you want to save history)
5. Click **Next** and choose save location
6. Click **Create**

### Step 4: Add Files to Xcode

1. **Add CoreML Model**:
   - Right-click project in navigator → **Add Files to "RoadDefectDetector"**
   - Navigate to `artifacts/ios/model/best.mlmodel` (after export)
   - Check **"Copy items if needed"**
   - Check **"RoadDefectDetector"** target
   - Click **Add**

2. **Add Swift Files**:
   - Copy all `.swift` files from `iOS/` folder:
     - `DetectionEngine.swift`
     - `ImageProcessor.swift`
     - `CameraView.swift`
     - `ResultsView.swift`
     - Replace `RoadDefectDetectorApp.swift` with our version
   - Drag and drop them into Xcode project
   - Make sure **"Copy items if needed"** is checked
   - Make sure **"RoadDefectDetector"** target is checked

3. **Update Info.plist**:
   - Click `Info.plist` in project
   - Add these keys (or use the template from `iOS/Info.plist.template`):
     - `NSCameraUsageDescription`: "This app needs camera access to detect road defects in real-time."
     - `NSPhotoLibraryUsageDescription`: "This app needs photo library access to analyze saved images."
     - `NSPhotoLibraryAddUsageDescription`: "This app needs permission to save annotated detection results to your photo library."

### Step 5: Build and Run

1. **Select your iPhone** from device menu (top bar in Xcode)
2. **Sign the app**:
   - Click project name in navigator
   - Select **RoadDefectDetector** target
   - Go to **Signing & Capabilities** tab
   - Check **"Automatically manage signing"**
   - Select your **Team**
3. **Build**: Press **Cmd+B** (or Product → Build)
4. **Run**: Press **Cmd+R** (or click Play button)
5. **First launch**: Trust the developer on your iPhone:
   - Go to Settings → General → VPN & Device Management
   - Tap your developer account
   - Tap **Trust**

### Step 6: Grant Permissions

When the app launches, it will ask for:
- **Camera permission** - Tap **Allow** when taking a photo
- **Photo Library permission** - Tap **Allow** when selecting from library
- **Photo Library Add permission** - Tap **Allow** when saving results

## 🎯 Using the App

### Taking a Photo

1. **Tap "Take Photo"** button on home screen
2. **Allow camera access** if first time
3. **Position camera** over road surface
4. **Tap capture button** (white circle)
5. **Wait for processing** (shows "Analyzing image...")
6. **View results** (automatically opens results screen)

### Selecting from Library

1. **Tap "Choose from Library"** button
2. **Allow photo library access** if first time
3. **Select a photo** of a road
4. **Wait for processing**
5. **View results**

### Viewing Results

The results screen shows:
- **Annotated image** with bounding boxes around defects
- **Detection count** (e.g., "3 defects detected")
- **List of detections** with:
  - Defect type (e.g., "Longitudinal Crack")
  - Class code (e.g., "D00")
  - Confidence percentage (e.g., "85%")
- **Color coding** for each defect type

### Saving Photos

1. **Tap "Save Photo"** button on results screen
2. **Allow photo library add permission** if first time
3. **Confirmation alert** appears: "Photo Saved!"
4. **Check Photos app** - annotated image is saved there

### Sharing Results

1. **Tap "Share"** button on results screen
2. **Choose sharing method**:
   - Messages
   - Mail
   - Save to Files
   - AirDrop
   - Social media apps
   - etc.

## 🎨 App Features

### Beautiful Design
- **Modern gradient colors** (blue theme)
- **Smooth animations** (button presses, transitions)
- **Clean card layouts** (organized information)
- **iOS design language** (familiar and intuitive)

### Smart Detection
- **AI-powered** (CoreML with Neural Engine)
- **Fast processing** (20-50ms per image)
- **Accurate results** (high confidence detections)
- **6 defect types** supported

### User-Friendly
- **Large buttons** (easy to tap)
- **Clear feedback** (loading states, success messages)
- **Helpful labels** (defect descriptions)
- **Professional appearance**

## 📸 Photo Tips

### Best Practices

1. **Good lighting**: Take photos in daylight
2. **Clear view**: Make sure road surface is clearly visible
3. **Close enough**: Get close enough to see defects clearly
4. **Flat angle**: Hold phone relatively flat (not too steep)
5. **Avoid blur**: Hold steady or use iPhone's stabilization

### What to Avoid

- ❌ Very dark/low light conditions
- ❌ Too far away (defects too small)
- ❌ Motion blur (moving while taking photo)
- ❌ Reflections/glare on road surface
- ❌ Objects blocking the road (cars, shadows)

## 🔧 Troubleshooting

### App Won't Build

- **Check signing**: Make sure team is selected and valid
- **Check iOS version**: Requires iOS 14.0+
- **Check model file**: Make sure CoreML model is added to project
- **Check Swift files**: Make sure all files compile without errors

### Camera Not Working

- **Check permissions**: Settings → Privacy → Camera → RoadDefectDetector → ON
- **Check device**: Camera only works on real device (not simulator)
- **Restart app**: Close and reopen the app

### Photos Not Saving

- **Check permissions**: Settings → Privacy → Photos → RoadDefectDetector → "Read and Write"
- **Check storage**: Make sure iPhone has storage space
- **Try again**: Sometimes takes a moment to save

### Slow Processing

- **Check device**: Neural Engine requires A12+ (iPhone XR/XS or newer)
- **Check model**: Make sure using FP16 model (smaller, faster)
- **Close other apps**: Free up memory

### No Detections Found

- **Try different photo**: Some photos may not have visible defects
- **Check confidence threshold**: Lower values show more detections (but may include false positives)
- **Check lighting**: Better lighting improves detection

## ✅ Quick Checklist

Before using the app, make sure:
- [ ] iPhone connected to Mac
- [ ] Xcode project created
- [ ] CoreML model added to project
- [ ] All Swift files added to project
- [ ] Info.plist permissions added
- [ ] App built successfully (Cmd+B)
- [ ] App installed on iPhone
- [ ] Permissions granted (camera, photos)
- [ ] Model trained and exported (from Phase 1)

## 🎉 You're Ready!

The app is now ready to use! Connect your iPhone, build, and run to start detecting road defects with beautiful, professional results.
