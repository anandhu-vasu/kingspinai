from chatterbot.response_selection import get_random_response

CHATBOT_OPTIONS={
    "read_only": True,                  
    "logic_adapters": [
        {
            'import_path': 'chatbot.core.logic.Ingenious',
        },
    ],
    "preprocessors": [
        "chatterbot.preprocessors.clean_whitespace",
        "chatbot.core.preprocessors.corrector"
    ],
    "storage_adapter":'chatbot.core.storage.DjangoStorageAdapter',
}
