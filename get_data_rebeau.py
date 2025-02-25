import time
import traceback
import requests
import undetected_chromedriver as uc
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
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

def scroll_to_load(driver):
    """Cuộn trang để tải đầy đủ sản phẩm."""
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def check_captcha(driver):
    """Kiểm tra và dừng nếu gặp Captcha của Amazon."""
    try:
        captcha_box = driver.find_element(By.XPATH, "//form[contains(@action, 'validateCaptcha')]")
        if captcha_box:
            print("Captcha phát hiện! Dừng thu thập dữ liệu để tránh bị chặn IP.")
            
            driver.quit()
            return True
    except:
        return False

def parse_product_data(html_content):
    """Phân tích HTML và trích xuất dữ liệu sản phẩm bằng BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.select("div.s-main-slot div[data-component-type='s-search-result']")
    data = []

    for product in products:
        try:
            title_elem = product.select_one("h2.a-size-mini span.a-text-normal")
            title = title_elem.text.strip() if title_elem else "Không có tiêu đề"

            price_whole = product.select_one("span.a-price-whole")
            price_fraction = product.select_one("span.a-price-fraction")
            price = f"{price_whole.text}.{price_fraction.text}" if price_whole and price_fraction else "Chưa cập nhật"

            url_elem = product.select_one("a.a-link-normal.s-no-outline")
            url = "https://www.amazon.com" + url_elem['href'] if url_elem else "Không có URL"
            
            data.append({"title": title, "price": price, "url": url})
        except Exception as e:
            print(f"Lỗi khi phân tích sản phẩm: {e}")
            continue
    
    return data

def scrape_amazon_search(driver, query="", max_pages=5):
    """Truy xuất tiêu đề, giá và URL sản phẩm từ nhiều trang tìm kiếm Amazon."""
    try:
        search_url = f"https://www.amazon.com/s?k={query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 10)

        all_data = []
        page_count = 0

        while page_count < max_pages:
            print(f"Đang thu thập dữ liệu trang {page_count + 1}...")

            # Kiểm tra Captcha
            if check_captcha(driver):
                break

            body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Cuộn trang để tải đầy đủ sản phẩm
            scroll_to_load(driver)
            time.sleep(2)

            # Lấy HTML và phân tích bằng BeautifulSoup
            html_content = driver.page_source
            page_data = parse_product_data(html_content)
            all_data.extend(page_data)

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "s-pagination-next")))
                if "s-pagination-disabled" in next_button.get_attribute("class"):
                    print("Không còn trang nào để lấy dữ liệu.")
                    # break
                next_button.click()
                time.sleep(5)  
            except Exception:
                print("Vui long cho.")
                # break

            page_count += 1

        if not all_data:
            raise Exception("Không tìm thấy sản phẩm nào!")

        df = pd.DataFrame(all_data)
        print(df)
        df.to_csv("amazon_products_optimized.csv", index=False)
        print("Dữ liệu đã được lưu vào 'amazon_products_optimized.csv'")
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        print(traceback.format_exc())
    finally:
        driver.quit()
        print("Trình duyệt đã đóng.")

if __name__ == '__main__':
    QUERY = "logitech"
    MAX_PAGES = 20
    
    driver = setup_driver()
    if driver:
        scrape_amazon_search(driver, QUERY, MAX_PAGES)
