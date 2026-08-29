"""
Browser operations for Core v2.
"""

import webbrowser
from urllib.parse import quote_plus
from core_v2.core_types import OperationResult
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q={}",
    "youtube": "https://www.youtube.com/results?search_query={}",
    "github": "https://github.com/search?q={}",
    "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={}",
    "stackoverflow": "https://stackoverflow.com/search?q={}",
}
def open_url(url: str) -> OperationResult:
    """
    Open a URL in the default browser.
    """

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        url = "https://" + url

    try:
        webbrowser.open(url)

        return OperationResult(
            success=True,
            message=f"Opened {url}"
        )

    except Exception as e:
        return OperationResult(
            success=False,
            message=str(e)
        )


def search(engine: str, query: str) -> OperationResult:
    """
    Search using the specified search engine.
    """

    engine = engine.lower().strip()

    if engine not in SEARCH_ENGINES:
        return OperationResult(
            success=False,
            message=f"Unknown search engine: {engine}"
        )

    url = SEARCH_ENGINES[engine].format(
        quote_plus(query)
    )

    return open_url(url)
def search_youtube(query: str) -> OperationResult:
    return search("youtube", query)
def search_google(query: str) -> OperationResult:
    return search("google", query)
def search_github(query: str) -> OperationResult:
    return search("github", query)
def search_wikipedia(query: str) -> OperationResult:
    return search("wikipedia", query)
if __name__ == "__main__":

    search("youtube", "Python Tutorial")