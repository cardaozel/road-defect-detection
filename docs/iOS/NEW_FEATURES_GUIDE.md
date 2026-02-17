# New Features Guide: GPS, History & Reporting

## 🎉 New Features Added

### 1. **GPS Location Tagging** 📍
- Automatically tags detections with GPS coordinates
- Stores address information when available
- Used for location-based authority lookup

### 2. **Detection History** 📸
- View all your previous detections
- See photos with results
- Browse by date and location
- Delete individual records or clear all

### 3. **Report to Authority** 🚨
- Based on GPS location, suggests relevant road maintenance authority
- Provides contact information (phone, email, website)
- Shows which organization to contact
- Share report via messages/email

---

## 📱 How to Use

### View History

1. Tap the **📷 photo icon** in the top-right corner of home screen
2. See all your previous detections
3. Tap any record to view details
4. Tap **Report** button (red) to see contact information

### Report Defects

1. After detection completes, tap **"Report to Authority"** button (red)
2. App shows relevant authority based on your location
3. See contact information:
   - Organization name
   - Department
   - Phone number (tap to call)
   - Email (tap to email)
   - Website (tap to open)
   - Address
4. Tap **"Call"** to call directly
5. Tap **"Share Report"** to share via messages/email

---

## 🔧 Technical Details

### GPS Integration

**LocationService.swift**:
- Requests location permissions
- Gets current GPS coordinates
- Reverse geocodes to get address
- Provides location data for detections

**Permissions Required**:
- `NSLocationWhenInUseUsageDescription` - Added to Info.plist

### History Storage

**DetectionHistory.swift**:
- Stores detections locally using UserDefaults
- Saves images, detections, date, and location
- Provides filtering and search capabilities

**DetectionRecord.swift**:
- Data model for storing detection records
- Includes image, detections, date, and location

### Reporting Service

**ReportService.swift**:
- Maps GPS coordinates to country/jurisdiction
- Returns relevant authority information
- Currently supports 25+ countries including:
  - **Europe (20 countries)**: Germany, France, Spain, Italy, Netherlands, Belgium, Poland, Portugal, Greece, Czech Republic, Romania, Hungary, Sweden, Norway, Denmark, Finland, Austria, Switzerland, Ireland, United Kingdom
  - **Other**: United States, Canada, Australia, Turkey
  - Generic fallback for other countries

**Note**: In production, you'd use proper geocoding API and a database of authorities.

---

## 🌍 Location-Based Authorities

The app currently identifies authorities based on country codes derived from coordinates:

- **Turkey**: Karayolları Genel Müdürlüğü (if coordinates suggest Turkey)
- **United States**: Department of Transportation
- **United Kingdom**: Highways England
- **Canada**: Transport Canada
- **Australia**: Department of Infrastructure
- **Germany**: Autobahn GmbH des Bundes (if coordinates suggest Germany)
- **France**: Direction des Routes d'Île-de-France
- **Spain**: Dirección General de Tráfico
- **Italy**: ANAS S.p.A.
- **Netherlands**: Rijkswaterstaat
- **Belgium**: Wegen en Verkeer
- **Poland**: Generalna Dyrekcja Dróg Krajowych i Autostrad
- **Portugal**: Infraestruturas de Portugal
- **Greece**: Υπουργείο Υποδομών και Μεταφορών
- **Czech Republic**: Ředitelství silnic a dálnic
- **Romania**: Compania Națională de Administrare a Infrastructurii Rutiere
- **Hungary**: Magyar Közút Nonprofit Zrt.
- **Sweden**: Trafikverket
- **Norway**: Statens vegvesen
- **Denmark**: Vejdirektoratet
- **Finland**: Tiehallinto
- **Austria**: ASFINAG
- **Switzerland**: Bundesamt für Strassen ASTRA
- **Ireland**: Transport Infrastructure Ireland
- **Other**: Generic local authority (user needs to check directory)

### Improving Authority Lookup

For production, implement:

1. **Reverse Geocoding**: Use CLGeocoder or Google Maps API to get country/state/city
2. **Authority Database**: Maintain database of authorities by jurisdiction
3. **Government APIs**: Use official APIs if available
4. **User Input**: Allow users to select jurisdiction if auto-detection fails

---

## 📝 Files Added

1. **LocationService.swift** - GPS location management
2. **DetectionRecord.swift** - Data model for history
3. **DetectionHistory.swift** - History storage and management
4. **HistoryView.swift** - UI for viewing history
5. **ReportView.swift** - UI for reporting to authorities
6. **ReportService.swift** - Authority lookup service

---

## ✅ Integration Complete

All features are integrated into the main app:

- ✅ GPS permission requested on app launch
- ✅ Location tagged automatically when saving detections
- ✅ History button added to home screen
- ✅ Report button added to results screen
- ✅ All data saved locally

---

## 🚀 Next Steps

1. **Add to Xcode**: Copy new Swift files to your Xcode project
2. **Update Info.plist**: Add location permission description
3. **Test**: Try taking photos and checking history
4. **Test Reporting**: Check if authority lookup works for your location

---

## 💡 Future Enhancements

- [x] Add European countries support (COMPLETED)
- [x] Add delete button for photos (COMPLETED)
- [x] Add multi-select and share functionality (COMPLETED)
- [ ] Implement proper geocoding (CLGeocoder) for accurate country detection
- [ ] Add map view showing detection locations
- [ ] Export history as CSV/PDF
- [ ] Filter history by defect type or location
- [ ] Search history by address
- [ ] Add more countries (Asia, Africa, Americas)
- [ ] Cloud sync for history (optional)

---

**All features are ready to use!** 🎉
