# 🚀 GitHub Repository Kurulumu

## Adım 1: Git Repository Kontrolü

Önce mevcut durumu kontrol edelim:

```bash
cd /Users/ardaozel/road_defect_detection
git status
git remote -v
```

## Adım 2: GitHub Repository Oluşturma

1. **GitHub'a gidin**: https://github.com/new
2. **Repository adı**: `road-defect-detection` (veya istediğiniz bir isim)
3. **Açıklama**: "YOLOv8-based Road Defect Detection System with iOS Mobile App"
4. **Public veya Private** seçin
5. **README, .gitignore, license eklemeyin** (zaten var)
6. **"Create repository"** tıklayın

## Adım 3: GitHub Repository'ye Bağlama

GitHub'da repository oluşturduktan sonra, size verilen URL'i kullanın:

```bash
# Eğer git repository yoksa:
git init

# Remote ekleyin (YOUR_USERNAME yerine GitHub kullanıcı adınızı yazın):
git remote add origin https://github.com/YOUR_USERNAME/road-defect-detection.git

# Veya SSH kullanıyorsanız:
# git remote add origin git@github.com:YOUR_USERNAME/road-defect-detection.git
```

## Adım 4: İlk Commit ve Push

```bash
# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Road Defect Detection System with YOLOv8 and iOS App"

# Main branch'e push et
git branch -M main
git push -u origin main
```

## Adım 5: Düzenli Güncellemeler

Düzenli olarak güncellemeleri yüklemek için:

```bash
# Değişiklikleri kontrol et
git status

# Değişiklikleri ekle
git add .

# Commit yap (anlamlı bir mesaj ile)
git commit -m "Update: Description of changes"

# GitHub'a push et
git push
```

## Otomatik Güncelleme Scripti

Kolaylık için bir script oluşturalım:

```bash
#!/bin/bash
# scripts/push_to_github.sh

cd "$(dirname "$0")/.."

echo "📊 Checking for changes..."
git status

read -p "Do you want to commit and push? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📝 Adding changes..."
    git add .
    
    read -p "Enter commit message: " message
    git commit -m "$message"
    
    echo "🚀 Pushing to GitHub..."
    git push
    
    echo "✅ Done! Changes pushed to GitHub."
else
    echo "❌ Cancelled."
fi
```

## .gitignore Dosyası

Projenin `.gitignore` dosyası şunları hariç tutar:
- Python virtual environment (`.venv/`)
- Training results (`results/`)
- Model weights (`weights/`, `*.pt`, `*.onnx`, etc.)
- Training logs (`training_log.txt`)
- Dataset files (`data/raw/`, `data/yolo/`)
- IDE files (`.idea/`, `.vscode/`)
- OS files (`.DS_Store`)

Bu sayede büyük dosyalar ve geçici dosyalar GitHub'a yüklenmez.

## Önemli Notlar

1. **Model dosyaları (.pt, .onnx) yüklenmez** - Bunlar çok büyük
2. **Training logs yüklenmez** - Gereksiz
3. **Dataset dosyaları yüklenmez** - Çok büyük, başka yerden indirilir
4. **Sadece kod ve config dosyaları yüklenir**

## GitHub Repository İçeriği

Yüklenecek dosyalar:
- ✅ Tüm Python scriptleri (`scripts/`)
- ✅ Config dosyaları (`configs/`)
- ✅ iOS uygulama kodu (`iOS/`)
- ✅ Documentation (`.md` dosyaları)
- ✅ Requirements (`requirements.txt`)
- ✅ README
- ✅ .gitignore

Yüklenmeyecek dosyalar:
- ❌ Model weights (`.pt`, `.onnx`)
- ❌ Training results (`results/`)
- ❌ Dataset (`data/raw/`, `data/yolo/`)
- ❌ Virtual environment (`.venv/`)
- ❌ Training logs

## Hızlı Komutlar

```bash
# Status kontrol
git status

# Değişiklikleri ekle ve commit
git add . && git commit -m "Update message"

# Push
git push

# Tümü bir arada
git add . && git commit -m "Update: your message" && git push
```
