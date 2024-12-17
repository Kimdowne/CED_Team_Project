from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore


class embedder:
    def __init__(self, path, file_name, chunk_size):
        self.llm = ChatOpenAI(
            temperature=0.1,
        )

        embed_path = f"../{path}/embedding/"
        file_path = f"../{path}/{file_name}"
        cache_dir = LocalFileStore(f"{embed_path}")
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator="\n",
            chunk_size=chunk_size,
            chunk_overlap=80,
        )
        loader = TextLoader(f"{file_path}")
        docs =  loader.load_and_split(text_splitter=splitter)
        embeddings = OpenAIEmbeddings()

        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings,  cache_dir)
        self.vectorstore = FAISS.from_documents(docs, cached_embeddings)
        
    
    def get_retriever(self, message):
        retriever = self.vectorstore.as_retriever()

        def format_docs(docs):
            return '\n\n'.join([d.page_content for d in docs])
        result = retriever.get_relevant_documents(message)
        result = format_docs(result)

        #print(result)

        return result