from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate
from config import VECTOR_DB_PATH, LLM_DEFAULT, LLM_FALLBACK
import os
import pickle

def get_llm(name):
    if name == "openai":
        return OpenAI(temperature=0)
    elif name == "ollama/mistral":
        return Ollama(model="mistral")
    raise ValueError("Unknown LLM")

# Robust prompt template for truthful multi-hop answers
QA_PROMPT_TEMPLATE = """
You are a careful and honest assistant answering questions based on multiple transcripts and policy documents.

Follow these instructions strictly:

1. If a person discusses a topic (e.g., mental health) more than once:
   - Always use the **most recent or strongest admission**, even if earlier parts of the document say the opposite.
   - Prioritize **specific self-disclosures** over vague general statements.

2. Always search the documents for **direct quotes** of the person speaking. Do not rely on general sentiment.

3. If a person says:
   - "I've got PTSD pretty bad" — that counts as a confirmed mental health condition.
   - Later statements like "I'm good" should not override earlier, more specific disclosures unless explicitly updated.

4. If the answer is "not mentioned" or "no concerns," check whether earlier or later in the documents a **contradictory disclosure** exists.

5. If the answer depends on recency, and timestamps or session dates are present, use those to resolve conflicts.

Format your answer like this:
✅ Final Answer:
[answer here]

🧾 Supporting Evidence:
"[exact quote]" — [document name]

🔍 Reasoning:
Explain how you resolved conflicting info, and why this quote was chosen.

Context information:
{context_str}

Query: {query_str}
Answer: """

def load_query_engine():
    llm = get_llm(LLM_DEFAULT)
    fallback_llm = get_llm(LLM_FALLBACK)

    try:
        # Check if index file exists
        index_path = os.path.join(VECTOR_DB_PATH, "index.pkl")
        if not os.path.exists(index_path):
            raise FileNotFoundError("No index found. Please upload documents and rebuild the index.")
            
        print("🔄 Loading existing index...")
        
        # Load the index from pickle file
        with open(index_path, 'rb') as f:
            index = pickle.load(f)
        
        print("✅ Index loaded successfully!")
        
        # Create custom prompt
        qa_prompt = PromptTemplate(QA_PROMPT_TEMPLATE)
        
        # Create query engine with aggressive retrieval settings
        query_engine = index.as_query_engine(
            llm=llm,
            similarity_top_k=10,  # Retrieve even more chunks
            response_mode="tree_summarize",  # Better for multi-document synthesis
            text_qa_template=qa_prompt,  # Use our robust prompt
            verbose=True
        )
        
        return query_engine
        
    except Exception as e:
        print(f"❗Error loading index: {e}")
        print("❗Creating fallback response...")
        
        # Create a helpful fallback response
        from llama_index.core import Document
        fallback_text = """
        No documents are currently indexed in the system. 
        
        To use this RAG assistant:
        1. Upload documents using the file uploader above
        2. Click "Rebuild Index with Uploaded Files"
        3. Then ask questions about your documents
        
        The system will then be able to answer questions based on your uploaded content.
        """
        fallback_doc = Document(text=fallback_text)
        index = VectorStoreIndex.from_documents([fallback_doc])
        return index.as_query_engine(llm=fallback_llm)