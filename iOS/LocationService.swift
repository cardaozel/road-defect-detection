//
//  LocationService.swift
//  RoadDefectDetector
//
//  GPS location service for tagging detections
//

import Foundation
import CoreLocation
import Contacts

class LocationService: NSObject, ObservableObject {
    private let locationManager = CLLocationManager()
    
    @Published var currentLocation: CLLocation?
    @Published var authorizationStatus: CLAuthorizationStatus = .notDetermined
    @Published var locationError: String?
    @Published var currentAddress: String?
    
    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.distanceFilter = 10 // Update every 10 meters
    }
    
    func requestPermission() {
        locationManager.requestWhenInUseAuthorization()
    }
    
    func startLocationUpdates() {
        guard authorizationStatus == .authorizedWhenInUse || authorizationStatus == .authorizedAlways else {
            requestPermission()
            return
        }
        
        locationManager.startUpdatingLocation()
    }
    
    func stopLocationUpdates() {
        locationManager.stopUpdatingLocation()
    }
    
    func getCurrentLocation() -> DetectionRecord.LocationData? {
        guard let location = currentLocation else { return nil }
        
        return DetectionRecord.LocationData(
            latitude: location.coordinate.latitude,
            longitude: location.coordinate.longitude,
            address: currentAddress
        )
    }
    
    private func reverseGeocode(location: CLLocation) {
        let geocoder = CLGeocoder()
        geocoder.reverseGeocodeLocation(location) { [weak self] placemarks, error in
            guard let self = self else { return }
            
            if let error = error {
                self.locationError = "Failed to get address: \(error.localizedDescription)"
                return
            }
            
            if let placemark = placemarks?.first {
                var addressComponents: [String] = []
                
                if let street = placemark.thoroughfare {
                    addressComponents.append(street)
                }
                if let city = placemark.locality {
                    addressComponents.append(city)
                }
                if let state = placemark.administrativeArea {
                    addressComponents.append(state)
                }
                if let country = placemark.country {
                    addressComponents.append(country)
                }
                
                self.currentAddress = addressComponents.joined(separator: ", ")
            }
        }
    }
}

extension LocationService: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        currentLocation = location
        reverseGeocode(location: location)
        locationError = nil
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        locationError = error.localizedDescription
        currentLocation = nil
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        authorizationStatus = manager.authorizationStatus
        
        switch authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            startLocationUpdates()
        case .denied, .restricted:
            locationError = "Location permission denied. Please enable it in Settings."
        case .notDetermined:
            requestPermission()
        @unknown default:
            break
        }
    }
}
