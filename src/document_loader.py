import os
import glob
import logging
from pypdf import PdfReader
from openai import OpenAI
import numpy as np
from rich.console import Console

console = Console()

# Suppress annoying pypdf formatting warnings
logging.getLogger("pypdf").setLevel(logging.ERROR)

client = OpenAI()

def load_and_chunk_pdfs(directory="data", chunk_size=600):
    chunks = []
    if not os.path.exists(directory):
        os.makedirs(directory)
        return chunks
        
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    if not pdf_files:
        return chunks
        
    for file in pdf_files:
        try:
            reader = PdfReader(file)
            filename = os.path.basename(file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
                    
            # Split text into chunks
            words = text.split()
            current_chunk = []
            current_len = 0
            
            for word in words:
                current_chunk.append(word)
                current_len += len(word) + 1
                
                if current_len >= chunk_size:
                    chunks.append({"source": filename, "text": " ".join(current_chunk)})
                    current_chunk = []
                    current_len = 0
            
            if current_chunk:
                chunks.append({"source": filename, "text": " ".join(current_chunk)})
                
        except Exception as e:
            console.print(f"[bold red]Error reading {file}: {e}[/bold red]")
            
    return chunks

def build_knowledge_base():
    """
    Loads all PDFs, extracts chunks, and pre-computes embeddings.
    """
    chunks = load_and_chunk_pdfs()
    
    if not chunks:
        console.print("[dim]No local PDFs found in data/ folder.[/dim]")
        return []
        
    console.print(f"📚 [bold green]Generating vector embeddings for {len(chunks)} local PDF chunks...[/bold green]")
    
    # Process embeddings in batches
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [c["text"] for c in batch]
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        for j, res in enumerate(response.data):
            batch[j]["embedding"] = res.embedding
            
    return chunks

def get_relevant_pdf_context(query, knowledge_base, top_k=2):
    """
    Returns the top_k most similar chunks of text as a string.
    """
    if not knowledge_base:
        return ""
        
    console.print("[dim]Searching local PDF Knowledge Base...[/dim]")
    
    query_res = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    query_emb = np.array(query_res.data[0].embedding)
    
    similarities = []
    for chunk in knowledge_base:
        chunk_emb = np.array(chunk["embedding"])
        sim = np.dot(query_emb, chunk_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(chunk_emb))
        similarities.append((sim, chunk))
        
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    context_str = ""
    for sim, chunk in similarities[:top_k]:
        context_str += f"[From PDF: {chunk['source']}]: {chunk['text']}\n\n"
        
    return context_str

KNOWLEDGE_BASE = build_knowledge_base()
