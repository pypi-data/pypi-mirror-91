"""PDF report rendering utilities."""
from abc import ABC, abstractmethod
import logging

import requests

log = logging.getLogger(__name__)


class PDFRenderer(ABC):
    """Abstract PDF renderer."""

    @abstractmethod
    def render(url: str) -> bytes:
        """Render a PDF document content from given URL."""
        pass

    @staticmethod
    def create_renderer_from_config(config):
        """PDF renderer instance factory."""
        if config.BROWSERLESS_API_URL and config.BROWSERLESS_API_TOKEN:
            log.info("Creating Browserless.io PDF renderer")
            return BrowserlessPDFRenderer(
                config.BROWSERLESS_API_URL, config.BROWSERLESS_API_TOKEN
            )

        log.info("No PDF renderer available")
        return None


class BrowserlessPDFRenderer(PDFRenderer):
    """Browserless IO implementation."""

    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token

    def render(self, url: str):
        headers = {
            "Cache-Control": "no-cache",
        }
        params = {"token": self.api_token}
        data = {
            "url": url,
            "options": {
                "displayHeaderFooter": True,
                "printBackground": False,
                "format": "A4",
            },
        }

        # Request server
        r = requests.post(self.api_url, headers=headers, params=params, json=data)
        r.raise_for_status()
        return r.content
