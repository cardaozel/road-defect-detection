//
//  ImageProcessor.swift
//  RoadDefectDetector
//
//  Image preprocessing utilities for YOLOv8 input
//

import UIKit
import CoreGraphics

/// Image preprocessing utilities
class ImageProcessor {
    
    /// Target input size for YOLOv8 model (640x640)
    static let inputSize: CGFloat = 640
    
    /// Preprocess image for YOLOv8 inference
    /// - Parameter image: Input image
    /// - Returns: Preprocessed image ready for model input
    static func preprocess(image: UIImage) -> UIImage? {
        // Resize to 640x640 while maintaining aspect ratio (letterbox)
        return resizeWithLetterbox(image: image, targetSize: inputSize)
    }
    
    /// Resize image to target size with letterbox (maintains aspect ratio)
    /// - Parameters:
    ///   - image: Source image
    ///   - targetSize: Target square size
    /// - Returns: Resized image with letterbox padding
    static func resizeWithLetterbox(image: UIImage, targetSize: CGFloat) -> UIImage? {
        let size = image.size
        let scale = min(targetSize / size.width, targetSize / size.height)
        let newSize = CGSize(width: size.width * scale, height: size.height * scale)
        
        // Create image renderer
        let renderer = UIGraphicsImageRenderer(size: CGSize(width: targetSize, height: targetSize))
        
        return renderer.image { context in
            // Fill with black background (letterbox)
            UIColor.black.setFill()
            context.fill(CGRect(x: 0, y: 0, width: targetSize, height: targetSize))
            
            // Calculate position to center the scaled image
            let xOffset = (targetSize - newSize.width) / 2
            let yOffset = (targetSize - newSize.height) / 2
            let rect = CGRect(x: xOffset, y: yOffset, width: newSize.width, height: newSize.height)
            
            // Draw scaled image
            image.draw(in: rect)
        }
    }
    
    /// Convert normalized bounding box coordinates to image coordinates
    /// - Parameters:
    ///   - normalizedBox: Normalized bounding box (0-1 range)
    ///   - imageSize: Size of the image
    ///   - letterboxOffset: Offset due to letterbox padding
    /// - Returns: Bounding box in image coordinates
    static func convertToImageCoordinates(
        normalizedBox: CGRect,
        imageSize: CGSize,
        letterboxOffset: CGPoint
    ) -> CGRect {
        // YOLOv8 outputs normalized coordinates (0-1)
        // Need to convert to image pixel coordinates
        let x = normalizedBox.origin.x * imageSize.width - letterboxOffset.x
        let y = normalizedBox.origin.y * imageSize.height - letterboxOffset.y
        let width = normalizedBox.width * imageSize.width
        let height = normalizedBox.height * imageSize.height
        
        // Convert from center-based to origin-based coordinates if needed
        // (YOLOv8 uses center-based, Vision uses origin-based)
        let originX = x - width / 2
        let originY = y - height / 2
        
        return CGRect(x: originX, y: originY, width: width, height: height)
    }
    
    /// Calculate letterbox offset for coordinate conversion
    /// - Parameters:
    ///   - originalSize: Original image size
    ///   - targetSize: Target size (640x640)
    /// - Returns: Offset point
    static func letterboxOffset(originalSize: CGSize, targetSize: CGFloat) -> CGPoint {
        let scale = min(targetSize / originalSize.width, targetSize / originalSize.height)
        let scaledWidth = originalSize.width * scale
        let scaledHeight = originalSize.height * scale
        
        let xOffset = (targetSize - scaledWidth) / 2
        let yOffset = (targetSize - scaledHeight) / 2
        
        return CGPoint(x: xOffset, y: yOffset)
    }
    
    /// Draw detection results on image
    /// - Parameters:
    ///   - image: Source image
    ///   - detections: Detection results
    ///   - engine: Detection engine for colors and descriptions
    /// - Returns: Annotated image with bounding boxes and labels
    static func drawDetections(
        image: UIImage,
        detections: [Detection],
        engine: DetectionEngine
    ) -> UIImage? {
        let renderer = UIGraphicsImageRenderer(size: image.size)
        
        return renderer.image { context in
            // Draw original image
            image.draw(at: .zero)
            
            // Draw each detection
            for detection in detections {
                let color = engine.color(for: detection.className)
                let description = engine.description(for: detection.className)
                let confidencePercent = Int(detection.confidence * 100)
                
                // Convert normalized coordinates to image coordinates
                let boundingBox = CGRect(
                    x: detection.boundingBox.origin.x * image.size.width,
                    y: detection.boundingBox.origin.y * image.size.height,
                    width: detection.boundingBox.width * image.size.width,
                    height: detection.boundingBox.height * image.size.height
                )
                
                // Draw bounding box with beautiful styling
                context.cgContext.setStrokeColor(color.cgColor)
                context.cgContext.setLineWidth(4.0)  // Thicker line for visibility
                context.cgContext.setLineCap(.round)
                context.cgContext.setLineJoin(.round)
                context.cgContext.stroke(boundingBox)
                
                // Draw label with beautiful background
                let labelText = "\(description) \(confidencePercent)%"
                let fontSize: CGFloat = max(16, min(image.size.width / 30, 20))  // Scale font with image size
                let font = UIFont.boldSystemFont(ofSize: fontSize)
                let attributes: [NSAttributedString.Key: Any] = [
                    .font: font,
                    .foregroundColor: UIColor.white
                ]
                let attributedString = NSAttributedString(string: labelText, attributes: attributes)
                let textSize = attributedString.size()
                
                // Label background with padding and rounded corners
                let padding: CGFloat = 8
                let cornerRadius: CGFloat = 8
                var labelRect = CGRect(
                    x: boundingBox.origin.x,
                    y: max(0, boundingBox.origin.y - textSize.height - padding * 2),
                    width: textSize.width + padding * 2,
                    height: textSize.height + padding * 2
                )
                
                // Ensure label doesn't go off screen
                if labelRect.maxX > image.size.width {
                    labelRect.origin.x = image.size.width - labelRect.width
                }
                if labelRect.minY < 0 {
                    labelRect.origin.y = boundingBox.maxY + 4
                }
                
                // Draw rounded rectangle background
                let path = UIBezierPath(
                    roundedRect: labelRect,
                    cornerRadius: cornerRadius
                )
                color.setFill()
                path.fill()
                
                // Add subtle shadow for depth
                context.cgContext.setShadow(
                    offset: CGSize(width: 0, height: 2),
                    blur: 4,
                    color: UIColor.black.withAlphaComponent(0.3).cgColor
                )
                path.fill()
                context.cgContext.setShadow(offset: .zero, blur: 0, color: nil)
                
                // Draw label text
                labelText.draw(
                    in: labelRect.insetBy(dx: padding, dy: padding),
                    withAttributes: attributes
                )
            }
        }
    }
}
