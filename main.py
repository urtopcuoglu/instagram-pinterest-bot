# main.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

# config/settings.py dosyasındaki ayarları içe aktarın
from config.settings import INSTAGRAM_LOGIN_URL, INSTAGRAM_SAVED_POSTS_URL, WAIT_TIME_SHORT, WAIT_TIME_MEDIUM, WAIT_TIME_LONG

# src/instagram.py dosyasındaki fonksiyonları içe aktarın
from src.instagram import login_instagram, get_saved_posts

# .env dosyasını yükle (hassas bilgileri çekmek için)
load_dotenv()

def initialize_driver():
    """Chrome WebDriver'ı başlatır ve döndürür."""
    driver = webdriver.Chrome()
    driver.maximize_window() # Tarayıcı penceresini tam ekran yapar
    return driver

def run_bot_flow():
    """Botun ana akışını çalıştırır."""
    driver = initialize_driver()
    instagram_username = os.getenv("INSTAGRAM_USERNAME")
    instagram_password = os.getenv("INSTAGRAM_PASSWORD")

    if not instagram_username or not instagram_password:
        print("Hata: Instagram kullanıcı adı veya şifre .env dosyasında tanımlı değil.")
        driver.quit()
        return

    try:
        print("WebDriver başarıyla başlatıldı.")
        
        # Instagram'a giriş yapmayı dene
        if login_instagram(driver, instagram_username, instagram_password):
            print("Instagram'a otomatik giriş başarılı.")
            
            # Giriş sonrası kaydedilenler sayfasına git
            print(f"Kaydedilen gönderiler URL'sine gidiliyor: {INSTAGRAM_SAVED_POSTS_URL}")
            driver.get(INSTAGRAM_SAVED_POSTS_URL)

            # Sayfanın yüklenmesini bekleyelim (örneğin bir gönderi linkinin görünmesini)
            try:
                WebDriverWait(driver, WAIT_TIME_MEDIUM).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]"))
                )
                print("Kaydedilenler sayfası başarılı bir şekilde yüklendi.")
                print(f"Güncel URL: {driver.current_url}")
            except:
                print("Kaydedilenler sayfası doğrudan URL ile yüklenemedi veya element bulunamadı.")
                print(f"Güncel URL: {driver.current_url}")
                # Buraya düşerse, profil sayfasına gidip "Kaydedilenler" sekmesine tıklama mantığını eklememiz gerekecek.
                # Şimdilik tarayıcıyı açık bırakıp manuel kontrol edebiliriz.

            time.sleep(WAIT_TIME_LONG) # Sayfayı gözlemlemek için uzun bir bekleme

            # get_saved_posts fonksiyonunu daha sonra burada çağıracağız
            # saved_posts_data = get_saved_posts(driver)
            # print(f"Çekilen gönderi sayısı: {len(saved_posts_data)}")

        else:
            print("Instagram'a otomatik giriş başarısız oldu. Lütfen .env dosyasındaki bilgileri ve internet bağlantınızı kontrol edin.")

    except Exception as e:
        print(f"Bot çalışırken bir hata oluştu: {e}")
    finally:
        print("Tarayıcı kapatılıyor.")
        driver.quit()

if __name__ == "__main__":
    run_bot_flow()