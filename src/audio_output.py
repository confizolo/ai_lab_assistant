import os
from openai import OpenAI

# Hide pygame welcome module output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

client = OpenAI()

def speak_text(text, output_file="response.mp3"):
    """
    Converts text to speech using OpenAI TTS and plays it directly out of the OS speakers.
    """
    print("Generating speech via OpenAI TTS...", flush=True)
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy", # Voices: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        response.stream_to_file(output_file)
        
        print(f"\n🗣️ Assistant says: \"{text}\"\n", flush=True)
        
        # Play using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Keep process alive while playing
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"Text-to-Speech playback failed: {e}", flush=True)
