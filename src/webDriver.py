from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')       # 창 숨기는 옵션 추가
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("lang=ko_KR")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)