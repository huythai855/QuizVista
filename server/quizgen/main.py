from bool_generator import BoolGenerator
from matching_generator import MatchingGenerator
from mcq_generator import MCQGenerator
from shortans_generator import ShortAnsGenerator
from fib_generator import FiB_Generator

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,  T5ForConditionalGeneration, T5Tokenizer, BertTokenizer, BertModel


class QuizGenConfig: 
    # bool model 
    bool_model: str = "ramsrigouthamg/t5_boolean_questions"
    bool_tokenizer: str = "t5-base"

    # short ans and fib scoring model 
    ans_scoring: str = "bert-base-uncased"
    # matching model 
    matching_model = "gemini-1.5-pro-latest"

    # shortans and distractor generation model
    qa_generation: str = "potsawee/t5-large-generation-squad-QuestionAnswer"
    distractor_generation: str = "potsawee/t5-large-generation-race-Distractor"

    cache_dir = "server/quizgen/cache/"


class QuizGenerator: 
    """
    Đây là main class dùng để tương tác với các class còn lại, khởi tạo mô hình, nhận input là context 
    và số lượng câu hỏi + số lượng câu hỏi được sinh ra 
    """
    def __init__(self, device = None): 
        self.device = device
        self._init_model()
        
    def _init_model(self): 
        # init bool model 
        self.bool_model = T5ForConditionalGeneration.from_pretrained(QuizGenConfig.bool_model,cache_dir = QuizGenConfig.cache_dir).to(self.device)
        self.bool_tokenizer = T5Tokenizer.from_pretrained(QuizGenConfig.bool_tokenizer, cache_dir = QuizGenConfig.cache_dir)

        # fib model and ans 
        self.scoring_tokenizer = BertTokenizer.from_pretrained(QuizGenConfig.ans_scoring, cache_dir=QuizGenConfig.cache_dir)
        self.scoring_model = BertModel.from_pretrained(QuizGenConfig.ans_scoring, cache_dir=QuizGenConfig.cache_dir).to(self.device)

        # mcq model and and 
        self.qa_tokenizer = AutoTokenizer.from_pretrained(QuizGenConfig.qa_generation, cache_dir=QuizGenConfig.cache_dir)
        self.qa_model = AutoModelForSeq2SeqLM.from_pretrained(QuizGenConfig.qa_generation, cache_dir=QuizGenConfig.cache_dir ).to(self.device)
        self.dist_tokenizer = AutoTokenizer.from_pretrained(QuizGenConfig.distractor_generation, cache_dir=QuizGenConfig.cache_dir)
        self.dist_model = AutoModelForSeq2SeqLM.from_pretrained(QuizGenConfig.distractor_generation, cache_dir=QuizGenConfig.cache_dir).to(self.device)


    def generate_one_type(self, type: str, context: str, num_question: int): 
        """
        Sinh ra câu hỏi dựa trên loại câu hỏi cần sinh 
        """
        if type == "bool": 
            generator = BoolGenerator(device=self.device, bool_model=self.bool_model, bool_tokenizer=self.bool_tokenizer)
            return generator.generate(context, num_question)
        elif type == "mcq": 
            generator = MCQGenerator(device=self.device, qa_model=self.qa_model, qa_tokenizer=self.qa_tokenizer, 
                        dist_model=self.dist_model, dist_tokenizer=self.dist_tokenizer)
            return generator.generate(context, num_question)
        elif type == "shortans": 
            generator = ShortAnsGenerator(device=self.device, qa_model=self.qa_model, qa_tokenizer=self.qa_tokenizer, 
                        scoring_model=self.scoring_model, scoring_tokenizer=self.scoring_tokenizer)
            return generator.generate(context, num_question)
        elif type == "fib": 
            generator = FiB_Generator(device=self.device, scoring_model=self.scoring_model, scoring_tokenizer=self.scoring_tokenizer)
            return generator.generate(context, num_question)
        elif type == "matching": 
            generator = MatchingGenerator()
            return generator.generate(context, num_question)
        else: 
            raise ValueError("Invalid type of question")
        
    def generate_multiple_type(self, types: dict, context: str): 
        """
        Sinh ra câu hỏi từ nhiều loại câu hỏi khác nhau 
        """
        questions = []
        for type in types.keys(): 
            questions.extend(self.generate_one_type(type, context, types[type]))
        return questions
        
if __name__ == '__main__': 

    import time 
    from pprint import pprint 


    def test_one_type(context: str, num_question: int, type: str): 
        start = time.time()
        generator = QuizGenerator()
        questions = generator.generate_one_type(type, context, num_question)
        print(f"Time: {time.time() - start}")
        pprint(questions)

    def test_multiple_type(context: str):
        start = time.time()
        generator = QuizGenerator()
        questions = generator.generate_multiple_type({
            "mcq": 2,
            "bool": 2,
            "shortans": 2,
            "fib": 2,
            "matching": 2
        }, context)
        print(f"Time: {time.time() - start}")
        pprint(questions)

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""
    
    test_one_type(context, 5, "matching")


    pass 