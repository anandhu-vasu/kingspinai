from enum import Enum

class ConvoChannels(str, Enum):
    WEB = "Web"
    WHATSAPP = "Whatsapp"
    TELEGRAM = "Telegram"
    MESSENGER = "Messenger"
    
    def __str__(self) -> str:
        return self.value
