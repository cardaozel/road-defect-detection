# 🔗 Cursor + GitHub Entegrasyonu

## Cursor'un Git Entegrasyonunu Kullanma

Cursor uygulaması GitHub ile entegre olduğu için, doğrudan Cursor arayüzünden GitHub'a push yapabilirsiniz.

## Yöntem 1: Cursor UI'dan (Önerilen)

1. **Source Control panelini açın** (Cursor'da sol taraftaki Git ikonu veya `Cmd+Shift+G`)
2. **"Publish to GitHub"** butonuna tıklayın
3. Cursor otomatik olarak:
   - GitHub'da repository oluşturur
   - Remote'u ayarlar
   - İlk commit'i yapar
   - Push eder

## Yöntem 2: Terminal'den (Manuel)

Eğer terminal kullanmak isterseniz:

```bash
cd /Users/ardaozel/road_defect_detection

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Road Defect Detection System"

# GitHub'da repository oluştur (web'de veya GitHub CLI ile)
# Sonra remote ekle:
git remote add origin https://github.com/YOUR_USERNAME/road-defect-detection.git

# Push et
git push -u origin main
```

## Yöntem 3: GitHub CLI (gh) ile

Eğer GitHub CLI yüklüyse:

```bash
cd /Users/ardaozel/road_defect_detection

# GitHub'da repository oluştur ve push et
gh repo create road-defect-detection --private --source=. --remote=origin --push
```

## Cursor'da Düzenli Güncellemeler

### Source Control Panelinden:

1. Değişiklikleri görmek için Source Control panelini açın
2. Değişen dosyaların yanındaki `+` işaretine tıklayarak stage edin
3. Commit mesajı yazın
4. `✓ Commit` butonuna tıklayın
5. `↑ Push` butonuna tıklayın (veya `Cmd+Shift+P` → "Git: Push")

### Terminal'den:

```bash
# Kolay script kullanarak
bash scripts/push_to_github.sh

# Veya manuel
git add .
git commit -m "Update: your message"
git push
```

## GitHub Kimlik Bilgileri

Cursor zaten GitHub ile bağlı olduğu için, genellikle ekstra kimlik bilgisi girmenize gerek yok. Eğer gerekirse:

1. Cursor Settings → Accounts → GitHub
2. GitHub hesabınızı bağlayın

## Notlar

- ✅ Cursor'un Git entegrasyonu GitHub authentication'ı otomatik yönetir
- ✅ `.gitignore` dosyası büyük dosyaları (models, results, dataset) hariç tutar
- ✅ Sadece kod ve dokümantasyon yüklenecek
- ✅ Training sırasında da commit/push yapabilirsiniz

## Önerilen Workflow

1. **Her önemli değişiklikten sonra:**
   - Source Control panelinden commit yapın
   - Push edin

2. **Training milestone'larında:**
   - Epoch tamamlandığında
   - Önemli metrikler iyileştiğinde
   - Yeni feature eklendiğinde

3. **Günlük/Haftalık:**
   - Düzenli commit yapın
   - Training progress'i dokümante edin
