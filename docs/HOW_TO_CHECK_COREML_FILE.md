# 🔍 How to Check CoreML File

**Guide to verify your CoreML model file is correct and ready for iOS**

---

## 📍 **Location of CoreML File**

Your CoreML model should be located at:
```
/Users/ardaozel/road_defect_detection/artifacts/ios/model/best.mlpackage
```

---

## ✅ **Method 1: Check via Terminal (Quick Check)**

### **1. Check if file exists:**
```bash
cd /Users/ardaozel/road_defect_detection
ls -lh artifacts/ios/model/best.mlpackage
```

**Expected output:**
- Should show a directory (`.mlpackage` is a package/folder, not a single file)
- Size should be approximately **21 MB**

### **2. Check file size:**
```bash
du -sh artifacts/ios/model/best.mlpackage
```

**Expected output:**
```
21M    artifacts/ios/model/best.mlpackage
```

### **3. Check internal structure:**
```bash
ls -la artifacts/ios/model/best.mlpackage/
```

**Expected output:**
```
drwxr-xr-x  ... Data
-rw-r--r--  ... Manifest.json
```

### **4. Verify model file inside package:**
```bash
ls -lh artifacts/ios/model/best.mlpackage/Data/com.apple.CoreML/
```

**Expected output:**
- Should show `model.mlmodel` file
- Size should be approximately **21 MB**

---

## ✅ **Method 2: Check via Python (Detailed Verification)**

### **1. Install coremltools (if not already installed):**
```bash
pip3 install coremltools
```

### **2. Run verification script:**
```bash
cd /Users/ardaozel/road_defect_detection
python3 -c "
import coremltools as ct
import os

model_path = 'artifacts/ios/model/best.mlpackage'
if os.path.exists(model_path):
    print('✅ Model file exists')
    print(f'   Location: {os.path.abspath(model_path)}')
    
    # Try to load the model
    try:
        model = ct.models.MLModel(model_path)
        print('✅ Model loaded successfully')
        print(f'   Model type: {type(model)}')
        
        # Get model specification
        spec = model.get_spec()
        print(f'   Input: {spec.description.input[0].name}')
        print(f'   Output: {spec.description.output[0].name}')
        print('✅ Model is valid and ready for iOS!')
    except Exception as e:
        print(f'❌ Error loading model: {e}')
else:
    print('❌ Model file not found!')
    print('   Run: python3 scripts/export_to_coreml.py')
"
```

**Expected output:**
```
✅ Model file exists
   Location: /Users/ardaozel/road_defect_detection/artifacts/ios/model/best.mlpackage
✅ Model loaded successfully
   Model type: <class 'coremltools.models.model.MLModel'>
   Input: image
   Output: (output names)
✅ Model is valid and ready for iOS!
```

---

## ✅ **Method 3: Check via Xcode (After Adding to Project)**

### **1. Open Xcode project**

### **2. Find the model in Project Navigator:**
- Look for `best.mlpackage` in your project files

### **3. Click on the model file:**
- Xcode will show model information in the editor

### **4. Verify model details:**
- **Type**: Should say "Core ML Model" or "Core ML Package"
- **Input**: Should show image input (640x640)
- **Output**: Should show detection outputs
- **Size**: Should show ~21 MB

### **5. Check Target Membership:**
- Click on `best.mlpackage` in Navigator
- Open File Inspector (⌘⌥1)
- Under **Target Membership**, make sure your app target is checked ✅

---

## ✅ **Method 4: Visual Inspection with Netron (Optional)**

### **1. Install Netron (if you want visual inspection):**
```bash
# Via Homebrew
brew install netron

# Or download from: https://github.com/lutzroeder/netron
```

### **2. Open model in Netron:**
```bash
netron artifacts/ios/model/best.mlpackage
```

This will open a web browser showing the model architecture visually.

---

## 🔍 **Quick Verification Checklist**

Run these commands to verify everything:

```bash
cd /Users/ardaozel/road_defect_detection

# 1. Check file exists
echo "1. Checking if file exists..."
ls -lh artifacts/ios/model/best.mlpackage && echo "✅ File exists" || echo "❌ File not found"

# 2. Check file size
echo -e "\n2. Checking file size..."
du -sh artifacts/ios/model/best.mlpackage

# 3. Check internal structure
echo -e "\n3. Checking internal structure..."
ls artifacts/ios/model/best.mlpackage/ 2>/dev/null && echo "✅ Structure looks good" || echo "❌ Invalid structure"

# 4. Check model file
echo -e "\n4. Checking model file..."
ls -lh artifacts/ios/model/best.mlpackage/Data/com.apple.CoreML/model.mlmodel 2>/dev/null && echo "✅ Model file found" || echo "❌ Model file missing"
```

---

## 📊 **Expected Results**

| Check | Expected Result |
|-------|----------------|
| **File exists** | ✅ `best.mlpackage` directory exists |
| **File size** | ✅ ~21 MB |
| **Structure** | ✅ Contains `Data/` and `Manifest.json` |
| **Model file** | ✅ `Data/com.apple.CoreML/model.mlmodel` exists |
| **Python load** | ✅ Model loads without errors |
| **Xcode display** | ✅ Shows model info in Xcode |

---

## ❌ **Common Issues**

### **Issue: File not found**
```bash
# Solution: Export the model
python3 scripts/export_to_coreml.py
```

### **Issue: File size is 0 or very small**
```bash
# Solution: Re-export the model
python3 scripts/export_to_coreml.py
```

### **Issue: Python can't load model**
```bash
# Solution: Install coremltools
pip3 install coremltools

# Then try loading again
```

### **Issue: Xcode doesn't show model info**
- Make sure model is added to project
- Check Target Membership is enabled
- Clean build folder (⇧⌘K) and rebuild

---

## 🎯 **Quick Test Command**

Run this single command to check everything:

```bash
cd /Users/ardaozel/road_defect_detection && \
echo "=== CoreML Model Check ===" && \
[ -d "artifacts/ios/model/best.mlpackage" ] && \
echo "✅ Model file exists" && \
du -sh artifacts/ios/model/best.mlpackage && \
[ -f "artifacts/ios/model/best.mlpackage/Data/com.apple.CoreML/model.mlmodel" ] && \
echo "✅ Model structure is correct" && \
echo "✅ Ready for Xcode!" || \
echo "❌ Model not found or invalid. Run: python3 scripts/export_to_coreml.py"
```

---

## 📝 **Summary**

**Your CoreML file should be:**
- ✅ Located at: `artifacts/ios/model/best.mlpackage`
- ✅ Size: ~21 MB
- ✅ Format: `.mlpackage` (CoreML package)
- ✅ Contains: `Data/com.apple.CoreML/model.mlmodel`
- ✅ Ready to drag into Xcode

**Next step:** Follow `docs/STEP_BY_STEP_PHASE2.md` Step 4 to add it to your Xcode project!

