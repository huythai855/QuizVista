from dotenv import load_dotenv
from langchain import hub 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os 
import pke 
import nltk
import string 
import traceback

load_dotenv()
GEMINI_API = os.getenv("GEMINI_APIKEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

class MatchingConfig: 
    gemini_model_name = "gemini-1.5-pro-latest"


class MatchingGenerator: 

    def __init__(self): 
        self.llm = ChatGoogleGenerativeAI(model = MatchingConfig.gemini_model_name, temperature=0.2, api_key = GEMINI_API)
        self.template = """Based on the following passage: 
        {context}
        Let's define the definition of keywords : {keyword}
        Return the JSON data containing the keywords and its definition as follow: 
        {{

            "Keyword1": "definition1", 

            "Keyword2" : "definition2", 

            ............................................, 

        }}
        """ 
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.llm 

    


    def generate(self, context: str, num_question: int = 4): 

        keywords = self.get_keyword(context, num_question)

        full_chain = (
            self.prompt 
            | self.llm 
            | StrOutputParser()
        )   
        result = full_chain.invoke({"context": context, "keyword": keywords})
        clean_text = result.replace("```json", "").replace("```", "").strip()

        return eval(clean_text)


    def get_keyword(self, context: str, num_question: int = 4): 
        """
        trích xuất keyword từ context 
        """
        output = []

        try: 
            extractor = pke.unsupervised.MultipartiteRank()
            extractor.load_document(input=context, language='en')
            pos = {'VERB', 'NOUN', 'PROPN'}

            extractor.candidate_selection(pos=pos)
            extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
            keyphrases = extractor.get_n_best(n= num_question)

            for val in keyphrases: 
                output.append(val[0])

        except : 
            output = []
            traceback.print_exc()

        return output
    

if __name__ == '__main__': 
    import time 
    from pprint import pprint

    def test(context: str): 
        start = time.time()


        matching = MatchingGenerator()
        result =  matching.generate(context)
        print(f"Time : {time.time() - start}")
        pprint(result)
        pass 

    context = """The history of the United States is what happened in the past in the United States, a country in North America. 
            Native Americans lived in the Americas for thousands of years. English people in 1607 went to the place now called Jamestown, Virginia. Other European settlers went to the colonies, mostly from England and later Great Britain. France, Spain, and the Netherlands also colonized North America. In 1775, a war between the thirteen colonies and Britain began when the colonists were upset over changes in British policies. On July 4, 1776, rebel leaders made the United States Declaration of Independence. 
            They won the Revolutionary War and started a new country. They signed the Constitution in 1787 and the Bill of Rights in 1791. George Washington, who had led the war, became its first president. During the 19th century, the United States gained much more land in the West and began to become industrialized. In 1861, several states in the South left the United States to start a new country called the Confederate States of America. This caused the American Civil War"""

    test(context)