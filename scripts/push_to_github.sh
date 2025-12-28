#!/bin/bash
# GitHub'a push için kolay script

cd "$(dirname "$0")/.."

echo "📊 Checking for changes..."
git status

echo ""
read -p "Değişiklikleri commit edip push etmek istiyor musunuz? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📝 Değişiklikler ekleniyor..."
    git add .
    
    if [ -z "$1" ]; then
        read -p "Commit mesajı girin: " message
    else
        message="$1"
    fi
    
    git commit -m "$message"
    
    echo "🚀 GitHub'a push ediliyor..."
    git push
    
    echo ""
    echo "✅ Tamamlandı! Değişiklikler GitHub'a yüklendi."
else
    echo "❌ İptal edildi."
fi
