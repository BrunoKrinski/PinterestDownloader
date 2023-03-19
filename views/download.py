import os
import time
import wget
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

def download_images():
    
    images_folder = f"C:\\Users\\{os.getlogin()}\\Pictures\\PinterestDownloader"
    os.makedirs(images_folder, exist_ok=True)
    
    global pb
    global status
    global images
    global return_button
    global return_container
    
    with open("tmp/urls.txt", 'r') as urls_file:
        urls = urls_file.readlines()
        for i, url in enumerate(urls):           
            url = url.replace('\n','')
            #print(f'\nUrl: {url}')
            win = True
            try:
                wget.download(url, out = images_folder)
            except:
                win = False
                print("\nCouldn't download!")
                continue
            if win:
                image_name = url.split('/')[-1]
                
                if len(images.controls) > 5:
                    images.controls.pop(0)
                
                images.controls.append(
                    ft.Image(
                        src = images_folder + '/' + image_name,
                        width = 200,
                        height = 400,
                        fit = ft.ImageFit.COVER,
                        repeat = ft.ImageRepeat.NO_REPEAT,
                        border_radius = ft.border_radius.all(10)))
                images.update()
            pb.value = i / len(urls)
            pb.update()
        pb.value = 1
        pb.update()
        
        status.value = "Download Finished!"
        status.update()
        
        return_container.height = 0
        return_container.update()
        return_button.height = 50
        return_button.update()
    return


def DownloadView(page, params):
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
        
    space = lambda height = 0 : ft.Container(height = height,
                                             padding = 0,
                                             margin = 0)
    
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
        "Downloading Images...",
        size = 50,
        color = ft.colors.BLUE,
        font_family = "RubikIso")
    
    global pb
    pb = ft.ProgressBar(
        width = page.width / 1.2,
        height = 20,
        color = ft.colors.WHITE)
    
    global images
    images = ft.Row(
        expand = 1, 
        wrap = False, 
        scroll = "always",
        #auto_scroll = True.
        alignment = ft.MainAxisAlignment.CENTER)
    
    return ft.View(
        "/search",
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            title,
            #space(5),    
            status,
            #space(5),    
            pb,
            #space(5),
            images,
            #space(5),
            return_button,
            return_container,
        ]
    )