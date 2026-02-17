# 🛠️ Xcode Troubleshooting & Prevention Guide
**Common issues and how to avoid them**

---

## ✅ **Current Status Check**

Before building, verify:

- [ ] All Swift files are in Project Navigator
- [ ] `best.mlpackage` is in Project Navigator
- [ ] All files have "Add to targets" checked
- [ ] No duplicate files (especially `RoadDefectDetectorApp 2.swift`)
- [ ] All files have proper imports (`import Combine` where needed)

---

## 🐛 **Common Issues & Solutions**

### **Issue 1: Missing `import Combine`**

**Error:**
```
Static subscript 'subscript(_enclosingInstance:wrapped:storage:)' is not available due to missing import of defining module 'Combine'
```

**Solution:**
- ✅ Already fixed in source files (`iOS/` folder)
- If you see this error, make sure you're using files from `iOS/` folder
- Files should have `import Combine` at the top

**Prevention:**
- Always use files from `iOS/` folder (they have all fixes)
- Don't manually edit files in Xcode project folder

---

### **Issue 2: ObservableObject Conformance**

**Error:**
```
Type 'DetectionEngine' does not conform to protocol 'ObservableObject'
```

**Solution:**
- ✅ Already fixed: `DetectionEngine` now conforms to `ObservableObject`
- Make sure you're using the updated file from `iOS/` folder

**Prevention:**
- Use files from `iOS/` folder (they're always up-to-date)

---

### **Issue 3: Duplicate Files**

**Error:**
```
'main' attribute can only apply to one type in a module
Invalid redeclaration of 'RoadDefectDetectorApp'
```

**Solution:**
- Delete duplicate files (especially `RoadDefectDetectorApp 2.swift`)
- Keep only one version of each file

**Prevention:**
- Don't copy files multiple times
- If Xcode asks to replace, choose "Replace"

---

### **Issue 4: Files Not in Target**

**Error:**
```
Use of unresolved identifier
File not found
```

**Solution:**
1. Click on the file in Project Navigator
2. Open File Inspector (⌘⌥1)
3. Check "Target Membership" → Check "RoadDefectDetector"

**Prevention:**
- Always check "Add to targets" when adding files

---

### **Issue 5: CoreML Model Not Found**

**Error:**
```
Model file not found in bundle
```

**Solution:**
1. Verify `best.mlpackage` is in Project Navigator
2. Check Target Membership (File Inspector → Target Membership)
3. Clean build folder (⇧⌘K) and rebuild

**Prevention:**
- Make sure model is added to target
- Use `.mlpackage` format (not `.mlmodel`)

---

### **Issue 6: Build Errors After Adding Files**

**Solution:**
1. **Clean build folder:** `⇧⌘K` (Shift + Command + K)
2. **Close Xcode completely**
3. **Reopen Xcode project**
4. **Build again:** `⌘B`

**Prevention:**
- Always clean build after adding/removing files

---

## ✅ **Prevention Checklist**

### **Before Adding Files:**
- [ ] Use files from `iOS/` folder (they have all fixes)
- [ ] Don't manually edit files
- [ ] Check for duplicates before adding

### **When Adding Files:**
- [ ] Check "Copy items if needed" (if adding from `iOS/` folder)
- [ ] **ALWAYS check "Add to targets: RoadDefectDetector"**
- [ ] Don't add files multiple times

### **After Adding Files:**
- [ ] Clean build folder (⇧⌘K)
- [ ] Build project (⌘B)
- [ ] Check for errors
- [ ] Verify files appear in Project Navigator

---

## 🔧 **Quick Fixes**

### **If You See Errors:**

1. **Clean Build:**
   ```
   Product → Clean Build Folder (⇧⌘K)
   ```

2. **Verify Files:**
   - Check all files are in Project Navigator
   - Check Target Membership for each file

3. **Re-add Files (if needed):**
   - Remove files from project (Remove Reference)
   - Re-add from `iOS/` folder
   - Make sure to check "Add to targets"

4. **Restart Xcode:**
   - Close Xcode completely
   - Reopen project
   - Build again

---

## 📋 **File Status Check**

Run this to verify everything:

```bash
cd /Users/ardaozel/road_defect_detection
./scripts/verify_xcode_setup.sh
```

---

## 🎯 **Best Practices**

1. **Always use source files from `iOS/` folder**
   - They have all the fixes
   - Don't edit files in Xcode project folder directly

2. **Check Target Membership**
   - Every file must be in target
   - Check File Inspector (⌘⌥1) → Target Membership

3. **Clean after changes**
   - Clean build folder after adding/removing files
   - Prevents cached errors

4. **One source of truth**
   - Keep `iOS/` folder as source
   - Copy to Xcode project when needed

---

## 🚨 **Emergency Fix**

If everything breaks:

1. **Remove all Swift files from Xcode project** (Remove Reference)
2. **Run:**
   ```bash
   cd /Users/ardaozel/road_defect_detection
   ./scripts/add_files_to_xcode.sh
   ```
3. **Re-add files in Xcode** (from `iOS/` folder)
4. **Clean and rebuild**

---

## ✅ **You Should Be Good Now!**

All the common issues have been fixed:
- ✅ Combine imports added
- ✅ ObservableObject conformance fixed
- ✅ Duplicate files removed
- ✅ Files are ready in project folder

**Just make sure to:**
1. Add files through Xcode (if not already added)
2. Check "Add to targets"
3. Clean build folder
4. Build project

---

**If you encounter any new errors, check this guide first!** 🚀

