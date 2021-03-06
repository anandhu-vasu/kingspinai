from chatterbot import ChatBot
from chatbot.core.corpus import TaggerLang
from chatterbot.response_selection import get_random_response

CHATBOT_OPTIONS={
    "read_only": True,                  
    "logic_adapters": [
        {
            "import_path": "chatterbot.logic.BestMatch",
            "response_selection_method": get_random_response,
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
