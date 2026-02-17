//
//  DetectionHistory.swift
//  RoadDefectDetector
//
//  Manages detection history storage
//

import Foundation
import SwiftUI
import Combine

class DetectionHistory: ObservableObject {
    @Published var records: [DetectionRecord] = []
    
    private let storageKey = "detection_history"
    
    init() {
        loadHistory()
    }
    
    /// Save a new detection record
    func save(record: DetectionRecord) {
        records.insert(record, at: 0) // Add to beginning (newest first)
        saveHistory()
    }
    
    /// Delete a record
    func delete(record: DetectionRecord) {
        records.removeAll { $0.id == record.id }
        saveHistory()
    }
    
    /// Delete all records
    func deleteAll() {
        records.removeAll()
        saveHistory()
    }
    
    /// Get records filtered by defect type
    func records(filteredBy className: String) -> [DetectionRecord] {
        return records.filter { record in
            record.detections.contains { $0.className == className }
        }
    }
    
    /// Load history from UserDefaults
    private func loadHistory() {
        guard let data = UserDefaults.standard.data(forKey: storageKey) else {
            records = []
            return
        }
        
        do {
            let decoder = JSONDecoder()
            records = try decoder.decode([DetectionRecord].self, from: data)
        } catch {
            print("Error loading history: \(error)")
            records = []
        }
    }
    
    /// Save history to UserDefaults
    private func saveHistory() {
        do {
            let encoder = JSONEncoder()
            let data = try encoder.encode(records)
            UserDefaults.standard.set(data, forKey: storageKey)
        } catch {
            print("Error saving history: \(error)")
        }
    }
}
