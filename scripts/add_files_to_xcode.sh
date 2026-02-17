#!/bin/bash
# Helper script to prepare files for Xcode
# Note: Files still need to be added through Xcode GUI

echo "📋 Preparing files for Xcode..."
echo ""

PROJECT_DIR="RoadDefectDetector/RoadDefectDetector"
IOS_DIR="iOS"
MODEL_DIR="artifacts/ios/model"

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Xcode project not found at $PROJECT_DIR"
    exit 1
fi

# Copy Swift files
echo "📄 Copying Swift files..."
if [ -d "$IOS_DIR" ]; then
    cp "$IOS_DIR"/*.swift "$PROJECT_DIR/" 2>/dev/null
    echo "✅ Swift files copied"
else
    echo "❌ iOS directory not found"
fi

# Copy CoreML model
echo "📦 Copying CoreML model..."
if [ -d "$MODEL_DIR/best.mlpackage" ]; then
    cp -r "$MODEL_DIR/best.mlpackage" "$PROJECT_DIR/" 2>/dev/null
    echo "✅ CoreML model copied"
else
    echo "⚠️  CoreML model not found at $MODEL_DIR/best.mlpackage"
fi

echo ""
echo "✅ Files are now in your Xcode project folder"
echo ""
echo "📖 Next steps in Xcode:"
echo "   1. Open Xcode project"
echo "   2. Right-click project → 'Add Files to RoadDefectDetector...'"
echo "   3. Navigate to: $(pwd)/$PROJECT_DIR"
echo "   4. Select all .swift files and best.mlpackage"
echo "   5. Check 'Add to targets' → Click 'Add'"
echo ""
echo "   OR use the detailed guide: docs/XCODE_ADD_FILES_DETAILED.md"

