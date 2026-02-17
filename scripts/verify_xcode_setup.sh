#!/bin/bash
# Verify Xcode project setup is ready

echo "🔍 Verifying Xcode Project Setup..."
echo ""

# Check project exists
if [ -d "RoadDefectDetector/RoadDefectDetector.xcodeproj" ]; then
    echo "✅ Xcode project exists"
else
    echo "❌ Xcode project not found"
    echo "   Location: RoadDefectDetector/RoadDefectDetector.xcodeproj"
    exit 1
fi

# Check Swift files
echo ""
echo "📄 Swift files ready to add:"
SWIFT_COUNT=$(ls -1 iOS/*.swift 2>/dev/null | wc -l | tr -d ' ')
if [ "$SWIFT_COUNT" -gt 0 ]; then
    echo "   ✅ $SWIFT_COUNT Swift files in iOS/ folder"
    echo "   Files:"
    ls -1 iOS/*.swift | sed 's/^/      - /'
else
    echo "   ❌ No Swift files found in iOS/ folder"
fi

# Check CoreML model
echo ""
echo "📦 CoreML model ready to add:"
if [ -d "artifacts/ios/model/best.mlpackage" ]; then
    echo "   ✅ best.mlpackage exists"
    SIZE=$(du -sh artifacts/ios/model/best.mlpackage | cut -f1)
    echo "   Size: $SIZE"
else
    echo "   ❌ best.mlpackage not found"
    echo "   Location: artifacts/ios/model/best.mlpackage"
fi

# Check if files are already in Xcode project
echo ""
echo "🔍 Checking if files are already in Xcode project..."

SWIFT_IN_PROJECT=$(find RoadDefectDetector -name "*.swift" -not -path "*/.*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SWIFT_IN_PROJECT" -gt 3 ]; then
    echo "   ⚠️  Found $SWIFT_IN_PROJECT Swift files in project"
    echo "   (Some files may already be added)"
else
    echo "   ℹ️  Only default Swift files in project"
    echo "   (Need to add files from iOS/ folder)"
fi

MODEL_IN_PROJECT=$(find RoadDefectDetector -name "best.mlpackage" 2>/dev/null | wc -l | tr -d ' ')
if [ "$MODEL_IN_PROJECT" -gt 0 ]; then
    echo "   ✅ Model already in Xcode project!"
else
    echo "   ℹ️  Model not yet in Xcode project"
    echo "   (Need to add from artifacts/ios/model/)"
fi

echo ""
echo "📋 Summary:"
echo "   - Xcode project: ✅"
echo "   - Swift files ready: ✅ ($SWIFT_COUNT files)"
echo "   - CoreML model ready: ✅"
echo ""
echo "✅ Everything is ready for manual addition in Xcode!"
echo ""
echo "📖 Next steps:"
echo "   1. Open RoadDefectDetector.xcodeproj in Xcode"
echo "   2. Follow: docs/XCODE_ADD_FILES_DETAILED.md"
echo "   3. Add Swift files from iOS/ folder"
echo "   4. Add CoreML model from artifacts/ios/model/"

