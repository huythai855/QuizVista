from transformers import T5Tokenizer, T5ForConditionalGeneration
import random 
from utils import beamsearch_encoding

class BoolConfig: 
    bool_model: str = "ramsrigouthamg/t5_boolean_questions"
    bool_tokenizer: str = "t5-base"


class BoolGenerator: 

    def __init__(self, device = None): 
        self.devce = device 
        pass 


    def _init_model(self): 
        self.bool_model = T5ForConditionalGeneration.from_pretrained(BoolConfig.bool_model).to(self.device)
        self.bool_tokenizer = T5Tokenizer.from_pretrained(BoolConfig.bool_tokenizer)


    def random_choice(self): 
        return bool(random.choice([0, 1]))

    def generate(self, context: str, num_question: int = 4): 

        



        pass 


    

