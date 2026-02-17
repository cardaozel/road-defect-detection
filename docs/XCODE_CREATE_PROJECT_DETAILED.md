# 📱 Xcode: Create Project - Step-by-Step Guide
**Exact instructions for every click and option**

---

## 🎯 **Step 1: Open Xcode**

### **What to do:**
1. **Open Finder** (click the Finder icon in Dock, or press `⌘ + Space` and type "Finder")
2. **Go to Applications** (click "Applications" in the left sidebar, or press `⌘ + Shift + A`)
3. **Find Xcode** (scroll or search for "Xcode")
4. **Double-click Xcode** to open it

**OR:**
- Press `⌘ + Space` (Spotlight)
- Type "Xcode"
- Press `Enter`

---

## 🎯 **Step 2: Create New Project**

### **What you'll see:**
- Xcode Welcome window (if first time)
- OR Xcode main window (if you've used it before)

### **What to click:**

**Option A - If you see Welcome window:**
1. Click **"Create a new Xcode project"** button (big blue button)
   - This opens the project template chooser

**Option B - If you see Xcode main window:**
1. Click **"File"** in the top menu bar
2. Click **"New"** in the dropdown menu
3. Click **"Project..."** (or press `⌘ + Shift + N`)

**You should now see:** Project template chooser window

---

## 🎯 **Step 3: Choose Template**

### **What you'll see:**
- Window titled "Choose a template for your new project"
- Left sidebar with categories (iOS, macOS, watchOS, etc.)
- Main area with template icons

### **What to click:**

1. **In the left sidebar:**
   - Click **"iOS"** (should be at the top, with a phone icon)
   - ✅ Make sure it's highlighted/selected

2. **In the main area (templates):**
   - Look for **"App"** template (first icon, usually)
   - It shows a phone icon with "App" text below
   - Click **"App"** icon

3. **At the bottom:**
   - Click **"Next"** button (blue button, bottom right)

**You should now see:** Project options window

---

## 🎯 **Step 4: Configure Project Options**

### **What you'll see:**
- Window titled "Choose options for your new project"
- Form with multiple fields

### **What to fill in (top to bottom):**

#### **1. Product Name:**
- **Field:** "Product Name"
- **What to type:** `RoadDefectDetector`
- **Click in the text field** and type it
- ✅ This will be your app name

#### **2. Team:**
- **Field:** "Team"
- **Dropdown menu**
- **What to select:**
  - If you have an Apple Developer account: Select your team name
  - If you don't have one: Select **"None"** or **"Add an Account..."**
  - For now, **"None"** is fine (you can add it later)

#### **3. Organization Identifier:**
- **Field:** "Organization Identifier"
- **What to type:** `com.ardaozel` (or `com.yourname`)
- **Format:** `com.yourname` (lowercase, no spaces)
- ✅ This creates a unique bundle ID

#### **4. Bundle Identifier:**
- **Field:** "Bundle Identifier" (below Organization Identifier)
- **What you'll see:** `com.ardaozel.RoadDefectDetector` (auto-filled)
- ✅ **Don't change this** - it's automatically created from Product Name + Organization Identifier

#### **5. Interface:**
- **Field:** "Interface"
- **Radio buttons:** "Storyboard" or "SwiftUI"
- **What to select:** 
  - ✅ Click **"SwiftUI"** (the radio button)
  - ⚠️ **IMPORTANT:** Make sure SwiftUI is selected (not Storyboard)

#### **6. Language:**
- **Field:** "Language"
- **Dropdown menu**
- **What to select:**
  - ✅ Click dropdown
  - ✅ Select **"Swift"** (should be default)

#### **7. Storage:**
- **Field:** "Storage" (or "Use Core Data")
- **Checkbox:** "Use Core Data"
- **What to do:**
  - ✅ **Leave it UNCHECKED** (don't check the box)
  - We don't need Core Data for this project

#### **8. Include Tests:**
- **Field:** "Include Tests"
- **Checkboxes:** "Include Unit Tests" and "Include UI Tests"
- **What to do:**
  - ✅ **Check "Include Unit Tests"** (optional, but recommended)
  - ⚪ **"Include UI Tests"** - optional (you can leave unchecked)

### **After filling everything:**
- **Click "Next"** button (blue button, bottom right)

**You should now see:** Save location dialog

---

## 🎯 **Step 5: Choose Save Location**

### **What you'll see:**
- Window titled "Save As:" or file browser
- Text field showing current location
- "Create" button

### **What to do:**

1. **Navigate to project directory:**
   - The dialog might show your home folder or Documents
   - **Click the folder path** at the top (shows current location)
   - **OR click "Desktop"** in the sidebar, then navigate

2. **Navigate to your project:**
   - **Option A - Type path:**
     - Click in the location field
     - Press `⌘ + Shift + G` (Go to folder)
     - Type: `/Users/ardaozel/road_defect_detection`
     - Press `Enter`
   
   - **Option B - Navigate manually:**
     - Click "Documents" or your home folder
     - Navigate to: `road_defect_detection` folder
     - Double-click to open it

3. **Verify location:**
   - You should see folders like: `iOS/`, `scripts/`, `docs/`, `artifacts/`
   - ✅ This confirms you're in the right place

4. **Project name field:**
   - **Field:** "Save As:" or project name field
   - **What you'll see:** `RoadDefectDetector` (auto-filled)
   - ✅ **Don't change this** - it's correct

5. **Source Control (optional):**
   - **Checkbox:** "Create Git repository on my Mac"
   - ✅ **You can check this** if you want Git (recommended)
   - ⚪ Or leave unchecked if you already have Git setup

6. **Final step:**
   - **Click "Create"** button (blue button, bottom right)

**Xcode will now:**
- Create the project folder
- Generate project files
- Open the project in Xcode

---

## 🎯 **Step 6: Wait for Xcode to Finish**

### **What you'll see:**
- Xcode loading/processing
- Progress indicator
- Project window opening

### **What happens:**
- Xcode creates: `RoadDefectDetector.xcodeproj`
- Creates project structure
- Opens the project in Xcode

### **When it's done:**
- You'll see the Xcode project window
- Left sidebar: Project Navigator (folder icon)
- Main area: Code editor
- ✅ **Project is created!**

---

## 🎯 **Step 7: Verify Project Structure**

### **What to check:**

1. **Left sidebar (Project Navigator):**
   - You should see: `RoadDefectDetector` (blue icon at top)
   - Under it: `RoadDefectDetector` folder (yellow folder)
   - Inside: `RoadDefectDetectorApp.swift` file

2. **Project location:**
   - Open Finder
   - Navigate to: `/Users/ardaozel/road_defect_detection/`
   - You should see: `RoadDefectDetector/` folder (NEW)
   - Inside: `RoadDefectDetector.xcodeproj` file

3. **Verify:**
   ```
   road_defect_detection/
   ├── RoadDefectDetector/          ← NEW (your Xcode project)
   │   ├── RoadDefectDetector.xcodeproj
   │   └── RoadDefectDetector/
   │       └── RoadDefectDetectorApp.swift
   ├── iOS/                         ← Existing
   ├── artifacts/                   ← Existing
   └── ...
   ```

---

## ✅ **Checklist: Did Everything Work?**

- [ ] Xcode opened successfully
- [ ] Created new project (File → New → Project)
- [ ] Selected iOS → App template
- [ ] Filled in Product Name: `RoadDefectDetector`
- [ ] Selected SwiftUI interface
- [ ] Selected Swift language
- [ ] Saved to: `/Users/ardaozel/road_defect_detection/`
- [ ] Project opened in Xcode
- [ ] See `RoadDefectDetector` in Project Navigator

---

## 🐛 **Troubleshooting**

### **Problem: Can't find "Create a new Xcode project"**
- **Solution:** Use File → New → Project (or `⌘ + Shift + N`)

### **Problem: Can't navigate to project folder**
- **Solution:** Use `⌘ + Shift + G` and type: `/Users/ardaozel/road_defect_detection`

### **Problem: "SwiftUI" option not available**
- **Solution:** Make sure you selected "iOS" → "App" template (not other templates)

### **Problem: Project won't create**
- **Solution:** 
  - Check you have write permissions
  - Try saving to Desktop first, then move it
  - Make sure Xcode is fully updated

### **Problem: Can't see Project Navigator**
- **Solution:** 
  - Press `⌘ + 1` to show Project Navigator
  - Or: View → Navigators → Show Project Navigator

---

## 📝 **Summary of All Clicks**

1. **Open Xcode** → Applications → Xcode
2. **File** → **New** → **Project** (or `⌘ + Shift + N`)
3. **iOS** (left sidebar) → **App** (main area) → **Next**
4. **Product Name:** `RoadDefectDetector`
5. **Team:** None (or your team)
6. **Organization Identifier:** `com.ardaozel`
7. **Interface:** **SwiftUI** (radio button)
8. **Language:** **Swift**
9. **Storage:** Leave unchecked
10. **Include Tests:** Check Unit Tests (optional)
11. **Next** button
12. **Navigate to:** `/Users/ardaozel/road_defect_detection`
13. **Create** button
14. ✅ **Done!**

---

## 🎯 **Next Steps**

After creating the project:
1. ✅ Project is created
2. 📁 Next: Add Swift files (Step 3 in `docs/STEP_BY_STEP_PHASE2.md`)
3. 📦 Next: Add CoreML model (Step 4 in `docs/STEP_BY_STEP_PHASE2.md`)

---

## 🔗 **Related Files**

- `docs/STEP_BY_STEP_PHASE2.md` - Complete Phase 2 guide
- `docs/PHASE2_PROJECT_LOCATION.md` - Where to create project

---

**You're ready to create your Xcode project! Follow these steps exactly, and you'll have your project set up in minutes.** 🚀

