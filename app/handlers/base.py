from abc import ABC, abstractmethod

class MessageHandler(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        pass
    
    @abstractmethod
    def handle(self, message: str) -> str:
        pass