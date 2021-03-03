from chatterbot import ChatBot
from chatbot.core.corpus import TaggerLang

CHATBOT_OPTIONS={
    "read_only": True,                  
    "logic_adapters": [
        {
            "import_path": "chatterbot.logic.BestMatch",
            "response_selection_method": "chatterbot.response_selection.get_random_response",
            "default_response": "I am sorry, but I do not understand.",
            "maximum_similarity_threshold": 0.90
        },
    ],
    "tagger_language": TaggerLang("en_core_web_md"),
    "preprocessors": [
        "chatterbot.preprocessors.clean_whitespace",
        "chatbot.core.preprocessors.corrector"
    ],
    "storage_adapter":'chatbot.core.storage.DjangoStorageAdapter',
}

CHATBOT_NAME= "Kingspinai"

KingspinAI = ChatBot(
    name = CHATBOT_NAME,
    botkey = CHATBOT_NAME,
    **CHATBOT_OPTIONS
)