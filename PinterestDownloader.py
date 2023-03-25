import flet as ft
import flet_route as ftr
from views.home import HomeView
from views.download import DownloadView

def main(page: ft.Page):
    page.theme_mode = "DARK"
    page.title = "Pinterest Downloader!"
    page.window_maximized = True
    page.window_movable = False
    page.window_resizable = False
    page.update()
    
    app_routes = [
        ftr.path(url = "/",
                 clear = True,
                 view = HomeView),
        ftr.path(url = "/download/:params",
                 clear = True,
                 view = DownloadView),        
    ]
        
    ftr.Routing(page = page, app_routes = app_routes)
    page.go(page.route)
        
ft.app(target=main)