# Thesis Information - Official Details

## Thesis Title
**On-Device Road Damage Detection for Municipal Reporting**

## Problem Statement
Timely road maintenance is hindered by manual inspections that miss small but safety-critical defects (e.g., cracks, potholes) under varying lighting, weather, and camera angles. There is a need for a lightweight, reliable object detector that can run on commodity smartphones to localize common road surface defects in real time.

## Goal / Aim
Design, train, and deploy a compact object detection model (e.g., YOLOv8-nano / SSD-MobileNet).

**Note**: YOLOv8s (Small) was selected instead of YOLOv8-nano for better accuracy while maintaining mobile compatibility.

## Dataset
**Road Damage Dataset 2022 (RDD2022)**
- Publicly available for research use
- Bounding-box annotations for multiple defect categories
- Defect types: longitudinal/transverse cracks, potholes, and other road surface defects
- Collected across several regions
- Training images: 19,089
- Validation images: 3,579
- 6 defect classes: D00, D01, D10, D11, D20, D40

## Student Information
- **Name**: Civan Arda Özel
- **Primary Supervisor**: Prof. Dr. Iftikhar Ahmed
- **Secondary Supervisor**: Prof. Dr. Raja Hashim Ali
- **Start Date**: December 2025
- **Submission Date**: January 2026

## Key Focus Areas
1. **On-device processing**: Model runs on commodity smartphones (no cloud dependency)
2. **Real-time detection**: Immediate feedback for field workers
3. **Municipal reporting**: Integration with reporting systems for maintenance workflows
4. **Lightweight model**: Compact architecture suitable for mobile deployment
5. **Reliable detection**: Consistent performance under varying conditions (lighting, weather, angles)

---

**This information should be used consistently across Phase 3 (Presentation) and Phase 4 (Thesis Documentation).**

