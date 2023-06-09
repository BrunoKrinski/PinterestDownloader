import os
import time
import getpass
import requests
import flet as ft
from sys import platform
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_images(email, password, link, browser):
    
    global err_message
    err_message = None
    
    if browser == "Chrome":            
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service_log_path=os.devnull, options=options)
    elif browser == "Firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(service_log_path=os.devnull, options=options)

    driver.get("https://pinterest.com/")
    
    enter_path = '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div/div'
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()
    except TimeoutException:
        err_message = "Error on login!"
        driver.quit()
        return

    username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))

    username_field.clear()
    username_field.send_keys(email)   
    password_field.clear()
    password_field.send_keys(password)
    
    enter_path = '//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button/div'
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()
    except TimeoutException:
        err_message = "Error on login!"
        driver.quit()
        return

    time.sleep(10)
    
    global urls
    urls = []
    
    for i in range(10):
        if i == 9:
            err_message = "Error on login or Pinterest link unavailable!"
            driver.quit()
            return
        
        driver.get(link)
        time.sleep(10)
        try:
            driver.find_element(By.CSS_SELECTOR,"div.FNs.zI7.iyn.Hsu")
            break
        except NoSuchElementException:
            continue
        
    
    global status
    status.value = "Searching for Images..."
    status.update()
    
    scroll_times = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        anchors = driver.find_elements(By.TAG_NAME, "img")

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
        
        driver.execute_script("window.scrollBy(0, 50);")
    driver.quit()
    
    urls = list(set(urls))
    
def download_images():
    
    global search_thread
    search_thread.join()
        
    global pb
    global urls
    global images
    global status
    global status2
    global err_message
    global return_button
    global return_container
    
    if err_message is not None:
        pb.height = 0
        pb.update()
        status.color = ft.colors.RED
        status.value = err_message
        status.update()
        return_container.height = 0
        return_container.update()
        return_button.height = 50
        return_button.update()
        return
        
    status.value = "Downloading Images..."
    status.update()
    
    usr = getpass.getuser()
    if platform == "linux" or platform == "linux2":
        images_folder = f"/home/{usr}/Pictures/PinterestDownloader/"
    elif platform == "win32":
        images_folder = f"C:\\Users\\{usr}\\Pictures\\PinterestDownloader\\"
    os.makedirs(images_folder, exist_ok = True)
        
    for i, url in enumerate(urls):           
        
        url = url.replace('\n','')      
        img_request = requests.get(url) 
            
        if img_request.status_code == 200:
            
            image_name = url.split('/')[-1]
            
            pth = f"{images_folder}{image_name}"
            with open(pth, 'wb') as f:
                f.write(img_request.content)
            
            if len(images.controls) > 5:
                images.controls.pop(0)
            
            images.controls.append(
                ft.Image(
                    src = pth,
                    width = 198,
                    height = 400,
                    fit = ft.ImageFit.COVER,
                    repeat = ft.ImageRepeat.NO_REPEAT,
                    border_radius = ft.border_radius.all(10)))
            images.update()
        pb.value = i / len(urls)
        pb.update()
    pb.value = 1
    pb.update()

    pb.height = 0
    pb.update()
    
    status.value = "Download Finished!"
    status.update()
    
    status2.value = f"Images saved in: {images_folder}"
    status2.size = 20
    status2.update()
    
    return_container.height = 0
    return_container.update()
    return_button.height = 50
    return_button.update()
    return

def DownloadView(page, params):
    
    email, password, link, browser = params['params'].split('&')
    link = link.replace("|","/")
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
        
    space = lambda height = 0 : ft.Container(height = height,
                                             padding = 0,
                                             margin = 0)
    
    global search_thread
    search_thread = Thread(target = search_images,
                           args = (email, password, link, browser))
    search_thread.start()
    
    download_thread = Thread(target = download_images)
    download_thread.start()
    
    def end_download(e):
        page.go("/")
                        
    title = ft.Text(
        "Pinterest Downloader!", 
        size = 100,
        color = ft.colors.BLUE,
        weight = ft.FontWeight.BOLD,
        font_family = "RubikIso")
    
    global return_button
    return_button = ft.ElevatedButton(
        content = ft.Text("Return!",
            color = ft.colors.BLUE,
            weight = ft.FontWeight.BOLD, 
            size = 25,
            font_family = "RubikIso"),
        height = 0,
        on_click = end_download)
    
    global return_container
    return_container = ft.Container(height = 50)
    
    global status
    status = ft.Text(
        "Initializing...",
        size = 50,
        color = ft.colors.GREEN,
        font_family = "RubikIso")
    
    global status2
    status2 = ft.Text(
        size = 0,
        color = ft.colors.WHITE)
    
    global pb
    pb = ft.ProgressBar(
        width = page.width / 1.2,
        height = 20,
        color = ft.colors.WHITE)
    
    global images
    images = ft.Row(
        expand = True, 
        alignment = ft.MainAxisAlignment.CENTER)
    
    col1 = ft.Column(
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            status, status2, pb,
        ]
    )
    
    col2 = ft.Column(
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            return_button, return_container
        ]
    )
        
    return ft.View(
        "/search",
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        controls = [
            title,
            col1,
            space(15),
            images,
            space(15),
            col2,
        ]
    )