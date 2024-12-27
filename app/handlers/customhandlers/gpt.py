from ..base import MessageHandler
from ...services.gpt import get_assistant_response

class GPTHandler(MessageHandler):
    def can_handle(self, message: str) -> bool:
        return message.lower().startswith('gpt')
    
    def handle(self, message: str) -> str:
        cleaned_message = message.lower().replace('gpt', '').strip()
        return get_assistant_response(cleaned_message)