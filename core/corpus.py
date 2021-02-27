import json

class Corpus:
    def load_from_dic(*dicts):
            for dic in dicts:
                corpus = dic["conversations"]
                categories = dic["categories"]
                name = dic["name"]
                yield corpus, categories, name
    def save_to_json(corpus,path="core/data/data.json"):
        if not isinstance(corpus, str):
            corpus = json.dumps(corpus);

        with open(path, "w") as f: 
            f.write(corpus)
