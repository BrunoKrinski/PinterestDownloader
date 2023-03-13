import os
import time
import wget
import flet as ft
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

images_folder = f"C:\\Users\\{os.getlogin()}\\Pictures\\PinterestDownloader"

os.makedirs(images_folder, exist_ok=True)

def searching(email, password, link, page):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)

    driver.get('https://br.pinterest.com/')

    enter_path = '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div/div'
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()

    username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))

    username_field.clear()
    username_field.send_keys(email)   
    password_field.clear()
    password_field.send_keys(password)

    enter_path = '//*[@id="__PWS_ROOT__"]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button/div'
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enter_path))).click()

    time.sleep(10)
    global urls
    urls = []
    
    driver.get(link)

    time.sleep(10)
    scroll_times = 0
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        anchors = driver.find_elements(By.TAG_NAME, 'img')
        anchors = [anchor for anchor in anchors]

        for anchor in anchors:
            try:
                link = anchor.get_attribute('srcset')
                link = link.split(',')[-1].split(' ')[1]
                urls.append(link)
            except:
                continue 
        scroll_times += 1

        if scroll_times == 100:
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            else:
                last_height = new_height
                scroll_times = 0
        
        driver.execute_script('window.scrollBy(0, 25);')
    driver.quit()
    urls = list(set(urls))
    return len(urls)  

def downloading():
    for url in urls:
        #print(f'\nUrl: {url}')
        try:
            wget.download(url, out=images_folder)
        except:
            #print("\nCouldn't download!")
            continue
    return

def main(page: ft.Page):
    page.title = "Pinterest Downloader"
    page.window_width = 900
    page.window_height = 600
    page.window_resizable = False
    page.window_top = 100
    page.window_left = 250
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
    
    global playing
    global default_message
    playing = True
    default_message = ""
        
    song = ft.Audio(
        src="audios/song.mp3", autoplay=True, release_mode=ft.audio.ReleaseMode.LOOP, volume=1
    )
    page.overlay.append(song)
        
    email = ft.TextField(label='E-mail',autofocus=True)
    password = ft.TextField(label='Password',password=True, can_reveal_password=True)
    link = ft.TextField(label='Pinterest Playlist Link')
    
    def song_play(e):
        e.control.selected = not e.control.selected
        e.control.update()
        global playing
        if playing:
            song.pause()
        else:
            song.resume()
        playing = not playing
    
    play_icon = ft.IconButton(icon=ft.icons.MUSIC_NOTE_ROUNDED, 
                              selected_icon=ft.icons.MUSIC_OFF_ROUNDED,
                              icon_size=50, 
                              on_click=song_play)
    
    def close_banner(e):
        page.banner.open = False
        page.update()
    
    page.banner = ft.Banner(leading=ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.RED, size=40),
                            actions=[ft.TextButton(content=ft.Text('Close!', 
                                                                   size=15, 
                                                                   font_family="RubikIso", 
                                                                   color=ft.colors.WHITE), 
                                                   on_click=close_banner)
                                     ]
                            )
    
    def show_banner_click(e):
        page.banner.content = ft.Text(default_message, 
                                      color=ft.colors.RED,
                                      style=ft.TextThemeStyle.DISPLAY_LARGE,
                                      font_family="RubikIso",
                                      size=25)
        page.banner.open = True
        page.update()
    
    def start_searching(e):
        global pinterest_email
        global pinterest_password
        global pinterest_link
        global default_message
        
        if email.value == "" or password.value == "" or link.value == "":
            default_message = "Please Fill All Fields!"
            show_banner_click(e)
            return
            
        if validators.email(email.value):        
            if validators.url(link.value):
                pinterest_email = email.value
                pinterest_password = password.value
                pinterest_link = link.value
                page.go('/searching')
            else:
                default_message = "Invalid Link Format!"
                show_banner_click(e)
                return
        else:
            default_message = "Invalid E-mail Format!"
            show_banner_click(e)
            return
    
    start_button = ft.ElevatedButton(content=ft.Text('Start!', 
                                                     size=30, 
                                                     font_family="RubikIso", 
                                                     color=ft.colors.WHITE), 
                                     on_click=start_searching)
    
    def to_home(e):
        page.go('/')

    def open_repo(e):
        page.launch_url('https://github.com/BrunoKrinski')
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(route='/',
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    controls = [ft.Text('Pinterest Downloader!',
                                        style=ft.TextThemeStyle.DISPLAY_LARGE,
                                        font_family="RubikIso"),
                                email,
                                password,
                                link,
                                start_button,
                                play_icon,
                                ft.Text('Developed by War Machine!',
                                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                                        font_family="RubikIso",
                                        color=ft.colors.RED),
                                ft.TextButton(content=ft.Text('GitHub!',
                                                              size=15,
                                                              font_family="RubikIso",
                                                              color=ft.colors.WHITE),
                                              on_click=open_repo),
                                                                  
                    ]
                )
            )
        if page.route == "/searching":
            page.views.append(
                ft.View(route="/searching",
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        controls = [
                            ft.Text('Searching for images...',
                                    style=ft.TextThemeStyle.DISPLAY_LARGE,
                                    font_family="RubikIso",),
                            ft.ProgressBar(width=600, 
                                           color=ft.colors.BLUE_900, 
                                           bgcolor="#eeeeee", 
                                           bar_height=10,
                                           tooltip='Searching for images!'),
                            play_icon
                        ]
                )
            )
        if page.route == "/download":
            page.views.append(
                ft.View(route="/download",
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        controls = [
                            ft.Text('Downloading images...',
                                    style=ft.TextThemeStyle.DISPLAY_LARGE,
                                    font_family="RubikIso",),
                            ft.ProgressBar(width=600, 
                                           color=ft.colors.BLUE_900, 
                                           bgcolor="#eeeeee", 
                                           bar_height=10,
                                           tooltip='Downloading images!'),
                            play_icon
                        ]
                )
            )
        if page.route == "/default":
            page.views.append(
                ft.View(route="/default",
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        controls = [
                            ft.Text("Download Finished!",
                                    style=ft.TextThemeStyle.DISPLAY_LARGE,
                                    font_family="RubikIso",),
                            ft.Text(f"Images saved on: {images_folder}",
                                    style=ft.TextThemeStyle.DISPLAY_LARGE,
                                    size=15),
                            ft.ElevatedButton(content=ft.Text('Return!',size=30,font_family="RubikIso"), 
                                              on_click=to_home),
                            play_icon
                        ]
                )
            )
        page.update()

        if page.route == "/":
            email.value = ""
            password.value = ""
            link.value = ""
        
        if page.route == "/download":
            downloading()
            page.go('/default')

        if page.route == "/searching":
            urls_size = searching(pinterest_email, pinterest_password, pinterest_link, page)
            urls_size = 10
            if urls_size > 0:
                page.go('/download')
            else:
                page.go('/default')
                

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)