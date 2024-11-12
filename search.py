import os
import gdown
import streamlit as st
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.parse
import random 
st.set_page_config(page_title="SEARCH ENGINER", page_icon="🎬", layout="wide")
def click_random_element(driver):
    """Nhấp đúp chuột vào một phần tử ngẫu nhiên trên trang."""
    # Tìm tất cả các phần tử có thể nhấp trên trang
    clickable_elements = driver.find_elements(By.XPATH,"//*[self::a or self::button or @onclick or @role='button']")
    
    # Kiểm tra nếu có phần tử có thể nhấp
    if clickable_elements:
        # Chọn một phần tử ngẫu nhiên
        random_element = random.choice(clickable_elements)
        
        # Thực hiện nhấp đúp chuột vào phần tử đã chọn
        actions = ActionChains(driver)
        actions.double_click(random_element).perform()
        
        # Thời gian nghỉ ngẫu nhiên sau khi nhấp
        time.sleep(random.uniform(0.5, 1))
    else:
        print("Không tìm thấy phần tử có thể nhấp nào trên trang.")

def openWeb(driver_path):
    # Đường dẫn đến trình điều khiển của trình duyệt, ở đây sử dụng Chrome
    # Thay đổi thành đường dẫn tới ChromeDriver trên máy của bạn
    driver = webdriver.Chrome()
    return driver
def simulate_scroll(driver):
    """Cuộn trang ngẫu nhiên."""
    scroll_amount = 50000
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(1)
def download_chorme_driver():
    gdrive_url = 'https://drive.google.com/file/d/1hTGC8t3PbfGxeAs0YhQTRApdveOwBQbM/view?usp=drive_link'  # Thay YOUR_FILE_ID bằng ID file trên Google Drive

    # Đường dẫn lưu tạm thời ChromeDriver trên máy
    driver_path = 'chromedriver.exe'

    # Tải file về từ Google Drive
    gdown.download(gdrive_url, driver_path, quiet=False)
    return driver_path
if 'driver1' not in st.session_state:
    st.session_state.driver1 = None 

if 'list_link' not in st.session_state:
    st.session_state.list_link = []
col1, col2 = st.columns([2,1])
try:
   driver = webdriver.Chrome()
   driver.close()
except Exception:
   st.write("Chưa có chormedriver.exe")
with col1:
    st.write("Đã có chormedriver.exe chưa. Nếu chưa bấm để tải")
with col2:
    if st.button("Tải chormedriver.exe"):
        driver_path= download_chorme_driver()
col1, col2 = st.columns([1,1])
with col1:
    url_driver = st.text_input("Nhập đường dẫn đến chormedriver.exe:")
    driver_path = url_driver
st.session_state.driver1 = openWeb(driver_path) 
st.write(f"['{datetime.now()}'] Thực thi khởi tạo bot")

with col2:
    find = st.text_input("Nhập từ khóa:")
                # Mã hóa chuỗi
    encoded_query = urllib.parse.quote(find)
    # URL kết quả
    url = f"https://www.tiktok.com/search/video?q={encoded_query}"

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Khởi tạo bot 1"):
        st.session_state.driver1.get(url)
        time.sleep(1)
        for i in range(1,10):   
            simulate_scroll(st.session_state.driver1)
            st.write(f"['{datetime.now()}'] ĐANG CUỘN LẦN ",i)
            time.sleep(1)
        links = st.session_state.driver1.find_elements(By.XPATH, "//a")
        st.session_state.list_link = []
        for i in links:
            try:
                link = i.get_attribute("href")
                if '/video/' in link:
                    st.session_state.list_link.append(link)
            except AttributeError:
                continue
        st.write(f"['{datetime.now()}'] đã lấy được {len(st.session_state.list_link )} video ")

with col2:
    if st.button("Khởi tạo bot 2"):
        for i in st.session_state.list_link :
            st.write(f"['{datetime.now()}'] tải từ link {i} ")
            driver2 = openWeb(driver_path)
            driver2.get('https://snaptik.vn/')
            time.sleep(1)
            textbox = driver2.find_element(By.XPATH, "//input[@id='url']")
            textbox.send_keys(i)
            time.sleep(1)
            download_btn1 = driver2.find_element(By.XPATH, "//button[@id='submit']")
            download_btn1.click()
            time.sleep(3)
            download_btn2 = driver2.find_element(By.XPATH, "//ul[@class='downloads']//a")
            download_btn2.click()
            time.sleep(2)
            click_random_element(driver2)
            click_random_element(driver2)
            time.sleep(5)
            driver2.close()