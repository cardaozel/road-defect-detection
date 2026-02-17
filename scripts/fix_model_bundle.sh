#!/bin/bash
# Script to verify and fix CoreML model bundle inclusion in Xcode project

set -e

echo "🔍 Checking CoreML Model Bundle Inclusion"
echo "=========================================="
echo ""

PROJECT_DIR="RoadDefectDetector/RoadDefectDetector"
MODEL_SOURCE="artifacts/ios/model/best.mlpackage"
MODEL_TARGET="$PROJECT_DIR/best.mlpackage"

# Check if model exists in source
if [ ! -d "$MODEL_SOURCE" ]; then
    echo "❌ Model not found at: $MODEL_SOURCE"
    echo ""
    echo "📦 To export the model, run:"
    echo "   python scripts/export_to_coreml.py"
    exit 1
fi

echo "✅ Model found at: $MODEL_SOURCE"

# Check if model exists in project directory
if [ ! -d "$MODEL_TARGET" ]; then
    echo "⚠️  Model not in Xcode project directory"
    echo "📦 Copying model to project directory..."
    cp -r "$MODEL_SOURCE" "$MODEL_TARGET"
    echo "✅ Model copied to: $MODEL_TARGET"
else
    echo "✅ Model already in project directory: $MODEL_TARGET"
fi

# Verify model structure
echo ""
echo "🔍 Verifying model structure..."
if [ -f "$MODEL_TARGET/Manifest.json" ] && [ -f "$MODEL_TARGET/Data/com.apple.CoreML/model.mlmodel" ]; then
    echo "✅ Model structure is valid"
    SIZE=$(du -sh "$MODEL_TARGET" | cut -f1)
    echo "   Size: $SIZE"
else
    echo "❌ Model structure is invalid"
    echo "   Expected files:"
    echo "   - Manifest.json"
    echo "   - Data/com.apple.CoreML/model.mlmodel"
    exit 1
fi

echo ""
echo "📋 Next Steps in Xcode:"
echo "======================"
echo ""
echo "1. Open RoadDefectDetector.xcodeproj in Xcode"
echo ""
echo "2. In Project Navigator, locate 'best.mlpackage'"
echo "   (If you don't see it, right-click project → 'Add Files to RoadDefectDetector...')"
echo ""
echo "3. Select 'best.mlpackage' in Project Navigator"
echo ""
echo "4. Open File Inspector (right panel, or Cmd+Option+1)"
echo ""
echo "5. Under 'Target Membership', check the box for 'RoadDefectDetector'"
echo ""
echo "6. Clean build folder: Product → Clean Build Folder (Cmd+Shift+K)"
echo ""
echo "7. Build and run: Product → Run (Cmd+R)"
echo ""
echo "✅ The model should now be included in the app bundle!"
echo ""
echo "💡 Tip: If the model still isn't found, try:"
echo "   - Remove 'best.mlpackage' from project (right-click → Delete → Remove Reference)"
echo "   - Re-add it using 'Add Files to RoadDefectDetector...'"
echo "   - Make sure 'Copy items if needed' is checked"
echo "   - Make sure 'Add to targets: RoadDefectDetector' is checked"
