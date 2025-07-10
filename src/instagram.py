# src/instagram.py'nin güncellenmiş hali (önceki kodun altına ekleyin veya mevcut get_saved_posts'u değiştirin)

# Diğer importlar zaten olmalı:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

from config.settings import INSTAGRAM_LOGIN_URL, INSTAGRAM_SAVED_POSTS_URL, WAIT_TIME_SHORT, WAIT_TIME_MEDIUM, WAIT_TIME_LONG

load_dotenv()

# login_instagram fonksiyonu burada kalacak, onu değiştirmedik
def login_instagram(driver, username, password):
    # ... (önceki login_instagram fonksiyonunuzun kodu)
    pass # Yer tutucu

def get_saved_posts(driver):
    """
    Instagram'dan kaydedilen gönderilerin URL'lerini, resim URL'lerini ve açıklamalarını çeker.
    Sayfayı aşağı kaydırarak tüm gönderileri yüklemeye çalışır.
    """
    print("Kaydedilen gönderileri çekmeye başlanıyor...")
    driver.get(INSTAGRAM_SAVED_POSTS_URL)
    
    # Sayfanın yüklenmesini bekle
    try:
        WebDriverWait(driver, WAIT_TIME_MEDIUM).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]")) # İlk gönderi linkini bekle
        )
        print("Kaydedilenler sayfası yüklendi.")
    except Exception as e:
        print(f"Kaydedilenler sayfası yüklenirken bir hata oluştu veya gönderi bulunamadı: {e}")
        return []

    saved_posts_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0 # Sonsuz döngüyü engellemek için deneme sayacı

    # Tüm gönderiler yüklenene kadar sayfayı kaydır
    print("Sayfa aşağı kaydırılıyor...")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(WAIT_TIME_SHORT) # Yeni içerik yüklenmesi için bekle

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts > 3: # Üç kez kaydırma yapılmasına rağmen yeni içerik gelmediyse dur
                print("Tüm gönderilerin yüklendiği varsayılıyor.")
                break
        else:
            scroll_attempts = 0 # Yeni içerik geldiyse sayacı sıfırla
        last_height = new_height
    
    print("Tüm gönderiler yüklendikten sonra veri çekiliyor...")

    # Gönderi elementlerini bul
    # Instagram'ın gönderi linkleri genellikle "/p/" ile başlar.
    # Bu XPath'i Instagram'ın güncel yapısına göre ayarlamanız gerekebilir.
    # Tarayıcınızın geliştirici araçlarını (F12) kullanarak doğru XPath/CSS selector'ları bulabilirsiniz.
    
    # Genel bir gönderi linki/container XPath'i örneği:
    # Bu, tüm gönderi kutularını içeren div'leri veya a etiketlerini bulmaya çalışır.
    # Her bir gönderinin bir resim (img) ve bir link (a) içereceğini varsayıyoruz.
    post_elements = driver.find_elements(By.XPATH, "//div[contains(@class, '_aagv')]/img/ancestor::a") 
    # Veya daha basit bir deneme: driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")

    # Eğer yukarıdaki XPath çalışmazsa, Instagram'ın mevcut HTML yapısına bakmanız gerekecektir.
    # Örneğin, aşağıdaki gibi bir yapı olabilir:
    # post_elements = driver.find_elements(By.CSS_SELECTOR, "div._aagv > img[srcset] + img[srcset] + img[srcset]")

    # Alternatif olarak:
    # post_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='_aagv'] > img[srcset]")
    # Bu elementler doğrudan gönderinin resmini veya linkini tutabilir.
    
    print(f"Bulunan potansiyel gönderi elementleri: {len(post_elements)}")

    for i, post_element in enumerate(post_elements):
        try:
            post_url = post_element.get_attribute("href")
            # Her bir post_element'in içindeki img etiketinin src'sini bulmaya çalışalım
            # Bu, post_element'in yapısına bağlıdır.
            # Örneğin, eğer post_element doğrudan <a> ise, içindeki <img>'yi bulmanız gerekir.
            # img_element = post_element.find_element(By.TAG_NAME, "img")
            # image_url = img_element.get_attribute("src")

            # Instagram'da genellikle ilk yüklenen resim daha düşük çözünürlüklü olur.
            # srcset attribute'u farklı çözünürlükleri içerir. En büyük olanı bulmaya çalışabiliriz.
            
            # Şimdilik örnek olarak sadece URL çekelim, resim ve açıklama için detaylı inceleme gerekecek
            image_url = None # Şimdilik boş bırakalım
            description = f"Instagram'dan kaydedilen gönderi {i+1}" # Varsayılan açıklama

            if post_url:
                saved_posts_data.append({
                    "url": post_url,
                    "image_url": image_url, # Daha sonra burayı geliştireceğiz
                    "description": description
                })
        except Exception as e:
            print(f"Gönderi elementi işlenirken hata: {e}")
            continue

    print(f"Toplam {len(saved_posts_data)} kaydedilen gönderi bilgisi çekildi.")
    return saved_posts_data