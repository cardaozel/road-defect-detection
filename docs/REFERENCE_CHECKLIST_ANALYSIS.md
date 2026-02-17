# Reference Checklist Analysis

## 1. Tezde Kullanılan Referanslar (BibTeX key → Bibliography Eşlemesi)

| BibTeX Key | Bibliography Karşılığı | Doğru? |
|------------|------------------------|--------|
| coreml2023 | [Apple, 2024a] Core ML | ✓ |
| swiftui2022 | [Apple, 2024b] SwiftUI | ✓ |
| edgeml2021 | [Dhar et al., 2021] On-device ML survey | ✓ |
| rdd2022 | [Arya et al., 2022] RDD2022 dataset | ✓ |
| rdd2020_2021 | [Arya et al., 2021] RDD2020 dataset | ✓ |
| yolov8 | [Ultralytics, 2023] YOLOv8 | ✓ |
| smartcitysurvey2021 | [Dong and Li, 2021] Smartphone sensing | ✓ |
| zaidi2021 | [Zaidi et al., 2021] Object detection survey | ✓ |
| terven2023 | [Terven and Cordova-Esparza, 2023] YOLO review | ✓ |
| yolov7_2022 | [Wang et al., 2022] YOLOv7 | ✓ |
| pham2022_yolov7 | [Pham et al., 2022] Road damage + YOLOv7 | ✓ |
| yolov5s_2022 | [Guo et al., 2022] Pavement + YOLOv5s | ✓ |
| yu2024 | [Yu et al., 2024] Road defect survey | ✓ |
| svrrd_2024 | [Ren et al., 2024] Street view dataset | ✓ |

**Sonuç:** Tezde kullanılan 14 benzersiz referansın hepsi bibliography listesinde mevcut ve doğru eşleniyor.

---

## 2. Birbirinden Farklılık (Duplicate / Çakışma Kontrolü)

- **rdd2022** ve **rdd2020_2021**: Farklı makaleler (2022 vs 2021, farklı dataset versiyonları) ✓
- **yolov7_2022** (Wang et al.) ve **pham2022_yolov7** (Pham et al.): Farklı çalışmalar; biri YOLOv7 mimarisi, diğeri yol hasarı tespiti ✓
- **yolov5s_2022** (Guo et al.) ve **yolov7_2022** (Wang et al.): Farklı modeller ✓

**Sonuç:** Çakışma yok; her key benzersiz bir kaynağı temsil ediyor.

---

## 3. Bibliography'de Olup Tezde Kullanılmayan Referanslar

| Bibliography Entry | Açıklama |
|--------------------|----------|
| [American Society of Civil Engineers, 2021] | Roads - tezde cite yok |
| [Apple, 2022] | Neural Engine - tezde cite yok |
| [Apple, 2023] | Core Location - tezde cite yok |
| [ASTM International, 2020] | Pavement surveys - tezde cite yok |
| [Carion et al., 2020] | DETR - tezde cite yok |
| [Cheng et al., 2024] | YOLO-World - tezde cite yok |
| [Ge et al., 2021] | YOLOX - tezde cite yok |
| [Guo et al., 2023] | Pavement transformer - tezde cite yok |
| [Hou et al., 2021] | Pavement monitoring review - tezde cite yok |
| [Liu et al., 2023] | Grounding DINO - tezde cite yok |
| [Lyu et al., 2022] | RTMDet - tezde cite yok |
| [Maeda et al., 2021] | GAN road damage - tezde cite yok |
| [Majidifard et al., 2020] | Pavement dataset - tezde cite yok |
| [Ozel, 2026] | Code repository - tezde cite yok |
| [Tan et al., 2020] | EfficientDet - tezde cite yok |
| [TRIP, 2022] | Transportation funding - tezde cite yok |
| [Wang et al., 2024a] | YOLOv10 - tezde cite yok |
| [Wang et al., 2024b] | YOLOv9 - tezde cite yok |
| [Xiong et al., 2020] | MobileDets - tezde cite yok |
| [Xu et al., 2022] | PP-YOLOE - tezde cite yok |
| [Zhao et al., 2023] | RT-DETR - tezde cite yok |

**Not:** Tezde cite edilmeyen kaynaklar bibliography'de kalabilir (LaTeX genelde sadece cite edilenleri listeler); ancak checklist’e göre “sadece kullanılan referanslar” isteniyorsa bu maddeler çıkarılabilir.

---

## 4. references.bib ile Bibliography Tutarlılığı

| Özellik | Durum |
|---------|-------|
| coreml2023 year | bib: 2024, checklist: Apple 2024a ✓ |
| swiftui2022 year | bib: 2024, checklist: Apple 2024b ✓ |
| Dhar et al. – "Shah, Mohak" vs "Shah, M." | Küçük fark; genelde kabul edilir ✓ |
| smartcitysurvey2021 – Author | bib: Dong, Dapeng and Li, Zili; checklist: Dong, D. and Li, Z. ✓ |

---

## 5. Checklist Uygunluk Özeti

| Kriter | Sonuç |
|--------|-------|
| Kullanılan referanslar bibliography'de var mı? | ✓ Evet (14/14) |
| Referanslar birbirinden farklı mı? | ✓ Evet |
| Duplicate / çakışma var mı? | ✗ Yok |
| BibTeX key'ler doğru eşleniyor mu? | ✓ Evet |

---

## 6. Öneriler

1. **Ozel, 2026 (code repository):** Eğer tezde “reproducible pipeline” veya “repository” referansı veriliyorsa bu cite edilebilir.
2. **Apple, 2023 (Core Location):** GPS/location tabanlı reporting için Dissemination veya metodoloji bölümünde kullanılabilir.
3. **Kullanılmayan referanslar:** Sadece cite edilenleri bırakmak istersen 21 referans listeden çıkarılabilir; ancak LaTeX/BibTeX genelde sadece cite edilenleri otomatik listeler.
