# Phase 4: Municipal Reporting Feature - Documentation Notes

## Feature Description for Thesis

### Municipal Reporting System with Contact Information

The iOS application includes a comprehensive municipal reporting system that enables users to directly contact road maintenance authorities based on their location. This feature addresses the practical need for reporting detected road defects to the appropriate municipal authorities.

#### Key Components

1. **Municipal Contact Database**
   - Contains contact information for road maintenance authorities in 25+ countries
   - Each entry includes:
     - Organization name
     - Department name
     - Phone number
     - Email address
     - Website URL
     - Physical address
     - Jurisdiction information

2. **Automatic Authority Identification**
   - Uses GPS coordinates to automatically identify the user's location
   - Determines the country/jurisdiction based on coordinates
   - Retrieves the appropriate municipal authority contact information
   - Eliminates the need for users to manually search for contact details

3. **One-Tap Communication Features**
   - **Direct Calling**: Tap-to-call functionality that initiates phone calls directly from the app
   - **Email Composition**: Pre-filled email with defect report details, ready to send
   - **Website Access**: Direct links to municipal authority websites
   - **Share Functionality**: Share complete defect reports via messages or email

#### Supported Countries

The system includes contact information for road maintenance authorities in:
- Turkey, Germany, France, Spain, Italy, Netherlands, Belgium
- Poland, Portugal, Greece, Czech Republic, Romania, Hungary
- Sweden, Norway, Denmark, Finland, Austria, Switzerland, Ireland
- United States, United Kingdom, Canada, Australia
- And more...

#### Implementation Details

**Location-Based Authority Lookup:**
- Uses reverse geocoding to determine country from GPS coordinates
- Maps coordinates to appropriate country codes
- Retrieves corresponding authority information from database

**Contact Information Structure:**
```swift
struct Authority {
    let name: String           // Organization name
    let department: String     // Department name
    let phone: String          // Phone number
    let email: String?         // Email address
    let website: String?       // Website URL
    let address: String?       // Physical address
    let jurisdiction: String   // Country/jurisdiction
}
```

**User Interface:**
- Displays complete contact information in organized format
- Provides interactive buttons for calling and emailing
- Shows formatted report with defect details and location
- Enables sharing of complete reports

#### Practical Benefits

1. **Streamlined Reporting Process**
   - Users don't need to search for contact information
   - Automatic identification of correct authority
   - Pre-filled report with all relevant details

2. **Direct Communication**
   - One-tap calling eliminates manual dialing
   - Pre-composed emails with defect information
   - Reduces barriers to reporting

3. **Comprehensive Information**
   - All contact methods available (phone, email, website)
   - Complete authority details for reference
   - Location-specific information

4. **Enhanced Usability**
   - Seamless integration with iOS native features
   - Professional presentation of contact information
   - Clear call-to-action buttons

#### Integration with Detection System

- Automatically triggered when user taps "Report" button
- Uses GPS coordinates from detection record
- Includes detection details in report message:
  - Date and time of detection
  - Number of defects found
  - Defect types and confidence scores
  - GPS coordinates and address
  - Contact information for relevant authority

#### Technical Implementation

**ReportService.swift:**
- Contains authority database with contact information
- Implements location-based authority lookup
- Formats contact information for display
- Creates formatted report messages

**ReportView.swift:**
- Displays contact information in user-friendly format
- Implements one-tap calling and email functionality
- Provides share functionality for reports
- Handles user interactions

#### Future Enhancements

- Integration with government APIs for real-time authority information
- Support for local/municipal level authorities (not just national)
- Multi-language support for contact information
- Integration with municipal reporting systems/APIs
- Offline caching of frequently accessed authorities

---

## How to Include in Thesis (Chapter 4 - Methodology / Chapter 5 - Results)

### In Methodology Chapter:
"The mobile application includes a comprehensive municipal reporting system that enables users to directly contact road maintenance authorities. The system maintains a database of contact information (phone numbers, email addresses, websites, and addresses) for road maintenance authorities in 25+ countries. Using GPS coordinates from detected defects, the system automatically identifies the appropriate municipal authority and provides one-tap calling and email functionality for direct reporting."

### In Results Chapter (RQ3):
"The reporting system includes a municipal contact database with phone numbers and email addresses for road maintenance authorities in 25+ countries. The system automatically identifies the correct authority based on GPS coordinates and provides one-tap communication features, including direct calling and pre-filled email composition. This eliminates the need for users to manually search for contact information and streamlines the reporting process, enhancing the practical effectiveness of the application for field workers."

---

**This feature significantly enhances the practical value of the application for municipal reporting, which is a key aspect of the thesis title "On-Device Road Damage Detection for Municipal Reporting".**

