//
//  HistoryView.swift
//  RoadDefectDetector
//
//  View to display detection history
//

import SwiftUI
import UIKit

struct HistoryView: View {
    @ObservedObject var history: DetectionHistory
    @ObservedObject var engine: DetectionEngine
    @State private var selectedRecord: DetectionRecord?
    @State private var showDetails = false
    @State private var showReport = false
    @State private var recordToReport: DetectionRecord?
    @State private var selectionMode = false
    @State private var selectedRecords: Set<UUID> = []
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background
                Color(red: 0.97, green: 0.98, blue: 1.0)
                    .ignoresSafeArea()
                
                if history.records.isEmpty {
                    // Empty state
                    VStack(spacing: 24) {
                        Image(systemName: "photo.on.rectangle.angled")
                            .font(.system(size: 80))
                            .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9).opacity(0.5))
                        
                        Text("No Detection History")
                            .font(.system(size: 24, weight: .bold, design: .rounded))
                            .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                        
                        Text("Your road defect detections will appear here")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, 40)
                    }
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(history.records) { record in
                                HistoryRecordCard(
                                    record: record,
                                    engine: engine,
                                    isSelected: selectedRecords.contains(record.id),
                                    selectionMode: selectionMode,
                                    onTap: {
                                        if selectionMode {
                                            if selectedRecords.contains(record.id) {
                                                selectedRecords.remove(record.id)
                                            } else {
                                                selectedRecords.insert(record.id)
                                            }
                                        } else {
                                            selectedRecord = record
                                            showDetails = true
                                        }
                                    },
                                    onReport: {
                                        recordToReport = record
                                        showReport = true
                                    }
                                )
                            }
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle(selectionMode ? "\(selectedRecords.count) Selected" : "Detection History")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    if selectionMode {
                        Button("Cancel") {
                            selectionMode = false
                            selectedRecords.removeAll()
                        }
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    if !history.records.isEmpty {
                        HStack {
                            if !selectionMode {
                                // Select button
                                Button(action: {
                                    selectionMode = true
                                }) {
                                    Text("Select")
                                        .font(.system(size: 16, weight: .semibold))
                                        .foregroundColor(.blue)
                                }
                                
                                // Menu for other actions
                                Menu {
                                    Button(role: .destructive, action: {
                                        history.deleteAll()
                                    }) {
                                        Label("Delete All", systemImage: "trash")
                                    }
                                } label: {
                                    Image(systemName: "ellipsis.circle")
                                        .foregroundColor(.blue)
                                }
                            } else {
                                // Share selected button
                                if !selectedRecords.isEmpty {
                                    Button(action: {
                                        shareSelectedImages()
                                    }) {
                                        Image(systemName: "square.and.arrow.up.fill")
                                            .foregroundColor(.blue)
                                    }
                                }
                                
                                // Delete selected button
                                if !selectedRecords.isEmpty {
                                    Button(role: .destructive, action: {
                                        deleteSelectedRecords()
                                    }) {
                                        Image(systemName: "trash.fill")
                                            .foregroundColor(.red)
                                    }
                                }
                            }
                        }
                    }
                }
            }
            .sheet(item: $selectedRecord) { record in
                HistoryDetailView(record: record, engine: engine)
            }
            .sheet(item: $recordToReport) { record in
                ReportView(record: record)
            }
        }
    }
    
    private func shareSelectedImages() {
        let recordsToShare = history.records.filter { selectedRecords.contains($0.id) }
        let images = recordsToShare.compactMap { $0.image }
        
        guard !images.isEmpty else { return }
        
        let activityVC = UIActivityViewController(activityItems: images, applicationActivities: nil)
        
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let rootViewController = windowScene.windows.first?.rootViewController {
            rootViewController.present(activityVC, animated: true)
            selectionMode = false
            selectedRecords.removeAll()
        }
    }
    
    private func deleteSelectedRecords() {
        let recordsToDelete = history.records.filter { selectedRecords.contains($0.id) }
        for record in recordsToDelete {
            history.delete(record: record)
        }
        selectionMode = false
        selectedRecords.removeAll()
    }
}

struct HistoryRecordCard: View {
    let record: DetectionRecord
    let engine: DetectionEngine
    let isSelected: Bool
    let selectionMode: Bool
    let onTap: () -> Void
    let onReport: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                // Selection indicator
                if selectionMode {
                    ZStack {
                        Circle()
                            .fill(isSelected ? Color.blue : Color.clear)
                            .frame(width: 28, height: 28)
                            .overlay(
                                Circle()
                                    .stroke(isSelected ? Color.blue : Color.gray, lineWidth: 2)
                                    .frame(width: 28, height: 28)
                            )
                        
                        if isSelected {
                            Image(systemName: "checkmark")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(.white)
                        }
                    }
                }
                
                // Thumbnail
                if let image = record.image {
                    ZStack(alignment: .topTrailing) {
                        Image(uiImage: image)
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                            .frame(width: 80, height: 80)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(isSelected ? Color.blue : Color.clear, lineWidth: 3)
                            )
                    }
                }
                
                // Info
                VStack(alignment: .leading, spacing: 8) {
                    Text(formatDate(record.date))
                        .font(.system(size: 18, weight: .bold, design: .rounded))
                        .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                    
                    Text("\(record.detections.count) defect\(record.detections.count == 1 ? "" : "s") detected")
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                    
                    if let location = record.location {
                        HStack(spacing: 4) {
                            Image(systemName: "location.fill")
                                .font(.system(size: 12))
                            Text(location.address ?? "\(String(format: "%.4f", location.latitude)), \(String(format: "%.4f", location.longitude))")
                                .font(.system(size: 12, weight: .medium))
                        }
                        .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                    }
                    
                    // Defect types
                    HStack(spacing: 8) {
                        ForEach(Array(Set(record.detections.map { $0.className })), id: \.self) { className in
                            Text(className)
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(.white)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(engine.color(for: className))
                                .cornerRadius(6)
                        }
                    }
                }
                
                Spacer()
                
                // Report button (only show when not in selection mode)
                if !selectionMode {
                    Button(action: onReport) {
                        Image(systemName: "exclamationmark.bubble.fill")
                            .font(.system(size: 20))
                            .foregroundColor(.white)
                            .frame(width: 44, height: 44)
                            .background(
                                LinearGradient(
                                    gradient: Gradient(colors: [
                                        Color(red: 1.0, green: 0.3, blue: 0.3),
                                        Color(red: 1.0, green: 0.5, blue: 0.3)
                                    ]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(12)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(isSelected ? Color.blue.opacity(0.1) : Color.white)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(isSelected ? Color.blue : Color.clear, lineWidth: 2)
                    )
                    .shadow(color: Color.black.opacity(0.05), radius: 10, x: 0, y: 5)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        if Calendar.current.isDateInToday(date) {
            formatter.dateStyle = .none
            formatter.timeStyle = .short
            return "Today, \(formatter.string(from: date))"
        } else if Calendar.current.isDateInYesterday(date) {
            formatter.dateStyle = .none
            formatter.timeStyle = .short
            return "Yesterday, \(formatter.string(from: date))"
        } else {
            formatter.dateStyle = .medium
            formatter.timeStyle = .short
            return formatter.string(from: date)
        }
    }
}

struct HistoryDetailView: View {
    let record: DetectionRecord
    let engine: DetectionEngine
    @Environment(\.dismiss) var dismiss
    @State private var annotatedImage: UIImage?
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Image
                    if let image = annotatedImage ?? record.image {
                        Image(uiImage: image)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .clipShape(RoundedRectangle(cornerRadius: 20))
                            .padding(.horizontal)
                    }
                    
                    // Info card
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Detection Details")
                            .font(.system(size: 24, weight: .bold, design: .rounded))
                        
                        // Date
                        InfoRow(icon: "calendar", title: "Date", value: formatDate(record.date))
                        
                        // Location
                        if let location = record.location {
                            InfoRow(
                                icon: "location.fill",
                                title: "Location",
                                value: location.address ?? "\(String(format: "%.6f", location.latitude)), \(String(format: "%.6f", location.longitude))"
                            )
                        }
                        
                        Divider()
                        
                        // Defections
                        Text("Defects Found (\(record.detections.count))")
                            .font(.system(size: 20, weight: .bold, design: .rounded))
                        
                        ForEach(Array(record.detections.enumerated()), id: \.offset) { index, detection in
                            BeautifulDetectionRow(
                                detection: Detection(
                                    className: detection.className,
                                    confidence: detection.confidence,
                                    boundingBox: CGRect(
                                        x: detection.boundingBox.x,
                                        y: detection.boundingBox.y,
                                        width: detection.boundingBox.width,
                                        height: detection.boundingBox.height
                                    )
                                ),
                                engine: engine,
                                index: index + 1
                            )
                        }
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .shadow(color: Color.black.opacity(0.05), radius: 15, x: 0, y: 5)
                    )
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationTitle("Detection Details")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .onAppear {
                generateAnnotatedImage()
            }
        }
    }
    
    private func generateAnnotatedImage() {
        guard let image = record.image else { return }
        
        let detections = record.detections.map { detectionData in
            Detection(
                className: detectionData.className,
                confidence: detectionData.confidence,
                boundingBox: CGRect(
                    x: detectionData.boundingBox.x,
                    y: detectionData.boundingBox.y,
                    width: detectionData.boundingBox.width,
                    height: detectionData.boundingBox.height
                )
            )
        }
        
        annotatedImage = ImageProcessor.drawDetections(
            image: image,
            detections: detections,
            engine: engine
        )
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}

struct InfoRow: View {
    let icon: String
    let title: String
    let value: String
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                .frame(width: 24)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                Text(value)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
            }
            
            Spacer()
        }
    }
}
