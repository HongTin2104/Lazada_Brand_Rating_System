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
        options.add_argument("--headless=new")  
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

def scrape_amazon_search(driver, query="", max_pages=5):
    """Truy xuất dữ liệu sản phẩm từ nhiều trang tìm kiếm Amazon."""
    try:
        search_url = f"https://www.amazon.com/s?k={query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 30)

        all_titles = []
        page_count = 0

        while page_count < max_pages:
            print(f"Đang thu thập dữ liệu trang {page_count + 1}...")

            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)

            wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")))

            elems_title = driver.find_elements(By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
            titles = [elem.text.strip() for elem in elems_title if elem.text.strip()]
            all_titles.extend(titles)

            try:
                next_button = driver.find_element(By.CLASS_NAME, "s-pagination-next")
                if "s-pagination-disabled" in next_button.get_attribute("class"):
                    print("Không còn trang nào để lấy dữ liệu.")
                    break 
                next_button.click()
                time.sleep(5) 
            except Exception:
                print("Không tìm thấy nút 'Next', kết thúc quá trình thu thập dữ liệu.")
                break

            page_count += 1

        if not all_titles:
            raise Exception("Không tìm thấy sản phẩm nào!")

        df = pd.DataFrame(all_titles, columns=['title'])
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
    QUERY = "logitech"
    MAX_PAGES = 5 
    
    driver = setup_driver()
    if driver:
        scrape_amazon_search(driver, QUERY, MAX_PAGES)
