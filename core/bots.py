from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
class SpaCy_en_md:
    ISO_639_1 = 'en_core_web_md'
    ISO_639 = 'en_core_web_md'
    ENGLISH_NAME = 'en_core_web_md'

KingspinAI = ChatBot(
    name = 'KingspinAI',
    read_only = False,                  
    logic_adapters = ["chatterbot.logic.BestMatch",
        {   
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'i honestly have no idea how to respond to that',
            'maximum_similarity_threshold': 0.9
        },],                 
    storage_adapter = "chatterbot.storage.SQLStorageAdapter",
    tagger_language=SpaCy_en_md,
    database_uri='sqlite:///db.sqlite3',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        "core.preprocessors.message_preprocess"
    ],
    response_selection_method=get_random_response

)