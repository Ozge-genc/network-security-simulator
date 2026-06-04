Siber Güvenlik ve Kriptografi Laboratuvarı
Bilgisayar Ağ Güvenliği dersi kapsamında geliştirilen bu proje; modern kriptografi algoritmalarını, veri doğrulama sistemlerini ve ağ izleme (sniffing) konseptlerini gerçek zamanlı olarak test edebileceğiniz interaktif bir siber güvenlik simülatörüdür.

Sadece savunma (şifreleme) mekanizmalarını değil, aynı zamanda saldırgan (kaba kuvvet ve sözlük saldırıları) simülasyonlarını da içerir.

 Özellikler ve Modüller
Bu laboratuvar 5 ana güvenlik modülünden oluşmaktadır:

 1. Sezar Şifrelemesi ve Kriptanaliz: Klasik kaydırma şifrelemesi ve anahtarsız metinleri saniyeler içinde çözen Brute-Force (Kaba Kuvvet) saldırı simülatörü.

 2. Hash, HMAC ve Parola Güvenliği: MD5, SHA-1 ve SHA-256 özet fonksiyonları. Banka API'lerinde kullanılan HMAC doğrulama sistemi. Sızdırılmış hash'leri kıran Sözlük Saldırısı (Dictionary Attack) aracı ve gerçek zamanlı Parola Güç (Entropy) Ölçer.

 3. AES (Simetrik Şifreleme): Fernet altyapısı kullanılarak 128-bit anahtarla AES şifreleme ve deşifreleme işlemleri.

 4. RSA ve Dijital İmza (Asimetrik Şifreleme): 512-bit Public/Private anahtar çifti üretimi. Gizlilik için asimetrik mesajlaşma ve inkar edememezlik (Non-repudiation) ilkesi için SHA-256 tabanlı Dijital İmza oluşturma/doğrulama.

 5. Ağ İletişimi (HTTP vs HTTPS): Verilerin ağ üzerinde taşınırken bir saldırgan (Sniffer) tarafından nasıl göründüğünü kanıtlayan gerçek zamanlı ağ paketi izleme simülasyonu.

 Kurulum
Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Depoyu Klonlayın:

Bash
git clone https://github.com/KULLANICI_ADINIZ/siber-guvenlik-lab.git
cd siber-guvenlik-lab
(Not: Yukarıdaki linke kendi GitHub depo adresinizi yazmayı unutmayın).

2. Gerekli Kütüphaneleri Yükleyin:

Bash
pip install -r requirements.txt
3. "Matrix" Karanlık Temasını Ayarlayın (Opsiyonel ama Havalı):
Proje ana dizininde .streamlit adında bir klasör ve içine config.toml dosyası oluşturup şu ayarları ekleyin:

Ini, TOML
[theme]
primaryColor = "#00ff00"
backgroundColor = "#050505"
secondaryBackgroundColor = "#111111"
textColor = "#00ff00"
font = "monospace"
4. Uygulamayı Başlatın:

Bash
streamlit run app.py
 Kullanılan Teknolojiler
Arayüz: Streamlit, Streamlit-Lottie

Kriptografi: cryptography (Fernet), rsa, hashlib, hmac

Dil: Python
