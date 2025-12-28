//
//  ResultsView.swift
//  RoadDefectDetector
//
//  Beautiful results view with photo saving
//

import SwiftUI

struct ResultsView: View {
    let image: UIImage
    let detections: [Detection]
    let engine: DetectionEngine
    let originalImage: UIImage?
    let locationService: LocationService
    let history: DetectionHistory
    let onSave: (UIImage) -> Void
    let onDelete: (() -> Void)?
    
    @State private var annotatedImage: UIImage?
    @State private var isProcessing = false
    @State private var showShareSheet = false
    @State private var showSaveAlert = false
    @State private var showReport = false
    @State private var showDeleteConfirmation = false
    
    var body: some View {
        ZStack {
            // Background
            Color(red: 0.97, green: 0.98, blue: 1.0)
                .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 24) {
                    // Image Section with beautiful card
                    VStack(spacing: 0) {
                        if let annotatedImage = annotatedImage {
                            Image(uiImage: annotatedImage)
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .clipShape(RoundedRectangle(cornerRadius: 20))
                        } else {
                            ZStack {
                                Image(uiImage: image)
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .clipShape(RoundedRectangle(cornerRadius: 20))
                                
                                if isProcessing {
                                    VStack(spacing: 16) {
                                        ProgressView()
                                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                            .scaleEffect(1.5)
                                        Text("Generating annotations...")
                                            .font(.system(size: 16, weight: .medium))
                                            .foregroundColor(.white)
                                    }
                                    .padding(30)
                                    .background(
                                        RoundedRectangle(cornerRadius: 20)
                                            .fill(Color.black.opacity(0.6))
                                    )
                                }
                            }
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 20)
                    .shadow(color: Color.black.opacity(0.1), radius: 20, x: 0, y: 10)
                    
                    // Action Buttons
                    VStack(spacing: 12) {
                        // Primary Actions Row
                        HStack(spacing: 12) {
                            // Save Button
                            Button(action: {
                                if let annotated = annotatedImage {
                                    onSave(annotated)
                                }
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "square.and.arrow.down.fill")
                                    Text("Save")
                                }
                                .font(.system(size: 16, weight: .semibold, design: .rounded))
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
                                .background(
                                    LinearGradient(
                                        gradient: Gradient(colors: [
                                            Color(red: 0.2, green: 0.5, blue: 0.9),
                                            Color(red: 0.4, green: 0.6, blue: 1.0)
                                        ]),
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .cornerRadius(16)
                            }
                            
                            // Share Button
                            Button(action: {
                                showShareSheet = true
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "square.and.arrow.up.fill")
                                    Text("Share")
                                }
                                .font(.system(size: 16, weight: .semibold, design: .rounded))
                                .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
                                .background(
                                    RoundedRectangle(cornerRadius: 16)
                                        .fill(Color.white)
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 16)
                                                .stroke(Color(red: 0.2, green: 0.5, blue: 0.9), lineWidth: 2)
                                        )
                                )
                            }
                            
                            // Delete Button (if onDelete callback provided)
                            if let onDelete = onDelete {
                                Button(action: {
                                    showDeleteConfirmation = true
                                }) {
                                    Image(systemName: "trash.fill")
                                        .font(.system(size: 18, weight: .semibold, design: .rounded))
                                        .foregroundColor(.white)
                                        .frame(width: 52, height: 52)
                                        .background(
                                            LinearGradient(
                                                gradient: Gradient(colors: [
                                                    Color(red: 1.0, green: 0.3, blue: 0.3),
                                                    Color(red: 1.0, green: 0.5, blue: 0.3)
                                                ]),
                                                startPoint: .topLeading,
                                                endPoint: .bottomTrailing
                                            )
                                        )
                                        .cornerRadius(16)
                                }
                            }
                        }
                        
                        // Report Button (if detections found)
                        if !detections.isEmpty {
                            Button(action: {
                                saveToHistory()
                                showReport = true
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "exclamationmark.bubble.fill")
                                    Text("Report to Authority")
                                }
                                .font(.system(size: 17, weight: .semibold, design: .rounded))
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
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
                                .cornerRadius(16)
                            }
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    // Results Summary Card
                    VStack(spacing: 0) {
                        // Header
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Detection Results")
                                    .font(.system(size: 24, weight: .bold, design: .rounded))
                                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                                
                                if detections.isEmpty {
                                    Text("No defects found")
                                        .font(.system(size: 16, weight: .medium))
                                        .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                                } else {
                                    Text("\(detections.count) defect\(detections.count == 1 ? "" : "s") detected")
                                        .font(.system(size: 16, weight: .medium))
                                        .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                                }
                            }
                            Spacer()
                            
                            // Success indicator
                            if !detections.isEmpty {
                                ZStack {
                                    Circle()
                                        .fill(Color.green.opacity(0.15))
                                        .frame(width: 50, height: 50)
                                    
                                    Image(systemName: "checkmark.circle.fill")
                                        .font(.system(size: 30))
                                        .foregroundColor(.green)
                                }
                            }
                        }
                        .padding(20)
                        
                        Divider()
                        
                        // Detections List
                        if detections.isEmpty {
                            VStack(spacing: 16) {
                                Image(systemName: "checkmark.shield.fill")
                                    .font(.system(size: 60))
                                    .foregroundColor(Color.green.opacity(0.6))
                                
                                Text("Great news!")
                                    .font(.system(size: 20, weight: .bold, design: .rounded))
                                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                                
                                Text("No road defects were detected in this image.")
                                    .font(.system(size: 16, weight: .medium))
                                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                                    .multilineTextAlignment(.center)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 40)
                        } else {
                            VStack(spacing: 12) {
                                ForEach(Array(detections.enumerated()), id: \.offset) { index, detection in
                                    BeautifulDetectionRow(
                                        detection: detection,
                                        engine: engine,
                                        index: index + 1
                                    )
                                }
                            }
                            .padding(20)
                        }
                    }
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .shadow(color: Color.black.opacity(0.05), radius: 15, x: 0, y: 5)
                    )
                    .padding(.horizontal, 20)
                    .padding(.bottom, 30)
                }
            }
        }
        .navigationTitle("Results")
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            generateAnnotatedImage()
        }
        .sheet(isPresented: $showShareSheet) {
            if let imageToShare = annotatedImage ?? image {
                ShareSheet(activityItems: [imageToShare])
            }
        }
        .sheet(isPresented: $showReport) {
            if let location = locationService.getCurrentLocation() {
                let record = DetectionRecord(image: image, detections: detections, location: location)
                ReportView(record: record)
            }
        }
        .alert("Delete Photo", isPresented: $showDeleteConfirmation) {
            Button("Cancel", role: .cancel) { }
            Button("Delete", role: .destructive) {
                onDelete?()
            }
        } message: {
            Text("Are you sure you want to delete this photo? This action cannot be undone.")
        }
    }
    
    private func saveToHistory() {
        let location = locationService.getCurrentLocation()
        let record = DetectionRecord(image: image, detections: detections, location: location)
        history.save(record: record)
    }
    
    private func generateAnnotatedImage() {
        isProcessing = true
        DispatchQueue.global(qos: .userInitiated).async {
            let annotated = ImageProcessor.drawDetections(
                image: image,
                detections: detections,
                engine: engine
            )
            DispatchQueue.main.async {
                self.annotatedImage = annotated
                self.isProcessing = false
            }
        }
    }
}

// Beautiful detection row with modern design
struct BeautifulDetectionRow: View {
    let detection: Detection
    let engine: DetectionEngine
    let index: Int
    
    var body: some View {
        HStack(spacing: 16) {
            // Index Badge
            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            gradient: Gradient(colors: [
                                engine.color(for: detection.className),
                                engine.color(for: detection.className).opacity(0.7)
                            ]),
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 44, height: 44)
                
                Text("\(index)")
                    .font(.system(size: 18, weight: .bold, design: .rounded))
                    .foregroundColor(.white)
            }
            
            // Detection Info
            VStack(alignment: .leading, spacing: 6) {
                Text(engine.description(for: detection.className))
                    .font(.system(size: 18, weight: .bold, design: .rounded))
                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                
                Text("Class: \(detection.className)")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
            }
            
            Spacer()
            
            // Confidence Badge
            VStack(spacing: 2) {
                Text("\(Int(detection.confidence * 100))%")
                    .font(.system(size: 20, weight: .bold, design: .rounded))
                    .foregroundColor(engine.color(for: detection.className))
                
                Text("confidence")
                    .font(.system(size: 10, weight: .medium))
                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(engine.color(for: detection.className).opacity(0.12))
            )
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color(red: 0.98, green: 0.99, blue: 1.0))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(engine.color(for: detection.className).opacity(0.2), lineWidth: 1)
                )
        )
    }
}

// Share sheet for sharing images
struct ShareSheet: UIViewControllerRepresentable {
    let activityItems: [Any]
    
    func makeUIViewController(context: Context) -> UIActivityViewController {
        let controller = UIActivityViewController(
            activityItems: activityItems,
            applicationActivities: nil
        )
        return controller
    }
    
    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}

struct ResultsView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            ResultsView(
                image: UIImage(systemName: "photo")!,
                detections: [
                    Detection(
                        className: "D00",
                        confidence: 0.85,
                        boundingBox: CGRect(x: 0.1, y: 0.1, width: 0.3, height: 0.2)
                    ),
                    Detection(
                        className: "D11",
                        confidence: 0.72,
                        boundingBox: CGRect(x: 0.5, y: 0.5, width: 0.2, height: 0.2)
                    )
                ],
                engine: DetectionEngine(),
                originalImage: UIImage(systemName: "photo"),
                locationService: LocationService(),
                history: DetectionHistory(),
                onSave: { _ in },
                onDelete: nil
            )
        }
    }
}
