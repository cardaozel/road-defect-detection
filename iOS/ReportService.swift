//
//  ReportService.swift
//  RoadDefectDetector
//
//  Service to find relevant authorities based on location
//

import Foundation
import CoreLocation

/// Service to find relevant road maintenance authorities
class ReportService {
    
    /// Road maintenance authority information
    struct Authority {
        let name: String
        let department: String
        let phone: String
        let email: String?
        let website: String?
        let address: String?
        let jurisdiction: String
    }
    
    /// Get relevant authority based on location
    static func getAuthority(for location: DetectionRecord.LocationData) -> Authority {
        // This is a simplified version - in production, you'd use:
        // 1. Geocoding API to get country/state/city
        // 2. Database of authorities by jurisdiction
        // 3. Government API if available
        
        // For now, we'll return generic information based on country
        // In a real app, you'd implement proper lookup
        
        // Try to determine country from coordinates
        // This is a placeholder - implement proper geocoding
        let country = getCountryCode(for: location)
        
        switch country {
        case "US":
            return Authority(
                name: "Department of Transportation",
                department: "Road Maintenance Division",
                phone: "1-800-ASK-DOT",
                email: "roaddefects@dot.gov",
                website: "https://www.transportation.gov",
                address: "1200 New Jersey Ave SE, Washington, DC 20590",
                jurisdiction: "United States"
            )
        case "UK":
            return Authority(
                name: "Highways England",
                department: "Road Maintenance",
                phone: "0300 123 5000",
                email: "info@highwaysengland.co.uk",
                website: "https://highwaysengland.co.uk",
                address: "Bridge House, 1 Walnut Tree Close, Guildford, GU1 4LZ",
                jurisdiction: "United Kingdom"
            )
        case "CA":
            return Authority(
                name: "Transport Canada",
                department: "Road Infrastructure",
                phone: "1-800-387-4999",
                email: "info@tc.gc.ca",
                website: "https://www.tc.gc.ca",
                address: "330 Sparks Street, Ottawa, ON K1A 0N5",
                jurisdiction: "Canada"
            )
        case "AU":
            return Authority(
                name: "Department of Infrastructure",
                department: "Road Maintenance",
                phone: "02 6274 7111",
                email: "info@infrastructure.gov.au",
                website: "https://www.infrastructure.gov.au",
                address: "GPO Box 594, Canberra ACT 2601",
                jurisdiction: "Australia"
            )
        case "TR": // Turkey
            return Authority(
                name: "Karayolları Genel Müdürlüğü",
                department: "Yol Bakım Dairesi",
                phone: "0312 203 10 00",
                email: "iletisim@kgm.gov.tr",
                website: "https://www.kgm.gov.tr",
                address: "İnönü Bulvarı No:14 06100 Çankaya/Ankara",
                jurisdiction: "Türkiye"
            )
        case "DE": // Germany
            return Authority(
                name: "Autobahn GmbH des Bundes",
                department: "Straßenerhaltung",
                phone: "+49 30 640967211",
                email: "kontakt@autobahn.de",
                website: "https://www.autobahn.de",
                address: "Heidestraße 15, 10557 Berlin",
                jurisdiction: "Deutschland"
            )
        case "FR": // France
            return Authority(
                name: "Direction des Routes d'Île-de-France",
                department: "Entretien des Routes",
                phone: "+33 1 46 76 87 00",
                email: "contact-usagers.dirif.drieat-if@developpement-durable.gouv.fr",
                website: "https://www.dir.ile-de-france.developpement-durable.gouv.fr",
                address: "15/17 rue Olof Palme, 94046 Créteil Cedex, France",
                jurisdiction: "France"
            )
        case "ES": // Spain
            return Authority(
                name: "Dirección General de Tráfico",
                department: "Mantenimiento de Carreteras",
                phone: "+34 902 887 060",
                email: "protecciondedatos@dgt.es",
                website: "https://www.dgt.es",
                address: "Calle Josefa Valcárcel, 28, 28071 Madrid, España",
                jurisdiction: "España"
            )
        case "IT": // Italy
            return Authority(
                name: "ANAS S.p.A.",
                department: "Manutenzione Strade",
                phone: "+39 800 841 148",
                email: "servizioclienti@stradeanas.it",
                website: "https://www.stradeanas.it",
                address: "Via A. Bergamini, 50, 00159 Rome, Italy",
                jurisdiction: "Italia"
            )
        case "NL": // Netherlands
            return Authority(
                name: "Rijkswaterstaat",
                department: "Wegonderhoud",
                phone: "+31 70 351 72 45",
                email: "info@rws.nl",
                website: "https://www.rijkswaterstaat.nl",
                address: "Rijnstraat 8, 2515 XP Den Haag, Netherlands",
                jurisdiction: "Nederland"
            )
        case "BE": // Belgium
            return Authority(
                name: "Wegen en Verkeer",
                department: "Wegonderhoud",
                phone: "+32 2 553 86 11",
                email: "info@wegenenverkeer.be",
                website: "https://www.wegenenverkeer.be",
                address: "Havenlaan 86C, 1000 Brussel, Belgium",
                jurisdiction: "België"
            )
        case "PL": // Poland
            return Authority(
                name: "Generalna Dyrekcja Dróg Krajowych i Autostrad",
                department: "Utrzymanie Dróg",
                phone: "+48 22 555 55 55",
                email: "kontakt@gddkia.gov.pl",
                website: "https://www.gddkia.gov.pl",
                address: "ul. Żelazna 59, 00-848 Warszawa, Poland",
                jurisdiction: "Polska"
            )
        case "PT": // Portugal
            return Authority(
                name: "Infraestruturas de Portugal",
                department: "Manutenção de Estradas",
                phone: "+351 707 200 200",
                email: "info@infraestruturasdeportugal.pt",
                website: "https://www.infraestruturasdeportugal.pt",
                address: "Avenida de Berlim, 3, 1800-031 Lisboa, Portugal",
                jurisdiction: "Portugal"
            )
        case "GR": // Greece
            return Authority(
                name: "Ελληνική Δημοκρατία - Υπουργείο Υποδομών και Μεταφορών",
                department: "Συντήρηση Δρόμων",
                phone: "+30 210 650 8000",
                email: "info@yme.gov.gr",
                website: "https://www.yme.gov.gr",
                address: "Acharnon 393-395, 111 43 Athens, Greece",
                jurisdiction: "Ελλάδα"
            )
        case "CZ": // Czech Republic
            return Authority(
                name: "Ředitelství silnic a dálnic",
                department: "Údržba Silnic",
                phone: "+420 954 234 567",
                email: "info@rsd.cz",
                website: "https://www.rsd.cz",
                address: "Lihovarská 12, 190 00 Praha 9, Czech Republic",
                jurisdiction: "Česká republika"
            )
        case "RO": // Romania
            return Authority(
                name: "Compania Națională de Administrare a Infrastructurii Rutiere",
                department: "Întreținere Drumuri",
                phone: "+40 21 319 60 89",
                email: "office@cnair.ro",
                website: "https://www.cnair.ro",
                address: "Bd. Unirii nr. 1, București, Romania",
                jurisdiction: "România"
            )
        case "HU": // Hungary
            return Authority(
                name: "Magyar Közút Nonprofit Zrt.",
                department: "Útfenntartás",
                phone: "+36 1 459 7000",
                email: "info@kozut.hu",
                website: "https://www.kozut.hu",
                address: "H-1138 Budapest, Váci út 185-189, Hungary",
                jurisdiction: "Magyarország"
            )
        case "SE": // Sweden
            return Authority(
                name: "Trafikverket",
                department: "Vägunderhåll",
                phone: "+46 771 503 503",
                email: "info@trafikverket.se",
                website: "https://www.trafikverket.se",
                address: "Roda Vagen 1, 781 89 Borlange, Sweden",
                jurisdiction: "Sverige"
            )
        case "NO": // Norway
            return Authority(
                name: "Statens vegvesen",
                department: "Vegvedlikehold",
                phone: "+47 22 07 30 00",
                email: "post@vegvesen.no",
                website: "https://www.vegvesen.no",
                address: "Hoffsveien 27, 0275 Oslo, Norway",
                jurisdiction: "Norge"
            )
        case "DK": // Denmark
            return Authority(
                name: "Vejdirektoratet",
                department: "Vejvedligeholdelse",
                phone: "+45 72 44 33 00",
                email: "vejdirektoratet@vd.dk",
                website: "https://www.vejdirektoratet.dk",
                address: "Niels Juels Gade 13, 1059 København K, Denmark",
                jurisdiction: "Danmark"
            )
        case "FI": // Finland
            return Authority(
                name: "Tiehallinto",
                department: "Tien ylläpito",
                phone: "+358 29 434 2000",
                email: "tiehallinto@tiehallinto.fi",
                website: "https://www.tiehallinto.fi",
                address: "Opastinsilta 12 A, 00520 Helsinki, Finland",
                jurisdiction: "Suomi"
            )
        case "AT": // Austria
            return Authority(
                name: "ASFINAG",
                department: "Straßenerhaltung",
                phone: "+43 59138 0",
                email: "info@asfinag.at",
                website: "https://www.asfinag.at",
                address: "Rennweg 5-7, 1030 Wien, Austria",
                jurisdiction: "Österreich"
            )
        case "CH": // Switzerland
            return Authority(
                name: "Bundesamt für Strassen ASTRA",
                department: "Strassenerhaltung",
                phone: "+41 58 464 14 11",
                email: "info@astra.admin.ch",
                website: "https://www.astra.admin.ch",
                address: "Mühlestrasse 2, 3063 Ittigen, Switzerland",
                jurisdiction: "Schweiz"
            )
        case "IE": // Ireland
            return Authority(
                name: "Transport Infrastructure Ireland",
                department: "Road Maintenance",
                phone: "+353 1 646 3366",
                email: "info@tii.ie",
                website: "https://www.tii.ie",
                address: "Parkgate Business Centre, Parkgate Street, Dublin 8, Ireland",
                jurisdiction: "Éire"
            )
        default:
            return Authority(
                name: "Local Road Authority",
                department: "Road Maintenance Department",
                phone: "Check local directory",
                email: nil,
                website: nil,
                address: nil,
                jurisdiction: "Local"
            )
        }
    }
    
    /// Get country code from coordinates (simplified - use proper geocoding in production)
    private static func getCountryCode(for location: DetectionRecord.LocationData) -> String {
        // This is a placeholder - in production, use reverse geocoding with CLGeocoder
        // For now, we use coordinate ranges as a fallback
        
        let lat = location.latitude
        let lon = location.longitude
        
        // Turkey: Latitude ~36-42°N, Longitude ~26-45°E
        if lat >= 36 && lat <= 42 && lon >= 26 && lon <= 45 {
            return "TR"
        }
        
        // Germany: Latitude ~47-55°N, Longitude ~6-15°E
        if lat >= 47 && lat <= 55 && lon >= 6 && lon <= 15 {
            return "DE"
        }
        
        // France: Latitude ~42-51°N, Longitude ~-5-8°E
        if lat >= 42 && lat <= 51 && lon >= -5 && lon <= 8 {
            return "FR"
        }
        
        // Spain: Latitude ~36-44°N, Longitude ~-10-4°E
        if lat >= 36 && lat <= 44 && lon >= -10 && lon <= 4 {
            return "ES"
        }
        
        // Italy: Latitude ~36-47°N, Longitude ~6-19°E
        if lat >= 36 && lat <= 47 && lon >= 6 && lon <= 19 {
            return "IT"
        }
        
        // Netherlands: Latitude ~50-54°N, Longitude ~3-7°E
        if lat >= 50 && lat <= 54 && lon >= 3 && lon <= 7 {
            return "NL"
        }
        
        // Belgium: Latitude ~49.5-51.5°N, Longitude ~2.5-6.5°E
        if lat >= 49.5 && lat <= 51.5 && lon >= 2.5 && lon <= 6.5 {
            return "BE"
        }
        
        // Poland: Latitude ~49-55°N, Longitude ~14-25°E
        if lat >= 49 && lat <= 55 && lon >= 14 && lon <= 25 {
            return "PL"
        }
        
        // Portugal: Latitude ~37-42°N, Longitude ~-9.5--6°E
        if lat >= 37 && lat <= 42 && lon >= -9.5 && lon <= -6 {
            return "PT"
        }
        
        // Greece: Latitude ~35-42°N, Longitude ~20-30°E
        if lat >= 35 && lat <= 42 && lon >= 20 && lon <= 30 {
            return "GR"
        }
        
        // Czech Republic: Latitude ~48.5-51°N, Longitude ~12-19°E
        if lat >= 48.5 && lat <= 51 && lon >= 12 && lon <= 19 {
            return "CZ"
        }
        
        // Romania: Latitude ~44-48°N, Longitude ~20-30°E
        if lat >= 44 && lat <= 48 && lon >= 20 && lon <= 30 {
            return "RO"
        }
        
        // Hungary: Latitude ~46-49°N, Longitude ~16-23°E
        if lat >= 46 && lat <= 49 && lon >= 16 && lon <= 23 {
            return "HU"
        }
        
        // Sweden: Latitude ~55-69°N, Longitude ~11-24°E
        if lat >= 55 && lat <= 69 && lon >= 11 && lon <= 24 {
            return "SE"
        }
        
        // Norway: Latitude ~58-71°N, Longitude ~4-31°E
        if lat >= 58 && lat <= 71 && lon >= 4 && lon <= 31 {
            return "NO"
        }
        
        // Denmark: Latitude ~54.5-58°N, Longitude ~8-13°E
        if lat >= 54.5 && lat <= 58 && lon >= 8 && lon <= 13 {
            return "DK"
        }
        
        // Finland: Latitude ~60-70°N, Longitude ~20-32°E
        if lat >= 60 && lat <= 70 && lon >= 20 && lon <= 32 {
            return "FI"
        }
        
        // Austria: Latitude ~46-49°N, Longitude ~9-17°E
        if lat >= 46 && lat <= 49 && lon >= 9 && lon <= 17 {
            return "AT"
        }
        
        // Switzerland: Latitude ~46-48°N, Longitude ~6-10°E
        if lat >= 46 && lat <= 48 && lon >= 6 && lon <= 10 {
            return "CH"
        }
        
        // Ireland: Latitude ~51-55°N, Longitude ~-11--5°E
        if lat >= 51 && lat <= 55 && lon >= -11 && lon <= -5 {
            return "IE"
        }
        
        // United Kingdom: Latitude ~50-61°N, Longitude ~-8-2°E
        if lat >= 50 && lat <= 61 && lon >= -8 && lon <= 2 {
            return "UK"
        }
        
        // Note: For production, use CLGeocoder.reverseGeocodeLocation to get actual country
        
        return "US" // Default fallback
    }
    
    /// Get formatted contact information
    static func getContactInfo(for authority: Authority) -> String {
        var info = "Contact Information:\n\n"
        info += "Organization: \(authority.name)\n"
        info += "Department: \(authority.department)\n"
        info += "Phone: \(authority.phone)\n"
        
        if let email = authority.email {
            info += "Email: \(email)\n"
        }
        if let website = authority.website {
            info += "Website: \(website)\n"
        }
        if let address = authority.address {
            info += "Address: \(address)\n"
        }
        
        return info
    }
    
    /// Create report message for sharing
    static func createReportMessage(
        for record: DetectionRecord,
        authority: Authority
    ) -> String {
        var message = "Road Defect Report\n\n"
        
        message += "Date: \(formatDate(record.date))\n"
        message += "Defects Found: \(record.detections.count)\n"
        
        if let location = record.location {
            message += "Location: \(location.latitude), \(location.longitude)\n"
            if let address = location.address {
                message += "Address: \(address)\n"
            }
        }
        
        message += "\nDefect Details:\n"
        for (index, detection) in record.detections.enumerated() {
            message += "\(index + 1). \(detection.className) - \(Int(detection.confidence * 100))% confidence\n"
        }
        
        message += "\n\(getContactInfo(for: authority))"
        
        return message
    }
    
    private static func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}
