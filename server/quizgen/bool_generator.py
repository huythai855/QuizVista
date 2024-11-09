from transformers import T5Tokenizer, T5ForConditionalGeneration
import random 
from utils import beamsearch_encoding, greedysearch_encoding, preprocessing_input_bool, sentence_tokenize

class BoolConfig: 
    bool_model: str = "ramsrigouthamg/t5_boolean_questions"
    bool_tokenizer: str = "t5-base"
    cache_dir = "server/quizgen/cache/"


class BoolGenerator: 

    def __init__(self, device = None, bool_model: T5ForConditionalGeneration = None, bool_tokenizer: T5Tokenizer = None): 
        self.devce = device 
        if bool_model and bool_tokenizer: 
            self.bool_model = bool_model
            self.bool_tokenizer = bool_tokenizer
        else: 
            self._init_model()


    def _init_model(self): 
        self.bool_model = T5ForConditionalGeneration.from_pretrained(BoolConfig.bool_model,cache_dir = BoolConfig.cache_dir).to(self.device)
        self.bool_tokenizer = T5Tokenizer.from_pretrained(BoolConfig.bool_tokenizer, cache_dir = BoolConfig.cache_dir)


    def random_choice(self): 
        return bool(random.choice([0, 1]))

    def generate(self, context: str, num_question: int = 4): 

        valid_sentences = sentence_tokenize(context)

        if len(valid_sentences) * 2 < num_question: 
            raise ValueError("Not enough valid sentences to generate questions")
        
        questions = []
        for i in range(num_question): 
            if i < len(valid_sentences):
                context = valid_sentences[i]
                answer = self.random_choice()
                input_ids, att_mask = preprocessing_input_bool(self.bool_tokenizer, context, self.device, answer)
                question = greedysearch_encoding(input_ids, att_mask, self.bool_model, self.bool_tokenizer)

                questions.append({
                    "question": question,
                    "answer": answer
                })

            elif i < len(valid_sentences) * 2: 
                context = valid_sentences[i % len(valid_sentences)] + ' ' + valid_sentences[(i + 1) % len(valid_sentences)]
                answer = self.random_choice()
                input_ids, att_mask = preprocessing_input_bool(self.bool_tokenizer, context, self.device, answer)
                question = greedysearch_encoding(input_ids, att_mask, self.bool_model, self.bool_tokenizer)

                questions.append({
                    "question": question,
                    "answer": answer
                })
        return questions 


    
if __name__ == '__main__': 
    from pprint import pprint 
    import time 

    def test(context: str):
        start = time.time()
        generator = BoolGenerator()
        questions = generator.generate(context)
        print(f"Time elapsed: {time.time() - start}")
        pprint(questions)

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""

    test(context)
    