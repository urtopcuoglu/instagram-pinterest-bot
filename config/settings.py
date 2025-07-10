# config/settings.py

# Instagram URL'leri
INSTAGRAM_LOGIN_URL = "https://www.instagram.com/accounts/login/"
INSTAGRAM_SAVED_POSTS_URL = "https://www.instagram.com/limozarus/saved/" # 'your_username' kısmını kendi kullanıcı adınızla değiştirin

# Pinterest URL'leri
PINTEREST_LOGIN_URL = "https://tr.pinterest.com/login/"
PINTEREST_CREATE_PIN_URL = "https://tr.pinterest.com/pin-builder/"

# Element bekleme süreleri (saniye cinsinden)
WAIT_TIME_SHORT = 5
WAIT_TIME_MEDIUM = 10
WAIT_TIME_LONG = 15

# WebDriver yolu (eğer PATH'e eklemediyseniz)
# WINDOWS için örnek:
# CHROME_DRIVER_PATH = "C:\\path\\to\\chromedriver.exe"
# LINUX/MACOS için örnek:
# CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

# Not: Eğer chromedriver.exe/chromedriver dosyasını sistem PATH'ine eklediyseniz bu satıra gerek yoktur.
# Genellikle driver'ı doğrudan proje klasörüne veya sistem PATH'ine koymak tercih edilir.