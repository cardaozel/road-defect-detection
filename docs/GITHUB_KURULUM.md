# 🚀 GitHub Repository Kurulum Rehberi

## ⚡ Hızlı Başlangıç

### Adım 1: GitHub'da Repository Oluşturma

1. **GitHub'a gidin**: https://github.com/new
2. **Repository adı**: `road-defect-detection` (veya istediğiniz isim)
3. **Açıklama**: "YOLOv8-based Road Defect Detection System with iOS Mobile App - Thesis Project"
4. **Public veya Private** seçin (önerilen: Private - thesis projesi için)
5. **ÖNEMLİ**: "Initialize with README" işaretlemeyin (zaten README var)
6. **"Create repository"** tıklayın

### Adım 2: Git Repository Hazırlama

Terminal'de şu komutları çalıştırın:

```bash
cd /Users/ardaozel/road_defect_detection

# İlk commit için dosyaları hazırla
git add .

# İlk commit
git commit -m "Initial commit: Road Defect Detection System with YOLOv8 and iOS App"
```

### Adım 3: GitHub Repository'ye Bağlama

GitHub'da repository oluşturduktan sonra size verilen URL'i kullanın:

```bash
# GitHub kullanıcı adınızı öğrenin (veya GitHub profil sayfanızdan alın)
# Örnek: https://github.com/your-username/road-defect-detection

# Remote ekleyin (YOUR_USERNAME yerine GitHub kullanıcı adınızı yazın):
git remote add origin https://github.com/YOUR_USERNAME/road-defect-detection.git

# Veya SSH kullanıyorsanız:
# git remote add origin git@github.com:YOUR_USERNAME/road-defect-detection.git
```

### Adım 4: İlk Push

```bash
# Branch'i main olarak ayarla
git branch -M main

# GitHub'a push et
git push -u origin main
```

GitHub kullanıcı adı ve şifre (veya Personal Access Token) isteyecek. Giriş yapın.

---

## 📝 Düzenli Güncellemeler İçin

### Yöntem 1: Manuel Komutlar

```bash
cd /Users/ardaozel/road_defect_detection

# Değişiklikleri kontrol et
git status

# Değişiklikleri ekle
git add .

# Commit yap
git commit -m "Update: Training progress, iOS improvements, etc."

# GitHub'a push et
git push
```

### Yöntem 2: Otomatik Script (Önerilen)

Hazırladığım script'i kullanın:

```bash
cd /Users/ardaozel/road_defect_detection

# Script'i çalıştır
bash scripts/push_to_github.sh

# Veya direkt commit mesajı ile:
bash scripts/push_to_github.sh "Update: Training epoch 1 completed"
```

### Yöntem 3: Tek Satır Komut

```bash
cd /Users/ardaozel/road_defect_detection && git add . && git commit -m "Update: your message here" && git push
```

---

## 📋 .gitignore Dosyası

Proje `.gitignore` dosyası ile şu dosyaları **hariç tutar** (yüklenmez):

### ❌ Yüklenmeyecek Dosyalar:
- ✅ Model dosyaları (`.pt`, `.onnx`, `.mlmodel`) - Çok büyük
- ✅ Training results (`results/`, `runs/`) - Çok büyük
- ✅ Training logs (`training_log.txt`) - Gereksiz
- ✅ Dataset dosyaları (`data/raw/`, `data/yolo/images/`) - Çok büyük
- ✅ Virtual environment (`.venv/`) - Gereksiz
- ✅ IDE dosyaları (`.vscode/`, `.idea/`)
- ✅ OS dosyaları (`.DS_Store`)

### ✅ Yüklenecek Dosyalar:
- ✅ Tüm Python scriptleri (`scripts/`)
- ✅ Config dosyaları (`configs/`)
- ✅ iOS uygulama kodu (`iOS/`)
- ✅ Documentation (`.md` dosyaları)
- ✅ README ve diğer dokümantasyon
- ✅ Requirements (`requirements.txt` varsa)
- ✅ Dataset config (`data/yolo/rdd2022.yaml`)

---

## 🔐 GitHub Authentication

### HTTPS ile (Şifre/Token):
```bash
git remote add origin https://github.com/YOUR_USERNAME/road-defect-detection.git
```
Push sırasında GitHub kullanıcı adı ve Personal Access Token isteyecek.

### SSH ile (Önerilen):
```bash
# SSH key varsa:
git remote add origin git@github.com:YOUR_USERNAME/road-defect-detection.git
```

SSH key yoksa:
1. https://docs.github.com/en/authentication/connecting-to-github-with-ssh
2. Veya HTTPS kullanın (daha kolay)

---

## 📊 Repository İçeriği Özeti

GitHub'da göreceğiniz dosyalar:

```
road-defect-detection/
├── README.md                    # Proje açıklaması
├── requirements.txt             # Python bağımlılıkları
├── .gitignore                   # Git ignore kuralları
├── scripts/                     # Python scriptleri
│   ├── train_yolov8.py
│   ├── prepare_rdd2022.py
│   ├── evaluate_rdd2022.py
│   ├── visualize_detections.py
│   └── ...
├── configs/                     # Training config dosyaları
│   ├── training.yaml
│   └── training_phase1_mps_safe.yaml
├── iOS/                         # iOS uygulama kodu
│   ├── RoadDefectDetectorApp.swift
│   ├── CameraView.swift
│   ├── DetectionEngine.swift
│   ├── ResultsView.swift
│   ├── HistoryView.swift
│   └── ...
└── *.md                         # Documentation dosyaları
```

---

## 🔄 Düzenli Güncelleme Önerileri

### Haftalık veya Önemli Milestone'larda:

```bash
# Örnek commit mesajları:
git commit -m "Update: Training epoch 1 completed, mAP improved to X%"
git commit -m "Update: iOS app - Added GPS location and reporting features"
git commit -m "Update: Added European countries to reporting service"
git commit -m "Update: Training progress - Epoch 50/200 completed"
git commit -m "Update: Final model trained, mAP >60% achieved"
```

### Commit Mesajı Önerileri:
- ✅ Açıklayıcı olun: "Update: what changed"
- ✅ Önemli değişiklikleri belirtin
- ✅ Training progress varsa ekleyin
- ✅ Feature eklemelerini belirtin

---

## ❓ Sık Sorulan Sorular

### Q: Model dosyaları yüklenmeyecek mi?
A: Hayır, `.gitignore` dosyası `.pt`, `.onnx` gibi dosyaları hariç tutar. Bunlar çok büyük (100MB+).

### Q: Training sırasında commit yapabilir miyim?
A: Evet! Training arka planda çalışır, commit yapmak training'i etkilemez.

### Q: Commit mesajı zorunlu mu?
A: Evet, her commit için anlamlı bir mesaj yazın.

### Q: Hangi sıklıkla push yapmalıyım?
A: Önerilen: 
- Her önemli değişiklikten sonra
- Training milestone'larında (epoch 1, 50, 100, 200)
- Yeni feature eklendiğinde
- Bug fix'lerinde

### Q: Eğer hata yaparsam?
A: Git geri alma komutları:
```bash
# Son commit'i geri al (dosyalar değişmeden)
git reset --soft HEAD~1

# Son commit'i tamamen geri al
git reset --hard HEAD~1
```

---

## 🎯 İlk Kurulum Komutları (Özet)

```bash
cd /Users/ardaozel/road_defect_detection

# 1. Git initialize (zaten yapıldı)
git init

# 2. İlk commit
git add .
git commit -m "Initial commit: Road Defect Detection System"

# 3. GitHub'da repository oluşturun (web'de)
# https://github.com/new

# 4. Remote ekleyin (YOUR_USERNAME değiştirin)
git remote add origin https://github.com/YOUR_USERNAME/road-defect-detection.git

# 5. Push edin
git branch -M main
git push -u origin main
```

---

## ✅ Başarı Kontrolü

GitHub'a başarıyla yüklendiğini kontrol etmek için:

1. GitHub'da repository'nizi açın
2. Dosyaların göründüğünü kontrol edin
3. README.md dosyasının okunduğunu kontrol edin
4. `scripts/`, `configs/`, `iOS/` klasörlerinin olduğunu kontrol edin

Başarılar! 🎉
