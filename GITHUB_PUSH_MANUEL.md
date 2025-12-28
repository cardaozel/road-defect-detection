# 🚀 GitHub'a Manuel Push Rehberi

## Terminal'den GitHub'a Push

### Adım 1: GitHub'da Repository Oluşturun

1. **GitHub'a gidin**: https://github.com/new
2. **Repository adı**: `road-defect-detection`
3. **Açıklama**: "YOLOv8-based Road Defect Detection System with iOS Mobile App"
4. **Private** seçin (önerilen)
5. **⚠️ ÖNEMLİ**: "Initialize with README", ".gitignore", "license" işaretlemeyin
6. **"Create repository"** tıklayın

### Adım 2: Repository URL'ini Kopyalayın

GitHub'da repository oluşturduktan sonra size şöyle bir URL gösterilecek:
```
https://github.com/cardaozel/road-defect-detection.git
```

### Adım 3: Terminal'den Bağlayın ve Push Edin

Terminal'de şu komutları çalıştırın:

```bash
cd /Users/ardaozel/road_defect_detection

# Remote ekleyin (cardaozel zaten kullanıcı adınız)
git remote add origin https://github.com/cardaozel/road-defect-detection.git

# Branch'i main olarak ayarlayın
git branch -M main

# Push edin
git push -u origin main
```

GitHub kullanıcı adı ve şifre (veya Personal Access Token) isteyecek.

---

## Personal Access Token Kullanma

Eğer şifre çalışmazsa, Personal Access Token kullanmanız gerekebilir:

1. **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. **"Generate new token (classic)"** tıklayın
3. **Note**: "Road Defect Detection" yazın
4. **Expiration**: İstediğiniz süreyi seçin
5. **Scopes**: `repo` işaretleyin
6. **"Generate token"** tıklayın
7. **Token'ı kopyalayın** (bir daha gösterilmeyecek!)

Push yaparken:
- **Username**: `cardaozel`
- **Password**: Token'ı yapıştırın

---

## Alternatif: SSH Kullanma

SSH key'iniz varsa:

```bash
# SSH ile remote ekleyin
git remote add origin git@github.com:cardaozel/road-defect-detection.git

# Push edin
git push -u origin main
```

SSH key yoksa HTTPS kullanın.

---

## Hızlı Komutlar (Özet)

```bash
cd /Users/ardaozel/road_defect_detection
git remote add origin https://github.com/cardaozel/road-defect-detection.git
git branch -M main
git push -u origin main
```

---

## Başarı Kontrolü

GitHub'da repository'nize gidin:
https://github.com/cardaozel/road-defect-detection

Dosyaların göründüğünü kontrol edin!

---

## Düzenli Güncellemeler

Sonraki güncellemeler için:

```bash
cd /Users/ardaozel/road_defect_detection
git add .
git commit -m "Update: your message here"
git push
```

Veya script kullanın:

```bash
bash scripts/push_to_github.sh
```
