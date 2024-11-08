from transformers import BertTokenizer, BertModel,  AutoModelForSeq2SeqLM, AutoTokenizer
from utils import preprocessing_input_qa
from scipy.spatial.distance import cosine


class ShortAnsConfig: 
    qa_generation: str = "potsawee/t5-large-generation-squad-QuestionAnswer"
    scoring: str = "bert-base-uncased"
    cache_dir = "server/quizgen/cache/"

class ShortAnsGenerator:

    def __init__(self, device = None):

        self.device = device 
        self._init_qa_model()
        self._init_scoring_model()
        
    def _init_qa_model(self): 
        self.qa_tokenizer = AutoTokenizer.from_pretrained(ShortAnsConfig.qa_generation, cache_dir = ShortAnsConfig.cache_dir)
        self.qa_model = AutoModelForSeq2SeqLM.from_pretrained(ShortAnsConfig.qa_generation, cache_dir = ShortAnsConfig.cache_dir).to(self.device)

    def _init_scoring_model(self):
        self.scoring_tokenizer = BertTokenizer.from_pretrained(ShortAnsConfig.scoring)
        self.scoring_model = BertModel.from_pretrained(ShortAnsConfig.scoring).to(self.device)

    def generate(self, context: str, num_question: int):
        """
        sinh ra câu hỏi - câu trả lời short-ans
        """

        qa_input_ids = preprocessing_input_qa(self.qa_tokenizer, context, self.device)
        max_sampling = int(num_question * 2)

        num_valid_quest = 0 
        questions = []
        for _ in range(max_sampling): 
            
            # quest gen 
            qa_output = self.qa_model.generate(input_ids=qa_input_ids, max_new_tokens= 128, do_sample= True) 
            ques_ans = self.qa_tokenizer.decode(qa_output[0], skip_special_tokens=False)
            ques_ans = ques_ans.replace(self.qa_tokenizer.eos_token, "").replace(self.qa_tokenizer.pad_token, "").split(self.qa_tokenizer.sep_token)

            if len(ques_ans) != 2: continue 
            quest, ans = ques_ans[0].strip(), ques_ans[1].strip()
            questions.append({
                "question": quest,
                "answer": ans
            })
            num_valid_quest += 1
            if num_valid_quest == num_question: break 

        return questions
    
    def get_sentence_embedding(self, sentence: str): 
        """
        tính embedding của một câu 
        """
        input = self.scoring_tokenizer(sentence, return_tensors="pt")
        output = self.scoring_model(**input)

        cls_embedding = output.last_hidden_state[:, 0, :].squeeze()
        return cls_embedding


    def scoring(self, sentence1: str, sentence2: str): 
        """
        Chấm điểm câu trả lời sử dụng cosine similarity
        """
        embedd1 = self.scoring(sentence1)
        embedd2 = self.scoring(sentence2)

        cosine_score = 1 - cosine(embedd1.detach().numpy(), embedd2.detach().numpy())

        return cosine_score >= 0.6 
    

if __name__ == '__main__': 
    from pprint import pprint 
    import time

    def test(context: str): 
        print("Test shortans generation")
        start = time.time()
        shortans_gen = ShortAnsGenerator()

        shortans = shortans_gen.generate(context, 5)

        pprint(shortans)
        end = time.time()
        print("Time: ", end - start)
        print("Pass Test scoring")

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""

    test(context)

