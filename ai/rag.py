import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv

# Ensure API key is loaded
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
INDEX_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "index.json")

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Splits text into smaller chunks."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def get_embedding(text: str) -> list[float]:
    """Gets the embedding vector for a given text."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values

def get_query_embedding(text: str) -> list[float]:
    """Gets the embedding vector for a search query."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values

def index_knowledge_base():
    """Reads files in knowledge_base, generates embeddings, and saves to index.json."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        
    index_data = []
    
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                chunks = chunk_text(content)
                for chunk in chunks:
                    if chunk.strip():
                        embedding = get_embedding(chunk)
                        index_data.append({
                            "file": filename,
                            "text": chunk,
                            "embedding": embedding
                        })
                print(f"Indexed {filename}")
            except Exception as e:
                print(f"Failed to read {filename}: {e}")
                
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f)
    print("Knowledge base indexing complete.")

def search_knowledge_base(query: str, top_k: int = 3) -> str:
    """Searches the indexed knowledge base and returns relevant context."""
    if not os.path.exists(INDEX_FILE):
        return "No knowledge base index found. Please add notes and run the indexer."
        
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_data = json.load(f)
        
    if not index_data:
        return "Knowledge base is empty."
        
    query_emb = np.array(get_query_embedding(query))
    
    # Calculate cosine similarity
    scored_chunks = []
    for item in index_data:
        doc_emb = np.array(item["embedding"])
        sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
        scored_chunks.append((sim, item))
        
    # Sort by similarity descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Take top K results
    top_results = [item for sim, item in scored_chunks[:top_k] if sim > 0.4] 
    
    if not top_results:
        return "No relevant information found in your notes."
        
    context = ""
    for res in top_results:
        context += f"[Source: {res['file']}]\n{res['text']}\n\n"
        
    return context.strip()

def answer_from_context(query: str, context: str) -> str:
    """Uses Gemini to answer the user's query based ONLY on the retrieved context."""
    if context in ["Knowledge base is empty.", "No knowledge base index found. Please add notes and run the indexer.", "No relevant information found in your notes."]:
        return "I couldn't find any information about that in your private notes."
        
    prompt = f"""
You are ROV, a smart and secure voice assistant.
Answer the user's question based strictly on the provided context from their private knowledge base.
If the answer is not in the context, politely say that you don't have information about it in the notes.
Keep your answer concise and suitable for spoken voice output (1-3 sentences).

Context:
{context}

Question:
{query}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

if __name__ == "__main__":
    index_knowledge_base()
