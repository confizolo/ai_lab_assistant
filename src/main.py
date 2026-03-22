import os
import sys
import threading
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

# Load secret variables from the specific .env file in the folder
load_dotenv()

# Validate API key before proceeding
if not os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY") == "sk-your-openai-api-key-here":
    console.print("[bold red]❌ Error:[/bold red] OPENAI_API_KEY is not set correctly in your .env file.")
    console.print("Please open the '.env' file in the voice_assistant folder and paste your key.")
    sys.exit(1)

from audio_capture import listen_for_wakeword, record_query
from research_agent import process_query
from audio_output import speak_text

def manual_input_thread_func(trigger_event):
    """Background thread that listens for an ENTER keypress in the terminal"""
    while True:
        try:
            sys.stdin.readline()
            trigger_event.set()
        except Exception:
            break

def run_assistant_loop():
    console.print(Panel.fit("[bold cyan]🔬 Lab Voice Assistant Started[/bold cyan]", border_style="cyan"))
    console.print("[dim]Ready and standing by.[/dim]")
    console.print("[yellow]Say 'hey slopper' or press [ENTER] in the terminal to ask a question.[/yellow]\n")
    
    # Setup hotkey event
    manual_trigger = threading.Event()
    
    # Start robust terminal keybinder thread
    input_thread = threading.Thread(target=manual_input_thread_func, args=(manual_trigger,), daemon=True)
    input_thread.start()
    
    while True:
        try:
            # 1. Wait for wake word OR the hotkey event
            listen_for_wakeword("hey slopper", trigger_event=manual_trigger)
            
            # 2. Record the user's question
            audio_file = record_query("current_query.wav")
            
            if audio_file:
                # 3. Transcribe, Search, and Synthesize
                answer = process_query(audio_file)
                
                # 4. Speak the answer back directly out of the speakers
                speak_text(answer, "current_response.mp3")
            
            console.print("\n[dim]" + "━"*50 + "[/dim]\n")
            
            # Clear manual trigger just in case
            manual_trigger.clear()
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Shutting down assistant. Goodbye![/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred in MAIN loop: {e}[/bold red]")
            try:
                speak_text("Sorry, I encountered an internal error.")
            except:
                pass

if __name__ == "__main__":
    run_assistant_loop()
