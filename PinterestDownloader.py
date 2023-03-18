import flet as ft
import flet_route as ftr
from views.home import HomeView
from views.search import SearchView
from views.download import DownloadView

def main(page: ft.Page):
    page.title = "Pinterest Downloader!"
    page.window_maximized = True
    
    app_routes = [
        ftr.path(url = "/",
                 clear = True,
                 view = HomeView),
        ftr.path(url = "/search/:params",
                 clear = True,
                 view = SearchView),
        #ftr.path(url = "/download",
        #         clear = True,
        #         view = DownloadView),        
    ]
        
    ftr.Routing(page = page, app_routes = app_routes)
    page.go(page.route)
        
ft.app(target=main)