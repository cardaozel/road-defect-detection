# 🚀 Terminal'den GitHub Repository Oluşturma

## Seçenek 1: Web'den (Önerilen - Daha Kolay)

1. https://github.com/new adresine gidin
2. Repository oluşturun
3. Terminal komutlarıyla push edin

**⏱️ Süre: 2-3 dakika**

---

## Seçenek 2: Terminal'den (GitHub CLI ile)

### Adım 1: GitHub CLI Kurulumu

**Homebrew ile:**
```bash
brew install gh
```

**Homebrew yoksa:**
1. https://brew.sh adresinden Homebrew kurun
2. Sonra `brew install gh`

### Adım 2: GitHub'a Giriş

```bash
gh auth login
```

Sizi yönlendirecek:
- GitHub'a giriş yapın
- Terminal'i yetkilendirin

### Adım 3: Repository Oluştur ve Push Et

```bash
cd /Users/ardaozel/road_defect_detection
gh repo create road-defect-detection --private --source=. --remote=origin --push
```

**⏱️ Süre: 5-10 dakika (kurulum dahil)**

---

## Hangisini Seçmeliyim?

### Web'den Yapın Eğer:
- ✅ Hızlıca yapmak istiyorsanız
- ✅ GitHub CLI kurmak istemiyorsanız
- ✅ Sadece bir kez yapacaksanız

### Terminal'den Yapın Eğer:
- ✅ Tekrar tekrar repository oluşturacaksanız
- ✅ Terminal kullanmayı seviyorsanız
- ✅ Otomasyon yapmak istiyorsanız

---

## Önerim

**İlk kez yapıyorsanız → Web'den yapın** (daha hızlı ve kolay)

Sonraki güncellemeler için zaten terminal komutları yeterli:
```bash
git add .
git commit -m "Update message"
git push
```
