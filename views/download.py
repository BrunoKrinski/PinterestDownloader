import time
import flet as ft
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global status
global urls

def search_images(email, password, link, page):
    print('executando seach ')
        
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)

    driver.get("https://br.pinterest.com/")

    enter_path = '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div/div'
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()

    username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))

    username_field.clear()
    username_field.send_keys(email)   
    password_field.clear()
    password_field.send_keys(password)
    
    enter_path = '//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button/div'
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()

    time.sleep(10)
    global urls
    urls = []
    
    driver.get(link)

    time.sleep(10)
    
    global status
    status.value = "Searching for Images..."
    status.update()
    
    scroll_times = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    i = 0
    while i < 10:
        i += 1
        anchors = driver.find_elements(By.TAG_NAME, "img")
        anchors = [anchor for anchor in anchors]

        for anchor in anchors:
            try:
                link = anchor.get_attribute("srcset")
                link = link.split(',')[-1].split(' ')[1]
                urls.append(link)
            except:
                continue 
        scroll_times += 1

        if scroll_times == 100:
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                scroll_times = 0
        
        driver.execute_script("window.scrollBy(0, 25);")
    driver.quit()
    #urls = list(set(urls))
    print('search')
    urls = list(set(urls))
    print(len(urls))
    #return urls
    page.go("/")

def download_images():
    print('executando download')    
    global search_thread
    search_thread.join()
    
    global status
    status.value = "Downloading Images"
    status.update()
    
    global pb
    pb.height = 0
    pb.update()
    
    global urls
    print('download')   
    print(len(urls)) 
    #for url in urls:
    #    print(url)

def DownloadView(page, params):
    
    email, password, link = params['params'].split('&')
    link = link.replace("|","/")
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
        
    space = lambda height = 0 : ft.Container(height = height)
    
    global search_thread
    search_thread = Thread(target = search_images,
                           args = (email, password, link, page))
    search_thread.start()
    '''
    download_thread = Thread(target = download_images)
    download_thread.start()
    '''
        
    space = lambda height = 0 : ft.Container(height = height)
    
    global status
    status = ft.Text(
        "Initializing...",
        size = 50,
        color = ft.colors.BLUE,
        font_family = "RubikIso")
    
    global pb
    pb = ft.ProgressBar(
        width = page.width / 1.2,
        height = 20,
        color = ft.colors.WHITE)
            
    title = ft.Text(
        "Pinterest Downloader!", 
        size = 100,
        color = ft.colors.BLUE,
        weight = ft.FontWeight.BOLD,
        font_family = "RubikIso")
        
    return ft.View(
        "/download",
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            title,
            space(75),    
            status,
            space(5),    
            pb,
        ]
    )