# # sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16
# # sg-col-inner
# # s-search-results
# # sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16
# # sg-col-inner
# # a-declarative
# # puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v2cecso46ziiky2912svgi7ywcj s-latency-cf-section puis-card-border
# # a-section
# # puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right
# # puisg-col-inner
# # a-section a-spacing-small a-spacing-top-small
# # a-section a-spacing-none puis-padding-right-small s-title-instructions-style
# # a-link-normal s-line-clamp-2 s-link-style a-text-normal
# # a-size-medium a-spacing-none a-color-base a-text-normal
# # <h2 aria-label="MX Keys S Combo - Performance Wireless Keyboard and Mouse with Palm Rest, Customizable Illumination, Fast Scrolling, Bluetooth, USB C, for Windows, Linux, Chrome, Mac" class="a-size-medium a-spacing-none a-color-base a-text-normal"><span>MX Keys S Combo - Performance Wireless Keyboard and Mouse with Palm Rest, Customizable Illumination, Fast Scrolling, Bluetooth, USB C, for Windows, Linux, Chrome, Mac</span></h2>
# # thứ tự của các thẻ từ cha đến con, lấy thẻ h2 aria-label cuar class a-size-medium a-spacing-none a-color-base a-text-normal ra làm tiêu đề (title), can sua css selector

import time
import traceback
import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

def setup_driver():
    """Khởi tạo trình duyệt với undetected-chromedriver."""
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        
        driver = uc.Chrome(options=options, headless=False, use_subprocess=True)
        
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        return driver
    except Exception as e:
        print(f"Lỗi khởi tạo trình duyệt: {e}")
        print(traceback.format_exc())
        return None

def scrape_amazon_search(query=""):
    """Truy xuất dữ liệu sản phẩm từ trang tìm kiếm Amazon."""
    driver = setup_driver()
    if driver is None:
        return
    
    try:
        search_url = f"https://www.amazon.com/s?k={query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 30)

        # Cuộn trang để tải dữ liệu
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        # Chờ phần tử tiêu đề xuất hiện
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
        ))

        # Lấy danh sách tiêu đề sản phẩm
        elems_title = driver.find_elements(By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
        titles = [elem.text.strip() for elem in elems_title[:10] if elem.text.strip()]

        if not titles:
            raise Exception("Không tìm thấy sản phẩm nào!")

        # Lưu dữ liệu vào DataFrame
        df = pd.DataFrame(titles, columns=['title'])
        print(df)
        
        # Lưu vào file CSV
        df.to_csv("amazon_products.csv", index=False)
        print("Dữ liệu đã được lưu vào 'amazon_products.csv'")
    
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        print(traceback.format_exc())
    
    finally:
        driver.quit()
        print("Trình duyệt đã đóng.")

if __name__ == '__main__':
    scrape_amazon_search("dareu")
