import pke 
from transformers import BertTokenizer, BertModel
from flashtext import KeywordProcessor
import pke.unsupervised
from utils import sentence_tokenize
from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
import string
import traceback 
import re 

class FiBConfig:
    cache_dir = "server/quizgen/cache/"
    scoring: str = "bert-base-uncased"


class FiB_Generator: 

    def __init__(self, device = None): 
        self.device = device
        self._init_scoring_model()

    
    def _init_scoring_model(self):
        self.scoring_tokenizer = BertTokenizer.from_pretrained(FiBConfig.scoring, cache_dir=FiBConfig.cache_dir)
        self.scoring_model = BertModel.from_pretrained(FiBConfig.scoring, cache_dir=FiBConfig.cache_dir).to(self.device)
    
    def generate(self, context: str, num_question: int = 4): 
        """
        sinh câu hỏi dạng fill-in-blank 
        """
        keywords = self.get_keyword(context, num_question)
        key_sentences = self.get_sentence(keywords, context)
        processed = []
        questions = []
        blank_token = "<blank>"
        for key in key_sentences: 
            if len(key_sentences[key]) > 0: 
                sent = key_sentences[key][0]

                insensitive_hippo = re.compile(re.escape(key), re.IGNORECASE)
                no_of_replacements =  len(re.findall(re.escape(key), sent, re.IGNORECASE))
                line = insensitive_hippo.sub(blank_token, sent)

                if key_sentences[key][0] not in processed and no_of_replacements < 2: 
                    questions.append({
                        "question": line, 
                        "answer": key
                    })
                    processed.append(key_sentences[key][0])
                    if len(questions) == num_question : break 

        return questions
    

    def get_keyword(self, context: str, num_question: int = 4): 
        """
        trích xuất keyword từ context 
        """
        output = []

        try: 
            extractor = pke.unsupervised.MultipartiteRank()
            extractor.load_document(input=context, language='en')
            pos = {'VERB', 'NOUN', 'PROPN'}

            stoplist = list(stopwords.words('english'))
            stoplist += list(string.punctuation)
            stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']

            extractor.candidate_selection(pos=pos, stoplist=stoplist)
            extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
            keyphrases = extractor.get_n_best(n= num_question * 2)

            for val in keyphrases: 
                output.append(val[0])

        except : 
            output = []
            traceback.print_exc()

        return output


    def get_sentence(keywords: list, context: str): 
        """
        trả về câu dài nhất chứa keyword 
        """
        keyword_processor = KeywordProcessor()
        sentences = sentence_tokenize(context)
        key_sentences = {}

        for word in keywords: 
            key_sentences[word] = []
            keyword_processor.add_keyword(word)

        for sentence in sentences: 
            key_founds = keyword_processor.extract_keywords(sentence)
            for key in key_founds: 
                key_sentences[key].append(sentence)

        for key in key_sentences.keys(): 
            values = key_sentences[key]
            values = sorted(values, key=len, reverse=True)
            key_sentences[key] = values[0]

        return key_sentences

    def scoring(self, question: str, answer1: str, answer2: str): 
        """
        Chấm điểm câu trả lời sử dụng cosine similarity
        """
        sentences1 = question.replace("<blank>", answer1)
        sentences2 = question.replace("<blank>", answer2)

        embedd1 = self.get_sentence_embedding(sentences1)
        embedd2 = self.get_sentence_embedding(sentences2)

        cosine_score = 1 - cosine(embedd1.detach().numpy(), embedd2.detach().numpy())

        return cosine_score >= 0.6

    def get_sentence_embedding(self, sentence: str): 
        """
        tính embedding của một câu 
        """
        input = self.scoring_tokenizer(sentence, return_tensors="pt")
        output = self.scoring_model(**input)

        cls_embedding = output.last_hidden_state[:, 0, :].squeeze()
        return cls_embedding
    

if __name__ == '__main__':

    import time 
    from pprint import pprint


    def test(context: str): 
        print("Test FiB generation")
        start = time.time()
        fib_gen = FiB_Generator()

        fib = fib_gen.generate(context, 5)

        pprint(fib)
        print("Time: ", time.time() - start)

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""

    test(context)