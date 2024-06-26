#!/bin/bash

# Python'un yüklü olduğundan emin olun
if ! command -v python3 &> /dev/null
then
    echo "Python yüklü değil. Lütfen Python'u yükleyin ve tekrar deneyin."
    exit
fi

# Sanal ortam oluşturun ve etkinleştirin
python3 -m venv venv
source venv/bin/activate

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python3 customgpt.py