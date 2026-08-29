from core_v2.browser import (
    open_url,
    search_google,
    
)


def open(url: str):
    return open_url(url)


def search(query: str):
    return search_google(query)


