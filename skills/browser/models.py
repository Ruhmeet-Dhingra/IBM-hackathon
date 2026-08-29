from dataclasses import dataclass


@dataclass
class BrowserRequest:

    url: str | None = None

    query: str | None = None