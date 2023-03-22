import flet as ft
import validators

def HomeView(page, params):
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
    
    space = lambda height = 0 : ft.Container(height = height,
                                             padding = 0,
                                             margin = 0)
    
    def close_banner(e):
        page.banner.open = False
        page.update()
    
    page.banner = ft.Banner(
        leading = ft.Icon(
            ft.icons.WARNING_ROUNDED, 
            color = ft.colors.RED, 
            size = 50),
        actions = [
            ft.TextButton(
                content = ft.Text('Close!', 
                    size = 25, 
                    font_family = "RubikIso", 
                    color = ft.colors.BLUE), 
                on_click = close_banner)
            ])
    
    def show_banner_click(e, message):
        page.banner.content = ft.Text(
            message, 
            color = ft.colors.RED,
            size = 50,
            font_family = "RubikIso")
        page.banner.open = True
        page.update()
    
    def start_download(e):       
        
        if email_text.value == "" or password_text.value == "" or link_text.value == "":
            message = "Please Fill All Fields!"
            show_banner_click(e, message)
            return
    
        if browser_selector.value is None:
            message = "Please Select Your Browser!"
            show_banner_click(e, message)
            return
        
        if validators.email(email_text.value):        
            if validators.url(link_text.value):
                url = link_text.value.replace("/","|")
                message = f"{email_text.value}&{password_text.value}&{url}&{browser_selector.value}"
                page.go(f"/download/{message}")
                return
            else:
                message = "Invalid Link Format!"
                show_banner_click(e, message)
                return
        else:
            message = "Invalid E-mail Format!"
            show_banner_click(e, message)
            return
                    
    title = ft.Text(
        "Pinterest Downloader!", 
        size = 100,
        color = ft.colors.BLUE,
        weight = ft.FontWeight.BOLD,
        font_family = "RubikIso")
    
    developed = ft.Text(
        "Developed by War Machine!",
        color = ft.colors.RED,
        weight = ft.FontWeight.BOLD, 
        size = 25,
        font_family = "RubikIso")
    
    start_button = ft.ElevatedButton(
        content = ft.Text("Start!",
            color = ft.colors.BLUE,
            weight = ft.FontWeight.BOLD, 
            size = 50,
            font_family = "RubikIso"),
        on_click = start_download)
    
    label_style = ft.TextStyle(
        color = ft.colors.BLUE,
        size = 15)
    
    email_text = ft.TextField(
        label = "Pinterest E-mail!",
        label_style = label_style,
        autofocus = True,
        hint_text = "example@domain.com",
        cursor_color = ft.colors.WHITE,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        text_size = 20,
        expand = True,
        focused_border_width = 5)
    
    password_text = ft.TextField(
        label = "Pinterest Password!",
        label_style = label_style,
        hint_text = "Your Password",
        cursor_color = ft.colors.WHITE,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        text_size = 20,
        password = True,
        can_reveal_password=True,
        expand = True,
        focused_border_width = 5)
        
    row1 = ft.Row(
        controls = [
            email_text,
            password_text
        ]
    )
    
    link_text = ft.TextField(
        label = "Pinterest Link!",
        label_style = label_style,
        hint_text = "https://br.pinterest.com/romipins/cute-cats/",
        cursor_color = ft.colors.WHITE,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        text_size = 20,
        expand = True,
        focused_border_width = 5)
    
    browser_selector = ft.Dropdown(
        width = 500,
        
        label = "Select Your Browser!",
        label_style = label_style,
        options=[
            ft.dropdown.Option("Chrome"),
            ft.dropdown.Option("Firefox"),
        ],
        content_padding = 23,
        text_size = 20,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        focused_border_width = 5,
        #focused_border_width = 100,
    )      
    
    row2 = ft.Row(
        controls = [
            link_text,
            browser_selector
        ]
    )
    
    input_data = ft.Column(
        controls = [
            row1, row2
        ]
    )
    
    github_button = ft.TextButton(
        content = ft.Text("GitHub!", 
            size = 20,
            font_family = "RubikIso",
            color = ft.colors.WHITE),
        on_click = lambda _ : 
            page.launch_url('https://github.com/BrunoKrinski'))
    
    infos = ft.Column(
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            developed, github_button
        ]
    )
        
    return ft.View(
        "/",
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        controls = [
            title,
            input_data,
            start_button,
            infos
        ]
    )