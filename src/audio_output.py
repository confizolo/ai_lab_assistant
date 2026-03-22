import os
from openai import OpenAI
from rich.console import Console

console = Console()

# Hide pygame welcome module output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

client = OpenAI()

def speak_text(text, output_file="response.mp3"):
    """
    Converts text to speech using OpenAI TTS and plays it directly out of the OS speakers.
    """
    console.print("[dim]Generating speech audio via OpenAI TTS...[/dim]")
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(output_file)
        
        console.print(f"\n[bold yellow]🗣️  Assistant says:[/bold yellow] [italic]\"{text}\"[/italic]\n")
        
        # Play using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
    except Exception as e:
        console.print(f"[bold red]Text-to-Speech playback failed: {e}[/bold red]")
