#!/usr/bin/env python3
"""Generate app icon for Road Defect Detector iOS app - Damaged Road Design."""

from PIL import Image, ImageDraw, ImageFont
import os
import math
from pathlib import Path


def create_app_icon(output_dir: Path, size: int = 1024):
    """Create a beautiful app icon showing a damaged road for iOS."""
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a new image with transparent background
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (blue gradient - matches app theme)
    # Top-left: Deep blue (#3366E6)
    # Bottom-right: Bright blue (#6699FF)
    for y in range(size):
        ratio = y / size
        r = int(51 + (102 - 51) * ratio)  # 0x33 to 0x66
        g = int(102 + (153 - 102) * ratio)  # 0x66 to 0x99
        b = int(230 + (255 - 230) * ratio)  # 0xE6 to 0xFF
        color = (r, g, b)
        draw.rectangle([(0, y), (size, y + 1)], fill=color)
    
    # Calculate road dimensions
    center = size // 2
    road_width = int(size * 0.7)  # Road takes up 70% of icon
    road_height = int(size * 0.5)
    road_x = (size - road_width) // 2
    road_y = int(size * 0.35)  # Positioned in upper-middle
    
    # Draw road surface with realistic gray color
    road_color = (80, 80, 85)  # Dark gray for asphalt
    road_shadow = (60, 60, 65)  # Darker for depth
    
    # Road shadow/border for depth
    shadow_offset = 3
    draw.rectangle(
        [road_x + shadow_offset, road_y + shadow_offset, 
         road_x + road_width + shadow_offset, road_y + road_height + shadow_offset],
        fill=road_shadow
    )
    
    # Main road surface
    draw.rectangle(
        [road_x, road_y, road_x + road_width, road_y + road_height],
        fill=road_color
    )
    
    # Add texture to road (small dots for asphalt texture)
    for i in range(0, road_width, 8):
        for j in range(0, road_height, 8):
            if (i + j) % 16 == 0:
                dot_color = (70, 70, 75) if (i + j) % 32 == 0 else (90, 90, 95)
                draw.ellipse(
                    [road_x + i, road_y + j, road_x + i + 2, road_y + j + 2],
                    fill=dot_color
                )
    
    # Draw lane divider (dashed yellow line)
    center_x = size // 2
    dash_length = 40
    dash_gap = 25
    line_y = road_y + road_height // 2
    line_width = 4
    
    x = road_x
    while x < road_x + road_width:
        draw.rectangle(
            [x, line_y - line_width // 2, min(x + dash_length, road_x + road_width), line_y + line_width // 2],
            fill=(255, 200, 0)  # Yellow
        )
        x += dash_length + dash_gap
    
    # Draw road defects - CRACKS (Longitudinal - Blue)
    # Main crack running along the road
    crack_start_x = road_x + int(road_width * 0.2)
    crack_y1 = road_y + int(road_height * 0.3)
    crack_y2 = road_y + int(road_height * 0.7)
    
    # Draw jagged crack line
    points = []
    current_y = crack_y1
    current_x = crack_start_x
    while current_y < crack_y2:
        points.append((current_x, current_y))
        current_y += 8
        # Add some jaggedness to the crack
        current_x += int((current_y - crack_y1) % 20) - 10
    
    if len(points) > 1:
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(0, 122, 255), width=5)  # iOS Blue
    
    # Draw transverse crack (perpendicular - Red)
    transverse_x1 = road_x + int(road_width * 0.6)
    transverse_x2 = road_x + int(road_width * 0.85)
    transverse_y = road_y + int(road_height * 0.45)
    
    points = []
    current_x = transverse_x1
    current_y = transverse_y
    while current_x < transverse_x2:
        points.append((current_x, current_y))
        current_x += 8
        current_y += int((current_x - transverse_x1) % 15) - 7
    
    if len(points) > 1:
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(255, 59, 48), width=5)  # iOS Red
    
    # Draw alligator crack pattern (network of cracks - Orange)
    alligator_center_x = road_x + int(road_width * 0.4)
    alligator_center_y = road_y + int(road_height * 0.6)
    alligator_size = 60
    
    # Draw network of interconnected cracks
    for angle in range(0, 360, 45):
        start_x = alligator_center_x
        start_y = alligator_center_y
        end_x = alligator_center_x + int(alligator_size * 0.6 * math.cos(math.radians(angle)))
        end_y = alligator_center_y + int(alligator_size * 0.6 * math.sin(math.radians(angle)))
        
        # Draw small cracks radiating from center
        for i in range(3):
            offset = i * 8
            draw.line(
                [start_x + offset, start_y + offset, end_x + offset, end_y + offset],
                fill=(255, 149, 0), width=3  # iOS Orange
            )
    
    # Draw POTHOLES (Purple circles)
    # Pothole 1
    pothole1_x = road_x + int(road_width * 0.75)
    pothole1_y = road_y + int(road_height * 0.35)
    pothole1_size = 25
    
    # Pothole shadow (darker circle)
    draw.ellipse(
        [pothole1_x - pothole1_size + 2, pothole1_y - pothole1_size + 2,
         pothole1_x + pothole1_size + 2, pothole1_y + pothole1_size + 2],
        fill=(50, 50, 55)
    )
    
    # Main pothole (purple)
    draw.ellipse(
        [pothole1_x - pothole1_size, pothole1_y - pothole1_size,
         pothole1_x + pothole1_size, pothole1_y + pothole1_size],
        fill=(175, 82, 222)  # iOS Purple
    )
    
    # Pothole inner (darker center)
    draw.ellipse(
        [pothole1_x - pothole1_size // 2, pothole1_y - pothole1_size // 2,
         pothole1_x + pothole1_size // 2, pothole1_y + pothole1_size // 2],
        fill=(120, 50, 160)
    )
    
    # Pothole 2 (smaller)
    pothole2_x = road_x + int(road_width * 0.55)
    pothole2_y = road_y + int(road_height * 0.7)
    pothole2_size = 18
    
    draw.ellipse(
        [pothole2_x - pothole2_size + 2, pothole2_y - pothole2_size + 2,
         pothole2_x + pothole2_size + 2, pothole2_y + pothole2_size + 2],
        fill=(50, 50, 55)
    )
    draw.ellipse(
        [pothole2_x - pothole2_size, pothole2_y - pothole2_size,
         pothole2_x + pothole2_size, pothole2_y + pothole2_size],
        fill=(175, 82, 222)
    )
    
    # Add some additional small cracks
    # Small crack on left side
    small_crack_x = road_x + int(road_width * 0.15)
    small_crack_y = road_y + int(road_height * 0.5)
    draw.line(
        [small_crack_x, small_crack_y, small_crack_x + 30, small_crack_y + 20],
        fill=(0, 122, 255), width=3
    )
    
    # Save the icon
    icon_path = output_dir / 'AppIcon.png'
    img.save(icon_path, 'PNG')
    print(f"✅ Created app icon: {icon_path}")
    
    # Also create different sizes for iOS
    ios_sizes = [
        (20, 'AppIcon-20.png'),      # Notification
        (29, 'AppIcon-29.png'),      # Settings
        (40, 'AppIcon-40.png'),      # Spotlight
        (60, 'AppIcon-60.png'),      # App
        (76, 'AppIcon-76.png'),      # iPad
        (83.5, 'AppIcon-83.5.png'),  # iPad Pro
        (1024, 'AppIcon-1024.png')   # App Store
    ]
    
    for icon_size, filename in ios_sizes:
        # Resize the icon
        resized = img.resize((int(icon_size * 2), int(icon_size * 2)), Image.Resampling.LANCZOS)
        # Crop to square if needed
        if resized.width != resized.height:
            min_dim = min(resized.width, resized.height)
            left = (resized.width - min_dim) // 2
            top = (resized.height - min_dim) // 2
            resized = resized.crop((left, top, left + min_dim, top + min_dim))
        
        output_path = output_dir / filename
        resized.save(output_path, 'PNG')
        print(f"✅ Created {filename} ({icon_size}pt @2x)")
    
    return icon_path


def create_app_icon_set(output_dir: Path):
    """Create iOS app icon set structure."""
    iconset_dir = output_dir / 'AppIcon.appiconset'
    iconset_dir.mkdir(parents=True, exist_ok=True)
    
    # Create Contents.json for Xcode
    contents_json = {
        "images": [
            {
                "filename": "AppIcon-20.png",
                "idiom": "iphone",
                "scale": "2x",
                "size": "20x20"
            },
            {
                "filename": "AppIcon-20.png",
                "idiom": "iphone",
                "scale": "3x",
                "size": "20x20"
            },
            {
                "filename": "AppIcon-29.png",
                "idiom": "iphone",
                "scale": "2x",
                "size": "29x29"
            },
            {
                "filename": "AppIcon-29.png",
                "idiom": "iphone",
                "scale": "3x",
                "size": "29x29"
            },
            {
                "filename": "AppIcon-40.png",
                "idiom": "iphone",
                "scale": "2x",
                "size": "40x40"
            },
            {
                "filename": "AppIcon-40.png",
                "idiom": "iphone",
                "scale": "3x",
                "size": "40x40"
            },
            {
                "filename": "AppIcon-60.png",
                "idiom": "iphone",
                "scale": "2x",
                "size": "60x60"
            },
            {
                "filename": "AppIcon-60.png",
                "idiom": "iphone",
                "scale": "3x",
                "size": "60x60"
            },
            {
                "filename": "AppIcon-20.png",
                "idiom": "ipad",
                "scale": "1x",
                "size": "20x20"
            },
            {
                "filename": "AppIcon-20.png",
                "idiom": "ipad",
                "scale": "2x",
                "size": "20x20"
            },
            {
                "filename": "AppIcon-29.png",
                "idiom": "ipad",
                "scale": "1x",
                "size": "29x29"
            },
            {
                "filename": "AppIcon-29.png",
                "idiom": "ipad",
                "scale": "2x",
                "size": "29x29"
            },
            {
                "filename": "AppIcon-40.png",
                "idiom": "ipad",
                "scale": "1x",
                "size": "40x40"
            },
            {
                "filename": "AppIcon-40.png",
                "idiom": "ipad",
                "scale": "2x",
                "size": "40x40"
            },
            {
                "filename": "AppIcon-76.png",
                "idiom": "ipad",
                "scale": "1x",
                "size": "76x76"
            },
            {
                "filename": "AppIcon-76.png",
                "idiom": "ipad",
                "scale": "2x",
                "size": "76x76"
            },
            {
                "filename": "AppIcon-83.5.png",
                "idiom": "ipad",
                "scale": "2x",
                "size": "83.5x83.5"
            },
            {
                "filename": "AppIcon-1024.png",
                "idiom": "ios-marketing",
                "scale": "1x",
                "size": "1024x1024"
            }
        ],
        "info": {
            "author": "xcode",
            "version": 1
        }
    }
    
    import json
    contents_path = iconset_dir / 'Contents.json'
    with open(contents_path, 'w') as f:
        json.dump(contents_json, f, indent=2)
    
    print(f"✅ Created AppIcon.appiconset structure")
    return iconset_dir


if __name__ == '__main__':
    import sys
    from pathlib import Path
    
    # Default output directory
    output_dir = Path('iOS/AppIcon')
    
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    
    print(f"Generating damaged road app icon in: {output_dir}")
    print("=" * 60)
    
    # Create the main icon
    create_app_icon(output_dir, size=1024)
    
    # Create iOS app icon set structure
    create_app_icon_set(output_dir)
    
    print("=" * 60)
    print("✅ App icon generation complete!")
    print(f"\nNew design: Realistic damaged road with:")
    print("  - Cracks (blue - longitudinal, red - transverse)")
    print("  - Alligator cracks (orange - network pattern)")
    print("  - Potholes (purple)")
    print("  - Road surface texture")
    print(f"\nTo use in Xcode:")
    print(f"1. Drag '{output_dir}/AppIcon.appiconset' folder into Xcode")
    print(f"2. Or copy individual PNG files to Assets.xcassets/AppIcon.appiconset/")
    print(f"\nMain icon file: {output_dir}/AppIcon-1024.png")
