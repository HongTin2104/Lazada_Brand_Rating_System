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

# import time
# import traceback
# import undetected_chromedriver as uc
# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium_stealth import stealth

# def setup_driver():
#     """Khởi tạo trình duyệt với undetected-chromedriver."""
#     try:
#         options = uc.ChromeOptions()
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        
#         driver = uc.Chrome(options=options, headless=False, use_subprocess=True)
        
#         stealth(driver,
#             languages=["en-US", "en"],
#             vendor="Google Inc.",
#             platform="Win32",
#             webgl_vendor="Intel Inc.",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True,
#         )
        
#         return driver
#     except Exception as e:
#         print(f"Lỗi khởi tạo trình duyệt: {e}")
#         print(traceback.format_exc())
#         return None

# def login_amazon(driver, email, password):
#     """Đăng nhập vào Amazon."""
#     try:
#         driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26useRedirectOnSuccess%3D1%26signIn%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
#         time.sleep(2)
        
#         email_input = driver.find_element(By.ID, "ap_email")
#         email_input.send_keys(email)
#         email_input.send_keys(Keys.RETURN)
#         time.sleep(2)
        
#         password_input = driver.find_element(By.ID, "ap_password")
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.RETURN)
#         time.sleep(5)
        
#         print("Đăng nhập thành công!")
#     except Exception as e:
#         print("Có lỗi khi đăng nhập:", e)
#         driver.quit()

# def scrape_amazon_search(driver, query=""):
#     """Truy xuất dữ liệu sản phẩm từ trang tìm kiếm Amazon."""
#     try:
#         search_url = f"https://www.amazon.com/s?k={query}"
#         driver.get(search_url)
#         wait = WebDriverWait(driver, 30)

#         body = driver.find_element(By.TAG_NAME, "body")
#         for _ in range(10):
#             body.send_keys(Keys.PAGE_DOWN)
#             time.sleep(2)

#         wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")))

#         elems_title = driver.find_elements(By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
#         titles = [elem.text.strip() for elem in elems_title[:100] if elem.text.strip()]

#         if not titles:
#             raise Exception("Không tìm thấy sản phẩm nào!")

#         df = pd.DataFrame(titles, columns=['title'])
#         print(df)
#         df.to_csv("amazon_products.csv", index=False)
#         print("Dữ liệu đã được lưu vào 'amazon_products.csv'")
#     except Exception as e:
#         print(f"Lỗi khi lấy dữ liệu: {e}")
#         print(traceback.format_exc())
#     finally:
#         driver.quit()
#         print("Trình duyệt đã đóng.")

# if __name__ == '__main__':
#     EMAIL = "0363117685"
#     PASSWORD = "Hayato2104"
#     QUERY = "dareu"
    
#     driver = setup_driver()
#     if driver:
#         login_amazon(driver, EMAIL, PASSWORD)
#         scrape_amazon_search(driver, QUERY)


# # s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator

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
    """Khởi tạo trình duyệt với undetected-chromedriver ở chế độ headless."""
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless=new")  # Chế độ headless
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        
        driver = uc.Chrome(options=options, headless=True, use_subprocess=True)
        
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

def scrape_amazon_search(driver, query=""):
    """Truy xuất dữ liệu sản phẩm từ trang tìm kiếm Amazon."""
    try:
        search_url = f"https://www.amazon.com/s?k={query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 30)

        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")))

        elems_title = driver.find_elements(By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
        titles = [elem.text.strip() for elem in elems_title[:100] if elem.text.strip()]

        if not titles:
            raise Exception("Không tìm thấy sản phẩm nào!")

        df = pd.DataFrame(titles, columns=['title'])
        print(df)
        df.to_csv("amazon_products.csv", index=False)
        print("Dữ liệu đã được lưu vào 'amazon_products.csv'")
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        print(traceback.format_exc())
    finally:
        driver.quit()
        print("Trình duyệt đã đóng.")

if __name__ == '__main__':
    QUERY = "dareu"
    
    driver = setup_driver()
    if driver:
        scrape_amazon_search(driver, QUERY)
