from chatterbot import utils
from chatterbot.trainers import Trainer
from chatbot.core.conversation import Statement
from chatbot.core.corpus import Corpus
from chatbot.core.exceptions import EmptyTrainingDataError

class SophisticatedTrainer(Trainer):
    def train(self, *corpus_data):
        dataset = self.chatbot.storage.dataset
        corpus_data = list(corpus_data)
        if dataset:
            corpus_data.extend(dataset)
        if not corpus_data:
            raise EmptyTrainingDataError()
        for corpus,categories,name in Corpus.load_from_dic(*corpus_data):
            statements_to_create = []

            for conversation_count, conversation in enumerate(corpus):
                if self.show_training_progress:
                    utils.print_progress_bar(
                        'Training ' + str(name),
                        conversation_count + 1,
                        len(corpus)
                    )
                
                for res in conversation["responses"]:
                    for stm in conversation["statements"]:
                        statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(stm)
                        response_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(res)

                        statement = Statement(
                            text=res,
                            search_text=response_search_text,
                            in_response_to=stm,
                            search_in_response_to=statement_search_text,
                            conversation='training',
                        )

                        statement.add_tags(*categories)

                        statement = self.get_preprocessed_statement(statement)

                        statements_to_create.append(statement)
            self.chatbot.storage.create_many(statements_to_create)



# x={
#     "name":""
#     "categories":[],
#     "conversations":[
#         {
#             "statements":[""],
#             "responses":[""]
#         }
#     ]
# }
