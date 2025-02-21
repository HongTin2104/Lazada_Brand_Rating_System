import time
import traceback
import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import mysql.connector

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

def convert_price_to_float(price_str):
    """Chuyển đổi chuỗi giá thành số thực (float)."""
    try:
        price_str = price_str.replace(",", "").replace("$", "")
        return float(price_str)
    except ValueError:
        return None

def save_to_mysql(data):
    """Lưu dữ liệu vào MySQL."""
    try:
        # Kết nối đến MySQL (không tạo database và bảng)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ng230204!",
            database="amazon_data"  # Đã có sẵn database
        )
        cursor = conn.cursor()

        # Chèn dữ liệu vào bảng `product`
        for item in data:
            cursor.execute("INSERT INTO product (title, price) VALUES (%s, %s)", (item['title'], item['price']))
        
        conn.commit()
        print("Dữ liệu đã được lưu vào MySQL.")
    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        cursor.close()
        conn.close()

def scrape_amazon_search(driver, query="", max_pages=5):
    """Truy xuất tiêu đề và giá sản phẩm từ nhiều trang tìm kiếm Amazon."""
    try:
        search_url = f"https://www.amazon.com/s?k={query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 10)

        all_data = []
        page_count = 0

        while page_count < max_pages:
            print(f"Đang thu thập dữ liệu trang {page_count + 1}...")

            body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)

            wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")))

            products = driver.find_elements(By.XPATH, "//div[contains(@class, 's-main-slot')]/div[@data-component-type='s-search-result']")

            for product in products:
                try:
                    elems_title = product.find_elements(By.XPATH, ".//h2[contains(@class, 'a-size-medium a-spacing-none a-color-base a-text-normal')]")
                    titles = [elem.text.strip() for elem in elems_title if elem.text.strip()]
                    title = titles[0] if titles else "Không có tiêu đề"
                except:
                    title = "Không có tiêu đề"

                try:
                    price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                    price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
                    price = f"{price_whole}.{price_fraction}"
                    price = convert_price_to_float(price)
                except:
                    price = None

                all_data.append({"title": title, "price": price})

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "s-pagination-next")))
                if "s-pagination-disabled" in next_button.get_attribute("class"):
                    print("Không còn trang nào để lấy dữ liệu.")
                    break
                time.sleep(5)
                next_button.click()
            except Exception:
                print("Không tìm thấy nút 'Next', kết thúc quá trình thu thập dữ liệu.")
                break

            page_count += 1

        if not all_data:
            raise Exception("Không tìm thấy sản phẩm nào!")

        # Lưu vào MySQL
        save_to_mysql(all_data)

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        print(traceback.format_exc())
    finally:
        driver.quit()
        print("Trình duyệt đã đóng.")


if __name__ == '__main__':
    QUERY = "logitech"
    MAX_PAGES = 6
    
    driver = setup_driver()
    if driver:
        scrape_amazon_search(driver, QUERY, MAX_PAGES)
