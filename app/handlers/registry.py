from typing import List
from .base import MessageHandler
from app.handlers.customhandlers.gpt import GPTHandler
from app.handlers.customhandlers.wikipedia import WikipediaHandler

class HandlerRegistry:
    def __init__(self):
        self.handlers: List[MessageHandler] = [
            GPTHandler(),
            WikipediaHandler()
        ]
    
    def get_handler(self, message: str) -> MessageHandler:
        for handler in self.handlers:
            if handler.can_handle(message):
                return handler
        return WikipediaHandler()  # default handler