from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API = os.getenv("GEMINI_APIKEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")


class PreprocessingData: 
    """
    Input: class nhận đầu vào là document ngừoi dùng (hoặc context) + một câu prompt về thông tin của document  
    Ouput : context liên quan đến câu prompt  
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model = "gemini-1.5-pro-latest", temperature=0.2, api_key = GEMINI_API) 
        self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", api_key = GEMINI_API)

        self.preprocessing_template = """
        Based on the following information: : {context} 
        Please summarize the text if it is longer than 4000 words and the text is summarized at least 3000 words. 
        Convert the above text into {language} language.
        Returns text as JSON as follows: 
        {{
        "Original language" : paragraph with original language, 
        "Translated language" ": paragraph with translated language 
        }}
        """




        self.preprocessing_prompt = ChatPromptTemplate.from_template(self.preprocessing_template)


    
    def preprocessing(self, document: str, language: str):
        full_chain = (
            self.preprocessing_prompt
            | self.llm 
            | StrOutputParser()
        )
        result = full_chain.invoke({"context": document, "language": language})
        
        return result 
    

    def user_prompting(self, document: str, user_prompt: str): 
        text_spliter = CharacterTextSplitter(
             separator="\n",
            chunk_size=512,
            chunk_overlap=50,
            length_function=len
        )

        chunks = text_spliter.split_text(document)
        db = FAISS.from_documents(
            chunks, 
            self.embedding
        )

        retriever = db.as_retriever(search_kwargs={"k": 5})
        results = retriever.get_relevant_documents(user_prompt)
        return results



if __name__ == "__main__":
    
    from pprint import pprint
    import time

    def test_preprocessing(document: str, language: str):
        start = time.time()

        preprocessor = PreprocessingData()
        result = preprocessor.preprocessing(document, language)
        print(result)

        print(f"Time elapsed: {time.time() - start}")

    def test_user_prompting(document: str, user_prompt: str):
        start = time.time()

        preprocessor = PreprocessingData()
        result = preprocessor.user_prompting(document, user_prompt)
        pprint(result)

        print(f"Time elapsed: {time.time() - start}")    


    document = "The history of the United States, a country in North America, began with the arrival of Native Americans in the United States from before 15,000 BC. Numerous indigenous cultures formed, and many disappeared in the 1500s. The arrival of Christopher Columbus in 1492 started the European colonization of the Americas. Most colonies were formed after 1600, and the United States was the first nation whose most distant origins are fully recorded. By the 1760s, the thirteen British colonies contained 2.5 million people and were established along the Atlantic Coast east of the Appalachian Mountains. After defeating France, the British government imposed a series of taxes, including the Stamp Act of 1765, rejecting the colonists' constitutional argument that new taxes needed their approval. Resistance to these taxes, especially the Boston Tea Party in 1773, led to Parliament issuing punitive laws designed to end self-government. Armed conflict began in Massachusetts in 1775."
    language = "fr"
    user_prompt = "Summarize the text above if it is longer than 4000 words and the text is summarized at least 3000 words. Convert the above text into French language."

    test_preprocessing(document, language)
    test_user_prompting(document, user_prompt)