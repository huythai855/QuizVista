from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils import preprocessing_input_qa, preprocessing_input_distract
import re 
# model config 
class QAConfig: 
    qa_generation: str = "potsawee/t5-large-generation-squad-QuestionAnswer"
    distractor_generation: str = "potsawee/t5-large-generation-race-Distractor"
    cache_dir = "server/quizgen/cache/"


# MCQ questgen model 
class MCQGenerator: 
    """
    This class is used to generate multiple choice questions from a given context and question using the fine-tuned model
    which is public on HuggingFace 
    """
    def __init__(self, device = None, qa_model: AutoModelForSeq2SeqLM = None, qa_tokenizer: AutoTokenizer = None, 
                        dist_model: AutoModelForSeq2SeqLM = None, dist_tokenizer: AutoTokenizer = None):

        self.device = device 
        if qa_model and qa_tokenizer and dist_model and dist_tokenizer:
            self.qa_model = qa_model
            self.qa_tokenizer = qa_tokenizer
            self.dist_model = dist_model
            self.dist_tokenizer = dist_tokenizer
        else: 
            self._init_qa_model()
    

    def _init_qa_model(self): 
        self.qa_tokenizer = AutoTokenizer.from_pretrained(QAConfig.qa_generation, cache_dir=QAConfig.cache_dir)
        self.qa_model = AutoModelForSeq2SeqLM.from_pretrained(QAConfig.qa_generation, cache_dir=QAConfig.cache_dir ).to(self.device)
        self.dist_tokenizer = AutoTokenizer.from_pretrained(QAConfig.distractor_generation, cache_dir=QAConfig.cache_dir)
        self.dist_model = AutoModelForSeq2SeqLM.from_pretrained(QAConfig.distractor_generation, cache_dir=QAConfig.cache_dir).to(self.device)



    def generate(self, context: str, num_question: int):

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

            # distractor gen 

            distract_input_ids = preprocessing_input_distract(self.dist_tokenizer, context, quest, ans, self.device)

            distract_output = self.dist_model.generate(input_ids=distract_input_ids, max_new_tokens= 128, do_sample= True)

            distraction = self.dist_tokenizer.decode(distract_output[0], skip_special_tokens=False)
            distraction = distraction.replace(self.dist_tokenizer.eos_token, "").replace(self.dist_tokenizer.pad_token, "")
            distractors = re.sub("<extra\S+>", self.dist_tokenizer.sep_token, distraction)
            distractors = [y.strip() for y in distractors.split(self.dist_tokenizer.sep_token)]
            
            options = [ans] + distractors

            while len(options) < 4: 
                options.append(options[0])


            questions.append({
                "question": quest,
                "options": options,
                "answer": ans
            })
            num_valid_quest += 1
            if num_valid_quest == num_question: break
        return questions
    

if __name__ == "__main__": 
    import time

    def test(context: str):
        start = time.time()
        mcq = MCQGenerator()
        questions = mcq.question_generation_sampling(context, 10)
        print(questions)
        end = time.time()
        print(f"Time elapsed: {end - start}")

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""


    test(context)
    
    

    








