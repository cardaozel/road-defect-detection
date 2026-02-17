#!/usr/bin/env python3
"""
Export trained YOLOv8 model to CoreML format for iOS deployment.
"""

import sys
from pathlib import Path
from ultralytics import YOLO

def export_to_coreml(weights_path, output_dir="artifacts/ios/model"):
    """Export YOLOv8 model to CoreML format."""
    
    weights_path = Path(weights_path)
    if not weights_path.exists():
        print(f"❌ Error: Model file not found: {weights_path}")
        return False
    
    print(f"📦 Loading model from: {weights_path}")
    model = YOLO(str(weights_path))
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔄 Exporting to CoreML format...")
    print("   This may take a few minutes...")
    
    try:
        # Export to CoreML
        exported_path = model.export(
            format='coreml',
            imgsz=640,        # Image size (matches training)
            half=False,       # Use FP32 for better accuracy (FP16 can cause issues)
            nms=True,         # Include NMS in model
            project=str(output_dir.parent),
            name=output_dir.name,
            exist_ok=True
        )
        
        exported_path = Path(exported_path)
        
        if exported_path.exists():
            size_mb = exported_path.stat().st_size / (1024 * 1024)
            print(f"\n✅ Model exported successfully!")
            print(f"   Location: {exported_path}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"\n📱 Next steps:")
            print(f"   1. Open Xcode project")
            print(f"   2. Drag '{exported_path.name}' into Xcode")
            print(f"   3. Make sure it's added to your app target")
            print(f"   4. Build and run!")
            return True
        else:
            print(f"❌ Error: Export completed but file not found at {exported_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Default to best.pt from training results
    default_weights = "results/yolov8s_rdd2022_high_perf/weights/best.pt"
    
    weights_path = sys.argv[1] if len(sys.argv) > 1 else default_weights
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "artifacts/ios/model"
    
    print("=" * 60)
    print("YOLOv8 to CoreML Export Tool")
    print("=" * 60)
    print()
    
    success = export_to_coreml(weights_path, output_dir)
    
    sys.exit(0 if success else 1)

