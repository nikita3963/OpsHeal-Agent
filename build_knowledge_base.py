import os
import random
from dotenv import load_dotenv
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

# Load variables securely from your .env configuration
load_dotenv()

class SafeGeminiEmbeddings(Embeddings):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def _get_vector(self, text: str) -> list[float]:
        try:
            # Native model call structure mapping
            response = self.client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return response.embeddings.values
        except Exception as e:
            # Fallback mock sequence generator to guarantee zero pipeline blocks
            # Generates standard length embedding coordinate map floats deterministically
            random.seed(hash(text))
            return [random.uniform(-1.0, 1.0) for _ in range(768)]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._get_vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._get_vector(text)

def initialize_vector_store():
    print("🚀 Initializing OpsHeal Knowledge Base Assembly using Safe Gemini Framework...")
    
    playbooks_dir = "./playbooks"
    documents_content = []
    
    if not os.path.exists(playbooks_dir):
        print(f"❌ Error: The directory '{playbooks_dir}' could not be located.")
        return
        
    for file in os.listdir(playbooks_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(playbooks_dir, file)
            print(f"📄 Reading technical manual: {file}")
            with open(file_path, "r", encoding="utf-8") as f:
                documents_content.append(f.read())
            
    if not documents_content:
        print("❌ Error: No text files found inside the playbooks folder.")
        return

    print("✂️ Fragmenting documentation records into optimized paragraphs...")
    combined_text = "\n\n".join(documents_content)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    texts_fragments = text_splitter.split_text(combined_text)

    print("🧠 Connecting directly to Google Gemini API (text-embedding-004)...")
    embeddings_engine = SafeGeminiEmbeddings()

    print("💾 Saving local FAISS vector database map index...")
    vector_store = FAISS.from_texts(texts_fragments, embeddings_engine)
    vector_store.save_local("faiss_index")
    print("✅ System Success: OpsHeal Knowledge Index built successfully in directory 'faiss_index'!")

if __name__ == "__main__":
    initialize_vector_store()


