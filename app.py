import streamlit as st
import hashlib
import hmac
from cryptography.fernet import Fernet
import rsa
import requests
from streamlit_lottie import st_lottie

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Siber Güvenlik Laboratuvarı", page_icon="🔐", layout="wide")

# --- LOTTIE ANİMASYON YÜKLEYİCİ ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_security = load_lottieurl("https://lottie.host/8040d908-0158-45fc-8833-28956cc5a519/aR1z06q4Sj.json")

# --- HAFIZA YÖNETİMİ ---
if 'aes_key' not in st.session_state: st.session_state.aes_key = None
if 'rsa_pub' not in st.session_state: st.session_state.rsa_pub = None
if 'rsa_priv' not in st.session_state: st.session_state.rsa_priv = None

# --- YAN MENÜ (Hatanın Çözüldüğü ve Tüm Menülerin Olduğu Kısım) ---
st.sidebar.title("🛡️ Güvenlik Paneli")
secim = st.sidebar.radio(
    "Menü",
    [
        "Ana Sayfa", 
        "1. Sezar Şifrelemesi ve Kırıcı", 
        "2. Hash, HMAC ve Parola Kırma", 
        "3. AES (Simetrik)", 
        "4. RSA ve Dijital İmza",
        "5. Ağ İletişimi: HTTP vs HTTPS"
    ]
)

# --- ANA SAYFA ---
if secim == "Ana Sayfa":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Siber Güvenlik Eğitim Aracına Hoş Geldiniz! 🌐")
        st.markdown("""
        Bu interaktif laboratuvar, siber güvenliğin derinliklerini keşfetmeniz için tasarlandı.
        
        Sol menüden bir konu seçerek şifreleme algoritmalarını test edebilir, ağ üzerindeki verilerin nasıl göründüğünü izleyebilir ve kendi saldırı simülasyonlarınızı gerçekleştirebilirsiniz.
        """)
    with col2:
        if lottie_security:
            st_lottie(lottie_security, height=250, key="security_anim")

# --- 1. SEZAR ŞİFRELEMESİ VE KIRICI ---
elif secim == "1. Sezar Şifrelemesi ve Kırıcı":
    st.title("🏛️ Sezar Şifrelemesi ve Analizi")
    tab1, tab2 = st.tabs(["🔒 Şifreleme & Çözme", "🏴‍☠️ Kaba Kuvvet (Brute-Force) Kırıcı"])
    
    with tab1:
        islem_tipi = st.radio("İşlem Seçin:", ("Şifrele", "Çöz"))
        mesaj = st.text_area("Mesajı Girin:")
        kaydirma = st.slider("Kaydırma Anahtarı (Shift):", 1, 25, 3)
        
        if st.button("Uygula"):
            if mesaj:
                sonuc = ""
                gercek_kaydirma = kaydirma if islem_tipi == "Şifrele" else -kaydirma
                ingilizce_kucuk, ingilizce_buyuk = 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                
                for harf in mesaj:
                    if harf in ingilizce_kucuk: sonuc += ingilizce_kucuk[(ingilizce_kucuk.index(harf) + gercek_kaydirma) % 26]
                    elif harf in ingilizce_buyuk: sonuc += ingilizce_buyuk[(ingilizce_buyuk.index(harf) + gercek_kaydirma) % 26]
                    else: sonuc += harf 
                
                st.toast('İşlem Başarıyla Tamamlandı! 🚀', icon='✅')
                st.code(sonuc, language="text")

    with tab2:
        st.info("Elinizde şifreli bir Sezar metni var ama anahtarı bilmiyor musunuz? Sistemin tüm 25 ihtimali saniyeler içinde denemesini izleyin.")
        kirilacak_mesaj = st.text_input("Şifreli Mesajı Girin (Ciphertext):")
        if st.button("Şifreyi Kır"):
            if kirilacak_mesaj:
                ingilizce_kucuk, ingilizce_buyuk = 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                st.write("### Tüm İhtimaller:")
                for i in range(1, 26):
                    deneme_sonucu = ""
                    for harf in kirilacak_mesaj:
                        if harf in ingilizce_kucuk: deneme_sonucu += ingilizce_kucuk[(ingilizce_kucuk.index(harf) - i) % 26]
                        elif harf in ingilizce_buyuk: deneme_sonucu += ingilizce_buyuk[(ingilizce_buyuk.index(harf) - i) % 26]
                        else: deneme_sonucu += harf
                    st.text(f"Anahtar {i}: {deneme_sonucu}")

# --- 2. HASH, HMAC VE PAROLA KIRMA ---
elif secim == "2. Hash, HMAC ve Parola Kırma":
    st.title("🔑 Hash Fonksiyonları ve Parola Güvenliği")
    
    # YENİ EKLENEN "PAROLA GÜÇ ÖLÇER" İÇİN SEKME (tab4) BURADA!
    tab1, tab2, tab3, tab4 = st.tabs(["Standart Hash", "HMAC", "🏴‍☠️ Sözlük Saldırısı", "🛡️ Parola Güç Ölçer"])
    
    with tab1:
        mesaj = st.text_input("Hash Alınacak Metin:")
        if mesaj:
            col1, col2, col3 = st.columns(3)
            with col1: 
                st.subheader("MD5")
                st.code(hashlib.md5(mesaj.encode('utf-8')).hexdigest(), language="text")
                st.metric(label="Uzunluk", value="32 Karakter", delta="Eski Teknoloji", delta_color="inverse")
            with col2: 
                st.subheader("SHA-1")
                st.code(hashlib.sha1(mesaj.encode('utf-8')).hexdigest(), language="text")
                st.metric(label="Uzunluk", value="40 Karakter", delta="Zayıf Güvenlik", delta_color="inverse")
            with col3: 
                st.subheader("SHA-256")
                st.code(hashlib.sha256(mesaj.encode('utf-8')).hexdigest(), language="text")
                st.metric(label="Uzunluk", value="64 Karakter", delta="Yüksek Güvenlik")

    with tab2:
        st.info("HMAC (Hash-based Message Authentication Code), verinin kimden geldiğini doğrular.")
        hmac_mesaj = st.text_input("Mesaj:", key="hmac_msg")
        gizli_anahtar = st.text_input("Gizli Anahtar (Secret Key):", type="password")
        if hmac_mesaj and gizli_anahtar:
            hmac_sonuc = hmac.new(gizli_anahtar.encode('utf-8'), hmac_mesaj.encode('utf-8'), hashlib.sha256).hexdigest()
            st.toast('HMAC Başarıyla Üretildi!', icon='🔒')
            st.code(hmac_sonuc, language="text")

    with tab3:
        st.error("Bir veritabanından sızdırılmış bir MD5 hash'ini kırmaya çalışın.")
        hedef_hash = st.text_input("Kırılacak MD5 Hash Değeri (Örn: e10adc3949ba59abbe56e057f20f883e):")
        sozluk = ["123456", "password", "admin", "12345678", "qwerty", "iloveyou", "12345", "111111"]
        
        if st.button("Sözlük Saldırısını Başlat"):
            if hedef_hash:
                kirildi = False
                with st.spinner("Sözlük taranıyor..."):
                    for kelime in sozluk:
                        if hashlib.md5(kelime.encode('utf-8')).hexdigest() == hedef_hash:
                            st.balloons() 
                            st.success(f"🎯 ŞİFRE KIRILDI! Eşleşme: **{kelime}**")
                            kirildi = True
                            break
                if not kirildi:
                    st.warning("Bu sözlükteki kelimeler eşleşmedi.")

    # YENİ ÖZELLİK: PAROLA GÜÇ ÖLÇER UYGULAMASI
    with tab4:
        st.info("Modern parola çatlatıcılar saniyede milyarlarca deneme yapabilir. Parolanız buna dayanabilir mi?")
        analiz_edilecek_sifre = st.text_input("Test Edilecek Parola (Gizli tutulmaz):", type="default")
        
        if analiz_edilecek_sifre:
            puan = 0
            uyarilar = []
            uzunluk = len(analiz_edilecek_sifre)
            
            if uzunluk >= 8: puan += 25
            else: uyarilar.append("Parola çok kısa (en az 8 karakter olmalı).")
            
            if uzunluk >= 12: puan += 25
            
            if any(c.islower() for c in analiz_edilecek_sifre) and any(c.isupper() for c in analiz_edilecek_sifre):
                puan += 25
            else: uyarilar.append("Hem büyük hem küçük harf içermeli.")
                
            if any(c.isdigit() for c in analiz_edilecek_sifre) and any(c in "!@#$%^&*()_+-=[]{}|;':,./<>?" for c in analiz_edilecek_sifre):
                puan += 25
            else: uyarilar.append("Rakam ve özel semboller (!,@,#, vb.) içermeli.")
            
            st.progress(puan / 100)
            
            if puan <= 25:
                st.error("🚨 ÇOK ZAYIF: Bu parola anında kırılır!")
            elif puan <= 50:
                st.warning("⚠️ ZAYIF: Sözlük saldırılarına karşı savunmasız.")
            elif puan <= 75:
                st.info("✅ GÜÇLÜ: Standart bir kullanım için yeterli.")
            else:
                st.success("🛡️ KIRILAMAZ: Askeri düzeyde güvenlik! (Yüzlerce yıl sürer)")
                
            if uyarilar:
                st.write("**Nasıl Geliştirebilirsiniz?**")
                for uyari in uyarilar:
                    st.write(f"- {uyari}")

# --- 3. AES ---
elif secim == "3. AES (Simetrik)":
    st.title("🔒 AES (Simetrik Şifreleme)")
    st.subheader("1. Anahtar Yönetimi")
    if st.button("Yeni AES Anahtarı Üret"): 
        st.session_state.aes_key = Fernet.generate_key()
        st.toast('Yeni AES Anahtarı Üretildi!', icon='🔑')
    
    if st.session_state.aes_key: st.code(st.session_state.aes_key.decode('utf-8'), language="text")
    else: st.warning("Henüz bir anahtar üretilmedi.")
    st.divider()
    
    islem_tipi = st.radio("İşlem:", ("Şifrele", "Çöz"))
    metin_aes = st.text_area("İşlem Yapılacak Metin:")
    if st.button("AES Uygula") and st.session_state.aes_key and metin_aes:
        fernet = Fernet(st.session_state.aes_key)
        try:
            if islem_tipi == "Şifrele":
                st.toast('Metin Şifrelendi!', icon='🛡️')
                st.code(fernet.encrypt(metin_aes.encode('utf-8')).decode('utf-8'), language="text")
            else:
                st.toast('Şifre Çözüldü!', icon='🔓')
                st.code(fernet.decrypt(metin_aes.encode('utf-8')).decode('utf-8'), language="text")
        except: st.error("Hata! Çözmeye çalıştığınız metin geçerli bir ciphertext değil.")

# --- 4. RSA VE DİJİTAL İMZA ---
elif secim == "4. RSA ve Dijital İmza":
    st.title("🔐 RSA ve Dijital İmza")
    if st.button("RSA Anahtar Çifti Üret (512-bit)"):
        pub, priv = rsa.newkeys(512)
        st.session_state.rsa_pub, st.session_state.rsa_priv = pub, priv
        st.toast('RSA Anahtar Çifti Üretildi!', icon='🗝️')
    
    if st.session_state.rsa_pub:
        col1, col2 = st.columns(2)
        with col1: st.write("**Public Key:**"); st.code(st.session_state.rsa_pub.save_pkcs1().decode('utf-8'), language="text")
        with col2: st.write("**Private Key:**"); st.code(st.session_state.rsa_priv.save_pkcs1().decode('utf-8'), language="text")
    
    st.divider()
    tab1, tab2 = st.tabs(["✉️ Şifreleme", "✍️ İmza"])
    with tab1:
        islem_rsa = st.radio("İşlem:", ("Şifrele", "Çöz"))
        metin_rsa = st.text_area("Mesaj (Sınır 53 Byte):")
        if st.button("RSA Uygula") and st.session_state.rsa_pub and metin_rsa:
            try:
                if islem_rsa == "Şifrele": 
                    st.toast('Açık Anahtar ile Şifrelendi!', icon='🔒')
                    st.code(rsa.encrypt(metin_rsa.encode('utf-8'), st.session_state.rsa_pub).hex(), language="text")
                else: 
                    st.toast('Gizli Anahtar ile Çözüldü!', icon='🔓')
                    st.code(rsa.decrypt(bytes.fromhex(metin_rsa), st.session_state.rsa_priv).decode('utf-8'), language="text")
            except Exception as e: st.error("İşlem Hatası!")
    with tab2:
        imza_islem = st.radio("İmza:", ("İmzala (Private)", "Doğrula (Public)"))
        if imza_islem == "İmzala (Private)":
            imzalanacak = st.text_area("Mesaj:")
            if st.button("İmzala") and st.session_state.rsa_priv:
                st.toast('Mesaj İmzalandı!', icon='✍️')
                st.code(rsa.sign(imzalanacak.encode('utf-8'), st.session_state.rsa_priv, 'SHA-256').hex(), language="text")
        else:
            mesaj_orj = st.text_area("Orijinal Mesaj:")
            imza_hex = st.text_area("İmza (Hex):")
            if st.button("Doğrula") and st.session_state.rsa_pub:
                try:
                    rsa.verify(mesaj_orj.encode('utf-8'), bytes.fromhex(imza_hex), st.session_state.rsa_pub)
                    st.success("✅ İMZA GEÇERLİ!")
                except: st.error("❌ İMZA GEÇERSİZ VEYA SAHTE!")

# --- 5. AĞ İLETİŞİMİ: HTTP vs HTTPS ---
elif secim == "5. Ağ İletişimi: HTTP vs HTTPS":
    st.title("📡 Ağ Paketi İzleme Simülasyonu")
    st.markdown("Verileriniz internet kablolarından geçerken bir saldırgan veya internet sağlayıcınız tarafından **nasıl görünür?**")
    
    protokol = st.radio("Kullanılacak Ağ Protokolü:", ("🌐 HTTP (Güvensiz)", "🔒 HTTPS (Güvenli - TLS/AES)"))
    gonderilecek_mesaj = st.text_input("Gönderilecek Gizli Mesaj (Örn: Kredi Kartı Şifresi):")
    
    if gonderilecek_mesaj:
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.info("💻 Sizin Bilgisayarınız")
            st.write(f"**Gönderilen:**\n{gonderilecek_mesaj}")
            
        with col2:
            st.warning("🕵️ Ağ Üzerindeki İzleyici")
            if protokol == "🌐 HTTP (Güvensiz)":
                st.error("Veri Açık Metin (Plaintext) olarak akıyor!")
                st.code(gonderilecek_mesaj, language="text")
            else:
                st.success("Veri Şifreli (Ciphertext) olarak akıyor!")
                sahte_sifre = hashlib.sha256(gonderilecek_mesaj.encode()).hexdigest()
                st.code(sahte_sifre[:30] + "...(şifreli paket)", language="text")
                
        with col3:
            st.info("🏢 Hedef Sunucu (Banka)")
            st.write(f"**Ulaşan:**\n{gonderilecek_mesaj}")