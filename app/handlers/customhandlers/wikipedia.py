from ..base import MessageHandler
from ...services.wiki import get_wikipedia_content

class WikipediaHandler(MessageHandler):
    def can_handle(self, message: str) -> bool:
        return True  # fallback handler
    
    def handle(self, message: str) -> str:
        return get_wikipedia_content(message)