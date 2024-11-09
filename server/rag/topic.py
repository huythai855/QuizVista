from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import wikipedia as wiki 
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import bs4
import os 
from dotenv import load_dotenv

load_dotenv()
GEMINI_API = os.getenv("GEMINI_APIKEY")

class TopicDataBase:
    """
    Class này init topic database chứa các bài viết và lưu trữ nó dưới dạng vector Database 
    """

    def __init__(self): 
        self.data_path = 'books'
        self.database_path = "vectorstores/db_faiss"

        wiki_title_filepath = "topic_base.txt"
        with open(wiki_title_filepath, 'r') as file: 
            self.topic_title = [line.strip() for line in file if line.strip()]

        self.vector_db = self.building_database()
    

    def wiki_article_crawler(self): 
        """:
        Load thông tin từ trong title 
        """

        web_paths = []
        for title in self.topic_title: 
            web_paths.append(f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")

        web_loader = WebBaseLoader(
            web_path= web_paths,
             bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(class_="mw-body-content")
            ),
        )

        web_docs = web_loader.load()

        for doc, path in zip(web_docs, web_paths):
            doc.metadata = {"source": path}

        return web_docs

    def book_crawler(self): 
        """
        Load thông tin từ trong sách 
        """
        book_loader = DirectoryLoader(self.data_path, glob=".pdf", loader_cls=PyPDFLoader)
        book_docs = book_loader.load()

        for doc in book_docs:
            doc.metadata = {"source": os.path.basename(doc.metadata.get("file_path", ""))}
        return book_docs
    
    def building_database(self):
        """
        xây dựng vectordatabase 
        """
        book_docs = self.book_crawler()
        web_docs = self.wiki_article_crawler()
        docs = book_docs + web_docs

        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 512, chunk_overlap = 50)
        chunks = text_splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata = {"source": chunk.metadata.get("source")}

        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",  google_api_key = GEMINI_API)

        vector_db = FAISS.from_documents(
            chunks, 
            embedding_model, 
        )
        vector_db.save_local(self.database_path)

        return vector_db
    
    def search(self, query: str): 
        """
        tìm kiếm thông tin từ query 
        """
        results = self.vector_db.similarity_search(query, k=5)
        for result in results:
            print(f"Result: {result.page_content}")
            print(f"Source: {result.metadata['source']}\n")
        
        return results








class TopicExtractor: 
    """
    class này sử dụng để trích xuất dữ liệu và tìm kiếm dữ liệu phù hợp với topic đầu vào ()
    input : 
        - short prompt (topic)
    output : 
        - thông tin được lấy ra từ topic 

    """


    def __init__(self): 
        pass 
    

    def download_dataset(self): 
        pass 


    def extract_information(self, keyword): 
        pass 

