import json

class Corpus:
    def load_from_dic(*dicts):
        for dic in dicts:
            corpus = dic["conversations"]
            categories = dic["categories"]
            name = dic["name"]
            yield corpus, categories, name
    def save_to_json(corpus,path="chatbot/core/data/data.json"):
        if not isinstance(corpus, str):
            corpus = json.dumps(corpus);

        with open(path, "w") as f: 
            f.write(corpus)

class TaggerLang:
    ISO_639_1 = ""
    def __init__(self,lang):
        TaggerLang.ISO_639_1 = lang