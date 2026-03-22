import os
import warnings
from openai import OpenAI
from duckduckgo_search import DDGS
from rich.console import Console

console = Console()

# Filter annoying DDGS package rename warning
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

# Assumes OPENAI_API_KEY is set in the environment
client = OpenAI()

def transcribe_audio(audio_path):
    console.print("[dim]Transcribing audio via Whisper API...[/dim]")
    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language="en"
            )
        console.print(f"👤  [bold blue]User Query:[/bold blue] \"{transcription.text}\"")
        return transcription.text
    except Exception as e:
        console.print(f"[bold red]Transcription failed: {e}[/bold red]")
        return ""

def perform_web_search(query):
    console.print("[dim]Searching the web via DuckDuckGo...[/dim]")
    try:
        results = DDGS().text(query, max_results=3)
        context = ""
        count = 1
        for r in results:
            context += f"Source {count}: {r.get('title')}\nInfo: {r.get('body')}\n\n"
            count += 1
        return context
    except Exception as e:
        console.print(f"[red]Search failed: {e}[/red]")
        return "No web search data available."

def generate_research_summary(query, web_context, pdf_context=""):
    console.print("[dim]Generating concise research summary via GPT-4o-mini...[/dim]")
    system_prompt = (
        "You are an extremely helpful and concise AI voice assistant running in a lab. "
        "The user will ask you a question aloud. You are provided with retrieved text from local PDFs, as well as live web search context. "
        "Summarize the direct answer using 1-4 short sentences maximum. "
        "IMPORTANT: You MUST explicitly state your source aloud at the beginning of your answer! "
        "If using PDF context, start with 'According to the file [filename]...'. "
        "If using Web context, start with 'Based on a web search...'. "
        "If both, mention both! "
        "Do NOT use asterisks, markdown formatting, bullet points, complex code snippets, or URLs. "
        "Use natural conversational English meant for the ear, not the eye."
    )
    
    # Combine the context properly
    combined_context = ""
    if pdf_context:
        combined_context += f"LOCAL PDF CONTEXT:\n{pdf_context}\n"
    if web_context:
        combined_context += f"WEB SEARCH CONTEXT:\n{web_context}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}\n\n{combined_context}"}
            ],
            max_tokens=200,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        console.print(f"[bold red]GPT Generation failed: {e}[/bold red]")
        return "I encountered an error trying to generate a response."

def process_query(audio_path):
    """
    Pipeline to transcribe, search, and generate a response.
    """
    text_query = transcribe_audio(audio_path)
    if not text_query or len(text_query.strip()) < 5:
        return "I didn't quite catch that."
    
    # Search local PDFs (imported dynamically to avoid circular issues)
    from document_loader import get_relevant_pdf_context, KNOWLEDGE_BASE
    pdf_context = get_relevant_pdf_context(text_query, KNOWLEDGE_BASE)
    
    # Search Web
    web_context = perform_web_search(text_query)
    
    # Generate unified answer
    answer = generate_research_summary(text_query, web_context, pdf_context)
    return answer
