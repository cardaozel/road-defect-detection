# Fix: CoreML Model Not Found in Bundle

## Problem
```
❌ Model file not found in bundle (tried both .mlpackage and .mlmodel)
❌ Model not loaded
```

This error occurs when the CoreML model file exists in your project directory but isn't included in the app bundle at runtime.

## Quick Fix

### Step 1: Verify Model Exists
Run the verification script:
```bash
./scripts/fix_model_bundle.sh
```

### Step 2: Add Model to Xcode Target

1. **Open Xcode Project**
   - Open `RoadDefectDetector/RoadDefectDetector.xcodeproj`

2. **Locate Model File**
   - In Project Navigator (left sidebar), find `best.mlpackage`
   - If you don't see it:
     - Right-click on project → "Add Files to RoadDefectDetector..."
     - Navigate to `RoadDefectDetector/RoadDefectDetector/best.mlpackage`
     - Select it and click "Add"

3. **Check Target Membership**
   - Select `best.mlpackage` in Project Navigator
   - Open File Inspector (right panel, or press `Cmd+Option+1`)
   - Under "Target Membership", check the box for **"RoadDefectDetector"**
   - This is the critical step!

4. **Clean and Rebuild**
   - Product → Clean Build Folder (`Cmd+Shift+K`)
   - Product → Run (`Cmd+R`)

## Alternative: Re-add Model

If the above doesn't work:

1. **Remove from Project**
   - Right-click `best.mlpackage` → Delete
   - Choose "Remove Reference" (don't move to trash)

2. **Re-add Model**
   - Right-click project → "Add Files to RoadDefectDetector..."
   - Select `best.mlpackage`
   - **Important**: Check these options:
     - ✅ "Copy items if needed"
     - ✅ "Add to targets: RoadDefectDetector"
   - Click "Add"

3. **Verify**
   - Select `best.mlpackage` in Project Navigator
   - Check File Inspector → Target Membership → "RoadDefectDetector" is checked

4. **Clean and Rebuild**
   - `Cmd+Shift+K` (Clean)
   - `Cmd+R` (Run)

## Verification

After fixing, the app should print:
```
✅ Found model at: /path/to/best.mlpackage
✅ Model loaded successfully
```

Instead of:
```
❌ Model file not found in bundle
```

## Debug Information

The updated `DetectionEngine.swift` now includes debug output that shows:
- Bundle resource path
- List of files in the bundle
- Exact error messages

Check the Xcode console for these messages when the app launches.

## Common Issues

### Issue: Model still not found after adding to target
**Solution**: 
- Make sure you're checking the correct target (RoadDefectDetector, not a test target)
- Try removing and re-adding the model file
- Check that the file extension is `.mlpackage` (not `.mlmodel`)

### Issue: "best 2.mlpackage" exists but not "best.mlpackage"
**Solution**: 
- Remove the duplicate "best 2.mlpackage"
- Ensure only "best.mlpackage" is in the project
- The code looks for "best.mlpackage" specifically

### Issue: Model loads but detection fails
**Solution**: 
- This is a different issue (model inference, not bundle inclusion)
- Check that the model was exported with `nms=True` (included in export script)
- Verify model input/output format matches expectations

## Related Files

- `iOS/DetectionEngine.swift` - Model loading code
- `scripts/export_to_coreml.py` - Model export script
- `scripts/fix_model_bundle.sh` - Verification script
