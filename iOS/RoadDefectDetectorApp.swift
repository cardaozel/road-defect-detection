//
//  RoadDefectDetectorApp.swift
//  RoadDefectDetector
//
//  Main app entry point - Beautiful, modern UI/UX
//

import SwiftUI
import Photos

@main
struct RoadDefectDetectorApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @StateObject private var detectionEngine = DetectionEngine()
    @StateObject private var locationService = LocationService()
    @StateObject private var history = DetectionHistory()
    @State private var selectedImage: UIImage?
    @State private var detections: [Detection] = []
    @State private var showCamera = false
    @State private var showPhotoLibrary = false
    @State private var showResults = false
    @State private var showHistory = false
    @State private var isProcessing = false
    @State private var showSaveSuccess = false
    
    // Beautiful gradient colors
    private let gradientColors = [
        Color(red: 0.2, green: 0.4, blue: 0.9),  // Deep blue
        Color(red: 0.4, green: 0.6, blue: 1.0),  // Bright blue
        Color(red: 0.5, green: 0.7, blue: 0.95)  // Light blue
    ]
    
    var body: some View {
        NavigationView {
            ZStack {
                // Beautiful gradient background
                LinearGradient(
                    gradient: Gradient(colors: [
                        Color(red: 0.95, green: 0.97, blue: 1.0),
                        Color(red: 0.98, green: 0.99, blue: 1.0)
                    ]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 0) {
                        // Hero Section with beautiful design
                        VStack(spacing: 24) {
                            // App Icon with gradient
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(
                                            gradient: Gradient(colors: gradientColors),
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 120, height: 120)
                                    .shadow(color: Color.blue.opacity(0.3), radius: 20, x: 0, y: 10)
                                
                                Image(systemName: "road.lanes")
                                    .font(.system(size: 60, weight: .medium))
                                    .foregroundColor(.white)
                            }
                            .padding(.top, 40)
                            
                            // App Title
                            VStack(spacing: 8) {
                                Text("Road Defect")
                                    .font(.system(size: 36, weight: .bold, design: .rounded))
                                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                                
                                Text("Detector")
                                    .font(.system(size: 36, weight: .bold, design: .rounded))
                                    .foregroundStyle(
                                        LinearGradient(
                                            gradient: Gradient(colors: gradientColors),
                                            startPoint: .leading,
                                            endPoint: .trailing
                                        )
                                    )
                            }
                            
                            // Subtitle
                            Text("AI-powered road defect detection\nInstant, accurate, and reliable")
                                .font(.system(size: 16, weight: .medium))
                                .foregroundColor(Color(red: 0.4, green: 0.4, blue: 0.5))
                                .multilineTextAlignment(.center)
                                .lineSpacing(4)
                                .padding(.horizontal, 40)
                        }
                        .padding(.bottom, 50)
                        
                        // Action Buttons with beautiful design
                        VStack(spacing: 20) {
                            // Camera Button - Primary Action
                            Button(action: {
                                showCamera = true
                            }) {
                                HStack(spacing: 16) {
                                    Image(systemName: "camera.fill")
                                        .font(.system(size: 24, weight: .semibold))
                                    Text("Take Photo")
                                        .font(.system(size: 20, weight: .semibold, design: .rounded))
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 64)
                                .background(
                                    LinearGradient(
                                        gradient: Gradient(colors: gradientColors),
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .cornerRadius(20)
                                .shadow(color: Color.blue.opacity(0.4), radius: 15, x: 0, y: 8)
                            }
                            .disabled(isProcessing)
                            .scaleEffect(isProcessing ? 0.95 : 1.0)
                            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isProcessing)
                            
                            // Photo Library Button - Secondary Action
                            Button(action: {
                                showPhotoLibrary = true
                            }) {
                                HStack(spacing: 16) {
                                    Image(systemName: "photo.on.rectangle.angled")
                                        .font(.system(size: 22, weight: .semibold))
                                    Text("Choose from Library")
                                        .font(.system(size: 18, weight: .semibold, design: .rounded))
                                }
                                .foregroundColor(Color(red: 0.2, green: 0.4, blue: 0.9))
                                .frame(maxWidth: .infinity)
                                .frame(height: 64)
                                .background(
                                    RoundedRectangle(cornerRadius: 20)
                                        .fill(Color.white)
                                        .shadow(color: Color.black.opacity(0.08), radius: 10, x: 0, y: 5)
                                )
                                .overlay(
                                    RoundedRectangle(cornerRadius: 20)
                                        .stroke(
                                            LinearGradient(
                                                gradient: Gradient(colors: gradientColors),
                                                startPoint: .leading,
                                                endPoint: .trailing
                                            ),
                                            lineWidth: 2
                                        )
                                )
                            }
                            .disabled(isProcessing)
                            
                            // Processing Indicator
                            if isProcessing {
                                HStack(spacing: 12) {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: Color.blue))
                                    Text("Analyzing image...")
                                        .font(.system(size: 16, weight: .medium))
                                        .foregroundColor(Color(red: 0.4, green: 0.4, blue: 0.5))
                                }
                                .padding(.top, 20)
                                .transition(.opacity.combined(with: .scale))
                            }
                        }
                        .padding(.horizontal, 32)
                        .padding(.bottom, 50)
                        
                        // Info Cards - Defect Types
                        VStack(spacing: 16) {
                            Text("Supported Defect Types")
                                .font(.system(size: 20, weight: .bold, design: .rounded))
                                .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                                .padding(.bottom, 8)
                            
                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 12) {
                                DefectTypeCard(
                                    icon: "line.diagonal",
                                    title: "Cracks",
                                    description: "Longitudinal & Transverse",
                                    color: Color(red: 0.2, green: 0.5, blue: 0.9)
                                )
                                DefectTypeCard(
                                    icon: "circle.grid.cross.fill",
                                    title: "Alligator",
                                    description: "Network cracks",
                                    color: Color(red: 1.0, green: 0.58, blue: 0.0)
                                )
                                DefectTypeCard(
                                    icon: "circle.circle.fill",
                                    title: "Pothole",
                                    description: "Road depression",
                                    color: Color(red: 0.69, green: 0.32, blue: 0.87)
                                )
                                DefectTypeCard(
                                    icon: "square.fill.on.circle.fill",
                                    title: "Other",
                                    description: "Marking & Repair",
                                    color: Color(red: 0.20, green: 0.78, blue: 0.35)
                                )
                            }
                        }
                        .padding(.horizontal, 32)
                        .padding(.bottom, 50)
                    }
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showHistory = true
                    }) {
                        Image(systemName: "photo.on.rectangle")
                            .font(.system(size: 20, weight: .medium))
                            .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                    }
                }
            }
            .sheet(isPresented: $showHistory) {
                HistoryView(history: history, engine: detectionEngine)
            }
            .sheet(isPresented: $showCamera) {
                CameraView(capturedImage: $selectedImage, isPresented: $showCamera)
            }
            .sheet(isPresented: $showPhotoLibrary) {
                PhotoLibraryView(selectedImage: $selectedImage, isPresented: $showPhotoLibrary)
            }
            .onChange(of: selectedImage) { newImage in
                if let image = newImage {
                    processImage(image)
                }
            }
            .sheet(isPresented: $showResults) {
                if let image = selectedImage {
                    NavigationView {
                        ResultsView(
                            image: image,
                            detections: detections,
                            engine: detectionEngine,
                            originalImage: selectedImage,
                            locationService: locationService,
                            history: history,
                            onSave: { savedImage in
                                saveImageToPhotoLibrary(savedImage)
                                saveToHistory(image: image)
                            },
                            onDelete: {
                                showResults = false
                                selectedImage = nil
                                detections = []
                            }
                        )
                        .toolbar {
                            ToolbarItem(placement: .navigationBarLeading) {
                                Button(action: {
                                    showResults = false
                                    selectedImage = nil
                                    detections = []
                                }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: "xmark.circle.fill")
                                        Text("Close")
                                    }
                                    .font(.system(size: 16, weight: .medium))
                                    .foregroundColor(.blue)
                                }
                            }
                        }
                    }
                }
            }
            .onAppear {
                locationService.requestPermission()
                locationService.startLocationUpdates()
            }
            .alert("Photo Saved!", isPresented: $showSaveSuccess) {
                Button("OK", role: .cancel) { }
            } message: {
                Text("Your annotated photo has been saved to your photo library.")
            }
        }
    }
    
    private func processImage(_ image: UIImage) {
        isProcessing = true
        
        DispatchQueue.global(qos: .userInitiated).async {
            detectionEngine.detect(image: image) { results in
                DispatchQueue.main.async {
                    self.detections = results
                    self.isProcessing = false
                    self.showResults = true
                }
            }
        }
    }
    
    private func saveImageToPhotoLibrary(_ image: UIImage) {
        PHPhotoLibrary.requestAuthorization { status in
            guard status == .authorized else {
                print("Photo library access denied")
                return
            }
            
            PHPhotoLibrary.shared().performChanges({
                PHAssetChangeRequest.creationRequestForAsset(from: image)
            }) { success, error in
                DispatchQueue.main.async {
                    if success {
                        self.showSaveSuccess = true
                    } else {
                        print("Error saving photo: \(error?.localizedDescription ?? "Unknown")")
                    }
                }
            }
        }
    }
    
    private func saveToHistory(image: UIImage) {
        let location = locationService.getCurrentLocation()
        let record = DetectionRecord(image: image, detections: detections, location: location)
        history.save(record: record)
    }
}

// Beautiful defect type card component
struct DefectTypeCard: View {
    let icon: String
    let title: String
    let description: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 32, weight: .medium))
                .foregroundColor(color)
                .frame(height: 40)
            
            Text(title)
                .font(.system(size: 14, weight: .bold, design: .rounded))
                .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
            
            Text(description)
                .font(.system(size: 11, weight: .medium))
                .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                .multilineTextAlignment(.center)
                .lineLimit(2)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 20)
        .padding(.horizontal, 12)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
        )
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
