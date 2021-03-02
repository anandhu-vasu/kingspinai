from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.comparisons import LevenshteinDistance
class SpaCy_en_md:
    ISO_639_1 = 'en_core_web_md'
    ISO_639 = 'en_core_web_md'
    ENGLISH_NAME = 'en_core_web_md'

KingspinAI = ChatBot(
    name = 'KingspinAI',
    read_only = True,                  
    logic_adapters = [
        {   
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": LevenshteinDistance,
            "response_selection_method": get_random_response,
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        },],
    tagger_language=SpaCy_en_md,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        "core.preprocessors.message_preprocess"
    ],
    storage_adapter='chatterbot.storage.DjangoStorageAdapter',
)