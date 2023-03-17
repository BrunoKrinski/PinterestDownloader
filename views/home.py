import flet as ft

def HomeView(page, params):
    
    page.fonts = {
        "RubikIso": "fonts/RubikIso-Regular.ttf"
    }
    
    space = lambda height = 0 : ft.Container(height = height)
            
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
        font_family = "RubikIso"))
    
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
        text_size = 20)
    
    password_text = ft.TextField(
        label = "Pinterest Password!",
        label_style = label_style,
        hint_text = "Your Password",
        cursor_color = ft.colors.WHITE,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        text_size = 20,
        password = True,
        can_reveal_password=True)
    
    link_text = ft.TextField(
        label = "Pinterest Link!",
        label_style = label_style,
        hint_text = "https://br.pinterest.com/romipins/cute-cats/",
        cursor_color = ft.colors.WHITE,
        border_color = ft.colors.WHITE,
        focused_color = ft.colors.WHITE,
        text_size = 20,
        password = True)
    
    github_button = ft.TextButton(
        content = ft.Text("GitHub!", 
            size = 20,
            font_family = "RubikIso",
            color = ft.colors.WHITE),
        on_click = lambda _ : 
            page.launch_url('https://github.com/BrunoKrinski'))      
    
    return ft.View(
        "/",
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        controls = [
            title,
            space(25),
            email_text,
            space(5),
            password_text,
            space(5),
            link_text,
            space(5),
            start_button,
            developed,
            github_button,
        ]
    )