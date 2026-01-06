# Email to Professor - Thesis Progress Update

**Subject:** Thesis Progress Update: Research Questions, Training Status, and Model Selection

---

**To:** Prof. Dr. Iftikhar Ahmed  
**CC:** Prof. Dr. Raja Hashim Ali  
**From:** Civan Arda Özel  
**Date:** [Current Date]

---

Dear Prof. Dr. Ahmed,

I hope this email finds you well. I am writing to provide an update on my thesis progress for "On-Device Road Damage Detection for Municipal Reporting" and to address a few important points regarding the research questions, training progress, and model selection.

## Research Questions

I have formulated three research questions that align with the thesis objectives:

**Research Question 1 (RQ1):** What is the detection accuracy and performance of a YOLOv8-based model when trained on the RDD2022 dataset for road defect detection?

This question investigates the achievable mAP@0.5, mAP@0.5:0.95, precision, and recall metrics, as well as the effectiveness of the YOLOv8 architecture for road defect detection compared to baseline methods.

**Research Question 2 (RQ2):** Can a YOLOv8-based road defect detection model be successfully deployed on iOS mobile devices using CoreML while maintaining real-time inference performance?

This question examines the feasibility of CoreML conversion, real-time inference capabilities (<50ms per image), model size requirements, and accuracy preservation after mobile optimization.

**Research Question 3 (RQ3):** What are the usability characteristics and practical effectiveness of a mobile application for real-time road defect detection in field conditions?

This question evaluates the user interface design, real-time detection effectiveness, location tagging and reporting capabilities, and overall practical applicability for field workers.

## Training Progress

The model training is progressing well:

- **Total epochs completed:** 174 out of 200 (87% complete)
- **Best performance achieved:**
  - **mAP@0.5: 49.19%** (achieved at Epoch 119)
  - **Precision: 60.82%** (achieved at Epoch 120)
  - **Recall: 47.22%**
  - **mAP@0.5:0.95: 20.58%**

The model shows consistent learning throughout training, with a 207% improvement from the initial 16.01% mAP@0.5 at Epoch 1 to the current best of 49.19%. Training is expected to complete all 200 epochs, and the model performance exceeds baseline methods (typically 30-45% mAP@0.5) while remaining suitable for mobile deployment.

## Model Selection: YOLOv8s vs YOLOv8-nano

I would like to address the model selection decision. While the initial thesis goal mentioned YOLOv8-nano as an example of a compact model, I selected **YOLOv8s (Small variant)** after initial experiments. This decision was made for the following reasons:

1. **Better Accuracy:** YOLOv8s (11M parameters) achieves significantly better detection accuracy (49.19% mAP@0.5) compared to what YOLOv8-nano (3M parameters) would typically achieve (approximately 35-40% mAP@0.5 based on literature).

2. **Still Mobile-Compatible:** YOLOv8s remains a compact model suitable for mobile deployment:
   - Model size: ~43MB in CoreML format (acceptable for mobile)
   - Real-time inference: <50ms on iPhone 12+ (meets requirement)
   - On-device processing: Successfully deployed using CoreML

3. **Meets Requirements:** The goal specified "a compact object detection model" - YOLOv8s fulfills this requirement while providing better performance for practical deployment.

4. **Justified Trade-off:** The slight increase in model size (from ~6MB to ~43MB) is justified by the substantial improvement in detection accuracy, which is critical for identifying small but safety-critical road defects as stated in the problem statement.

I believe this decision aligns with the thesis objective of creating a reliable, practical solution for road defect detection while maintaining mobile compatibility. I will document this design decision and rationale in the methodology chapter of the thesis.

## Current Status

- ✅ **Phase 1 (Training):** 174/200 epochs completed, achieving 49.19% mAP@0.5
- ✅ **Phase 2 (iOS App):** Complete iOS application with CoreML integration, real-time detection, GPS tagging, and municipal reporting features
- ✅ **Phase 3 (Presentation):** Presentation slides prepared with all research questions and results
- 🔄 **Phase 4 (Thesis Documentation):** Ready to begin writing

I would be happy to discuss any of these points further or make adjustments based on your feedback. Please let me know if you have any questions or concerns.

Thank you for your guidance and support.

Best regards,  
Civan Arda Özel

---

**Thesis Title:** On-Device Road Damage Detection for Municipal Reporting  
**Supervisors:** Prof. Dr. Iftikhar Ahmed (Primary), Prof. Dr. Raja Hashim Ali (Secondary)

