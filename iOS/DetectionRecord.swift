//
//  DetectionRecord.swift
//  RoadDefectDetector
//
//  Data model for storing detection history
//

import Foundation
import UIKit
import CoreLocation

/// Detection record stored in history
struct DetectionRecord: Codable, Identifiable {
    let id: UUID
    let date: Date
    let imageData: Data
    let detections: [DetectionData]
    let location: LocationData?
    
    struct DetectionData: Codable {
        let className: String
        let confidence: Float
        let boundingBox: BoundingBox
        
        struct BoundingBox: Codable {
            let x: Double
            let y: Double
            let width: Double
            let height: Double
        }
    }
    
    struct LocationData: Codable {
        let latitude: Double
        let longitude: Double
        let address: String?
    }
    
    init(id: UUID = UUID(), date: Date = Date(), image: UIImage, detections: [Detection], location: LocationData?) {
        self.id = id
        self.date = date
        self.imageData = image.jpegData(compressionQuality: 0.8) ?? Data()
        self.detections = detections.map { detection in
            DetectionData(
                className: detection.className,
                confidence: detection.confidence,
                boundingBox: DetectionData.BoundingBox(
                    x: Double(detection.boundingBox.origin.x),
                    y: Double(detection.boundingBox.origin.y),
                    width: Double(detection.boundingBox.width),
                    height: Double(detection.boundingBox.height)
                )
            )
        }
        self.location = location
    }
    
    var image: UIImage? {
        return UIImage(data: imageData)
    }
}
