import flet as ft
import flet_route as ftr
from views.home import HomeView

def main(page: ft.Page):
    page.title = "Pinterest Downloader!"
    page.window_maximized = True
    
    app_routes = [
        ftr.path(url = "/",
                 clear = True,
                 view = HomeView)
    ]
    
    ftr.Routing(page = page, app_routes = app_routes)
    page.go(page.route)

ft.app(target=main)