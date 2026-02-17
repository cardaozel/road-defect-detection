//
//  DetectionEngine.swift
//  RoadDefectDetector
//
//  CoreML inference engine for YOLOv8 road defect detection
//

import Foundation
import CoreML
import Vision
import UIKit
import Combine

/// Detection result containing bounding box and confidence
struct Detection {
    let className: String
    let confidence: Float
    let boundingBox: CGRect
}

/// CoreML-based detection engine for road defects
class DetectionEngine: ObservableObject {
    
    // MARK: - Properties
    
    private var model: VNCoreMLModel?
    private let classNames = ["D00", "D01", "D10", "D11", "D20", "D40"]
    private let classDescriptions = [
        "D00": "Longitudinal Crack",
        "D01": "Transverse Crack",
        "D10": "Alligator Crack",
        "D11": "Pothole",
        "D20": "Marking Blur",
        "D40": "Road Repair"
    ]
    
    // Confidence threshold (adjust based on your model performance)
    var confidenceThreshold: Float = 0.4
    
    // MARK: - Initialization
    
    init() {
        loadModel()
    }
    
    /// Load CoreML model
    private func loadModel() {
        // Debug: List all bundle resources
        if let resourcePath = Bundle.main.resourcePath {
            print("📦 Bundle resource path: \(resourcePath)")
            if let contents = try? FileManager.default.contentsOfDirectory(atPath: resourcePath) {
                print("📦 Bundle contents (\(contents.count) items):")
                for item in contents.prefix(20) {
                    print("   - \(item)")
                }
            }
        }
        
        // Try .mlpackage first (newer format), then .mlmodel (older format)
        var modelURL = Bundle.main.url(forResource: "best", withExtension: "mlpackage")
        if modelURL == nil {
            print("⚠️ best.mlpackage not found, trying .mlmodel...")
            modelURL = Bundle.main.url(forResource: "best", withExtension: "mlmodel")
        }
        
        guard let modelURL = modelURL else {
            print("❌ Model file not found in bundle (tried both .mlpackage and .mlmodel)")
            print("❌ Make sure 'best.mlpackage' is added to your Xcode project target:")
            print("   1. Open Xcode")
            print("   2. Select 'best.mlpackage' in Project Navigator")
            print("   3. In File Inspector, check 'Target Membership' → 'RoadDefectDetector'")
            print("   4. Clean build folder (Cmd+Shift+K) and rebuild")
            return
        }
        
        print("✅ Found model at: \(modelURL.path)")
        
        do {
            // Compile model if needed
            let compiledURL = try MLModel.compileModel(at: modelURL)
            let mlModel = try MLModel(contentsOf: compiledURL)
            
            // Create Vision framework wrapper
            guard let vnModel = try? VNCoreMLModel(for: mlModel) else {
                print("❌ Failed to create VNCoreMLModel")
                return
            }
            
            self.model = vnModel
            print("✅ Model loaded successfully")
        } catch {
            print("❌ Error loading model: \(error.localizedDescription)")
            print("❌ Full error: \(error)")
        }
    }
    
    // MARK: - Detection
    
    /// Detect road defects in an image
    /// - Parameters:
    ///   - image: Input image
    ///   - completion: Callback with detection results
    func detect(image: UIImage, completion: @escaping ([Detection]) -> Void) {
        guard let model = model else {
            print("❌ Model not loaded")
            completion([])
            return
        }
        
        guard let ciImage = CIImage(image: image) else {
            print("❌ Failed to create CIImage")
            completion([])
            return
        }
        
        // Create Vision request
        let request = VNCoreMLRequest(model: model) { [weak self] request, error in
            guard let self = self else { return }
            
            if let error = error {
                print("❌ Detection error: \(error)")
                completion([])
                return
            }
            
            guard let observations = request.results as? [VNRecognizedObjectObservation] else {
                // Handle YOLOv8 output format (may need custom post-processing)
                let detections = self.processYOLOv8Output(request: request, imageSize: image.size)
                completion(detections)
                return
            }
            
            // Process observations
            let detections = observations.compactMap { observation -> Detection? in
                guard observation.confidence >= self.confidenceThreshold,
                      let topLabelObservation = observation.labels.first else {
                    return nil
                }
                
                let className = topLabelObservation.identifier
                let confidence = topLabelObservation.confidence
                let boundingBox = observation.boundingBox
                
                return Detection(
                    className: className,
                    confidence: confidence,
                    boundingBox: boundingBox
                )
            }
            
            completion(detections)
        }
        
        // Configure request
        request.imageCropAndScaleOption = .scaleFill
        
        // Perform request on background queue
        let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try handler.perform([request])
            } catch {
                print("❌ Error performing detection: \(error)")
                DispatchQueue.main.async {
                    completion([])
                }
            }
        }
    }
    
    /// Process YOLOv8 raw output (custom post-processing if needed)
    private func processYOLOv8Output(request: VNRequest, imageSize: CGSize) -> [Detection] {
        // YOLOv8 CoreML export outputs MLMultiArray
        // Note: If you export with --nms flag, output format will be different
        
        var detections: [Detection] = []
        
        // Try to get MLFeatureValue from request
        guard let observations = request.results else {
            return detections
        }
        
        // If CoreML model includes NMS, output will be in VNRecognizedObjectObservation format
        // Otherwise, we need to parse MLMultiArray manually
        for observation in observations {
            if let objObservation = observation as? VNRecognizedObjectObservation {
                guard objObservation.confidence >= confidenceThreshold,
                      let topLabel = objObservation.labels.first else {
                    continue
                }
                
                let detection = Detection(
                    className: topLabel.identifier,
                    confidence: topLabel.confidence,
                    boundingBox: objObservation.boundingBox
                )
                detections.append(detection)
            }
        }
        
        // If no observations found, try direct MLMultiArray parsing
        // (This would require accessing the underlying MLModel directly)
        
        return detections
    }
    
    // MARK: - Helper Methods
    
    /// Get human-readable description for class name
    func description(for className: String) -> String {
        return classDescriptions[className] ?? className
    }
    
    /// Get color for class (for visualization) - Beautiful iOS colors
    func color(for className: String) -> UIColor {
        let colors: [String: UIColor] = [
            "D00": UIColor(red: 0.0, green: 0.48, blue: 1.0, alpha: 1.0),      // iOS Blue - Longitudinal crack
            "D01": UIColor(red: 1.0, green: 0.23, blue: 0.19, alpha: 1.0),     // iOS Red - Transverse crack
            "D10": UIColor(red: 1.0, green: 0.58, blue: 0.0, alpha: 1.0),      // iOS Orange - Alligator crack
            "D11": UIColor(red: 0.69, green: 0.32, blue: 0.87, alpha: 1.0),    // iOS Purple - Pothole
            "D20": UIColor(red: 1.0, green: 0.8, blue: 0.0, alpha: 1.0),       // iOS Yellow - Marking blur
            "D40": UIColor(red: 0.20, green: 0.78, blue: 0.35, alpha: 1.0)     // iOS Green - Road repair
        ]
        return colors[className] ?? .systemGray
    }
}
