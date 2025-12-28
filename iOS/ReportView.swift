//
//  ReportView.swift
//  RoadDefectDetector
//
//  View to show reporting information based on location
//

import SwiftUI

struct ReportView: View {
    let record: DetectionRecord
    @Environment(\.dismiss) var dismiss
    @State private var authority: ReportService.Authority?
    
    var body: some View {
        NavigationView {
            ZStack {
                Color(red: 0.97, green: 0.98, blue: 1.0)
                    .ignoresSafeArea()
                
                if let authority = authority {
                    ScrollView {
                        VStack(spacing: 24) {
                            // Header
                            VStack(spacing: 12) {
                                Image(systemName: "exclamationmark.shield.fill")
                                    .font(.system(size: 60))
                                    .foregroundColor(Color(red: 1.0, green: 0.3, blue: 0.3))
                                
                                Text("Report Road Defects")
                                    .font(.system(size: 28, weight: .bold, design: .rounded))
                                    .foregroundColor(Color(red: 0.1, green: 0.1, blue: 0.2))
                                
                                Text("Contact the relevant authority to report these road defects")
                                    .font(.system(size: 16, weight: .medium))
                                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                                    .multilineTextAlignment(.center)
                                    .padding(.horizontal)
                            }
                            .padding(.top)
                            
                            // Authority Information Card
                            VStack(alignment: .leading, spacing: 20) {
                                Text("Contact Information")
                                    .font(.system(size: 22, weight: .bold, design: .rounded))
                                
                                // Organization
                                ContactRow(
                                    icon: "building.2.fill",
                                    title: "Organization",
                                    value: authority.name
                                )
                                
                                // Department
                                ContactRow(
                                    icon: "person.3.fill",
                                    title: "Department",
                                    value: authority.department
                                )
                                
                                Divider()
                                
                                // Phone
                                if let phoneURL = URL(string: "tel://\(authority.phone.replacingOccurrences(of: " ", with: "").replacingOccurrences(of: "-", with: ""))") {
                                    Link(destination: phoneURL) {
                                        ContactRow(
                                            icon: "phone.fill",
                                            title: "Phone",
                                            value: authority.phone,
                                            isAction: true
                                        )
                                    }
                                    .buttonStyle(PlainButtonStyle())
                                } else {
                                    ContactRow(
                                        icon: "phone.fill",
                                        title: "Phone",
                                        value: authority.phone
                                    )
                                }
                                
                                // Email
                                if let email = authority.email, let emailURL = URL(string: "mailto:\(email)") {
                                    Link(destination: emailURL) {
                                        ContactRow(
                                            icon: "envelope.fill",
                                            title: "Email",
                                            value: email,
                                            isAction: true
                                        )
                                    }
                                    .buttonStyle(PlainButtonStyle())
                                }
                                
                                // Website
                                if let website = authority.website, let websiteURL = URL(string: website) {
                                    Link(destination: websiteURL) {
                                        ContactRow(
                                            icon: "safari.fill",
                                            title: "Website",
                                            value: website,
                                            isAction: true
                                        )
                                    }
                                    .buttonStyle(PlainButtonStyle())
                                }
                                
                                // Address
                                if let address = authority.address {
                                    ContactRow(
                                        icon: "mappin.circle.fill",
                                        title: "Address",
                                        value: address
                                    )
                                }
                                
                                // Jurisdiction
                                ContactRow(
                                    icon: "globe",
                                    title: "Jurisdiction",
                                    value: authority.jurisdiction
                                )
                            }
                            .padding()
                            .background(
                                RoundedRectangle(cornerRadius: 20)
                                    .fill(Color.white)
                                    .shadow(color: Color.black.opacity(0.05), radius: 15, x: 0, y: 5)
                            )
                            .padding(.horizontal)
                            
                            // Action Buttons
                            VStack(spacing: 16) {
                                // Call Button
                                if let phoneURL = URL(string: "tel://\(authority.phone.replacingOccurrences(of: " ", with: "").replacingOccurrences(of: "-", with: ""))") {
                                    Link(destination: phoneURL) {
                                        HStack {
                                            Image(systemName: "phone.fill")
                                            Text("Call \(authority.name)")
                                        }
                                        .font(.system(size: 18, weight: .semibold, design: .rounded))
                                        .foregroundColor(.white)
                                        .frame(maxWidth: .infinity)
                                        .frame(height: 56)
                                        .background(
                                            LinearGradient(
                                                gradient: Gradient(colors: [
                                                    Color.green,
                                                    Color(red: 0.0, green: 0.7, blue: 0.3)
                                                ]),
                                                startPoint: .leading,
                                                endPoint: .trailing
                                            )
                                        )
                                        .cornerRadius(16)
                                    }
                                }
                                
                                // Share Report Button
                                Button(action: shareReport) {
                                    HStack {
                                        Image(systemName: "square.and.arrow.up.fill")
                                        Text("Share Report")
                                    }
                                    .font(.system(size: 18, weight: .semibold, design: .rounded))
                                    .foregroundColor(Color(red: 0.2, green: 0.5, blue: 0.9))
                                    .frame(maxWidth: .infinity)
                                    .frame(height: 56)
                                    .background(
                                        RoundedRectangle(cornerRadius: 16)
                                            .fill(Color.white)
                                            .overlay(
                                                RoundedRectangle(cornerRadius: 16)
                                                    .stroke(Color(red: 0.2, green: 0.5, blue: 0.9), lineWidth: 2)
                                            )
                                    )
                                }
                            }
                            .padding(.horizontal)
                            .padding(.bottom, 30)
                        }
                    }
                } else {
                    ProgressView("Loading contact information...")
                }
            }
            .navigationTitle("Report Defects")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .onAppear {
                loadAuthority()
            }
        }
    }
    
    private func loadAuthority() {
        guard let location = record.location else {
            // Default authority if no location
            authority = ReportService.Authority(
                name: "Local Road Authority",
                department: "Road Maintenance",
                phone: "Check local directory",
                email: nil,
                website: nil,
                address: nil,
                jurisdiction: "Local"
            )
            return
        }
        
        authority = ReportService.getAuthority(for: location)
    }
    
    private func shareReport() {
        guard let authority = authority else { return }
        
        let message = ReportService.createReportMessage(for: record, authority: authority)
        let activityVC = UIActivityViewController(activityItems: [message], applicationActivities: nil)
        
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let rootViewController = windowScene.windows.first?.rootViewController {
            rootViewController.present(activityVC, animated: true)
        }
    }
}

struct ContactRow: View {
    let icon: String
    let title: String
    let value: String
    var isAction: Bool = false
    
    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: icon)
                .font(.system(size: 20))
                .foregroundColor(isAction ? Color(red: 0.2, green: 0.5, blue: 0.9) : Color(red: 0.5, green: 0.5, blue: 0.6))
                .frame(width: 30)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
                Text(value)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(isAction ? Color(red: 0.2, green: 0.5, blue: 0.9) : Color(red: 0.1, green: 0.1, blue: 0.2))
            }
            
            Spacer()
            
            if isAction {
                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(Color(red: 0.5, green: 0.5, blue: 0.6))
            }
        }
        .padding(.vertical, 4)
    }
}
