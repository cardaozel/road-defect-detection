# Hocanın Checklist Durumu - Mevcut Dosyalara Göre

List of Abbreviations **TAMAM** (sen söyledin).

---

## ✅ Çözülmüş / Mevcut Dosyalarda Uyumlu

| # | Madde | Durum | Kanıt |
|---|-------|-------|-------|
| 5-6 | List of Abbreviations | ✅ Tamam | `PHASE4_LIST_OF_ABBREVIATIONS.md` – 2 sütunlu, alfabetik |
| 8 | Ch1: RQ ve Objectives | ✅ Var | `PHASE4_CHAPTER1` satır 110-116: "Research questions" bölümü, RQ1-RQ3 |
| 14 | RQ traceability | ✅ Var | Ch4: `tab:rq-traceability` tablosu; Ch7: RQ→method→result paragrafı |
| 7 | Chapter-content separation | ✅ Tamam | Result figürleri sadece Ch6'da; Ch5'te referans verildi |
| 10 | Captions | ✅ Tamam | "Enter Caption", "axonomy" düzeltildi |
| 11 | Acronyms first use | ✅ Tamam | Glossary sıralaması doğru |
| 13 | Code repo link | ✅ Tamam | Dissemination'da URL eklendi |
| 15 | Contributions | ✅ Var | Ch1 satır 118-126: "Contributions" bölümü, 4 maddelik liste |
| 16 | Baselines | ✅ Tamam | Kapsam dışı veya açıklandı |
| 17 | Hyperparameter protocol | ✅ Var | Ch5: "Hyperparameter tuning protocol" – search space, budget, validation-only, no test leakage |
| 18 | Feature leakage | ✅ Tamam | Ch5.5.3: "avoids test leakage" – sadece train/validation kullanımı açıklandı |

---

## ✅ Doğrulandı (Figure refs + Orphan refs)

| # | Madde | Durum | Kanıt |
|---|-------|-------|-------|
| 9 | Figure references | ✅ Tamam | **Ch3:** fig:ch3-taxonomy, fig:ch3-focus-counts, fig:ch3-year-counts, fig:ch3-focus-year – hepsi intro’da cite edildi. **Ch6:** fig:training-curves, fig:pr-curve, fig:confusion-matrix, fig:val-detections – hepsi metinde cite edildi. **Ch1, Ch2, Ch4, Ch5:** tüm fig/tab ref’leri tanımlı ve kullanılıyor. |
| 12 | Orphan refs | ✅ Tamam | 36 cite key kullanılıyor; hepsi `references.bib`’de var. 36 bib entry var; hepsi en az bir kez cite edilmiş. Orphan yok. |

---

## ❌ Dokümanlarda Çözülmemiş (Overleaf / LaTeX)

| # | Madde | Ne Yapılmalı |
|---|-------|--------------|
| 1 | AI-generated text ≤20% | Manuel kontrol / yeniden yazma |
| 2 | Page numbering | Overleaf'te ayar: kapak yok, ön sayfalar Roma, bölümler Arap |
| 3 | Blank pages | Gereksiz boş sayfaları sil |
| 4 | LaTeX/Word hataları | "Enter Caption", "axonomy", template sayfası – Overleaf'te düzelt |

---

## Özet

- **Çözülmüş:** 11 madde (List of Abbr, Ch1 RQ, Ch1 Contributions, RQ traceability, Hyperparameter protocol, Baselines, Feature leakage, Ch5–content separation, Captions, Acronyms first use, Code repo link)
- **Kısmen / Overleaf kontrolü:** 2 madde (Figure references, Orphan refs)
- **Overleaf/LaTeX'te yapılacak:** 4 madde (page numbering, blank pages, LaTeX hataları)
- **İçerik/scope kararı:** 1 madde (AI text)
