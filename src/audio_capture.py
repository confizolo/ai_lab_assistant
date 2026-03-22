import pyaudio
import numpy as np
import speech_recognition as sr
import wave
from rich.console import Console

console = Console()

def listen_for_wakeword(wakeword="hey assistant", trigger_event=None):
    """
    Listens continuously on the microphone until the custom wakeword is detected.
    Uses Google's free STT for quick flexible custom wake words on ARM devices.
    If trigger_event is provided and set, it activates instantly.
    Returns True when detected.
    """
    console.print(f"[dim]Loading '{wakeword}' wake word listener...[/dim]")
    
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 400
    
    with sr.Microphone(sample_rate=16000) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        console.print(f"👂 [bold green]Listening for wake word: '{wakeword}' or [ENTER]...[/bold green]")
        
        while True:
            # Check parallel trigger
            if trigger_event and trigger_event.is_set():
                console.print("\n[bold magenta]⚡ Keybinder manually triggered![/bold magenta]")
                trigger_event.clear()
                return True
                
            try:
                # Listen in short bursts
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                # Use generalized free google transcription to catch the wake word
                text = r.recognize_google(audio).lower()
                
                # Check if 'assistant' or 'hey assistant' is in the text
                if "assistant" in text or wakeword in text:
                    console.print(f"\n[bold magenta]🎯 Wake word heard! (Matched '{text}')[/bold magenta]")
                    return True
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                console.print(f"[red]STT Service Error: {e}[/red]")
                import time
                time.sleep(2)
                continue

def record_query(output_filename="query.wav"):
    """
    Records audio using SpeechRecognition until silence is detected,
    then saves it to standard wav.
    """
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        console.print("[dim]Adjusting for ambient noise...[/dim]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        console.print("🎙️  [bold cyan]Listening for your query... (Speak now)[/bold cyan]")
        
        try:
            audio_data = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            console.print("[yellow]No speech detected, returning to standby.[/yellow]")
            return None
        
    console.print("[dim]Recording finished, processing...[/dim]")
    with open(output_filename, "wb") as f:
        f.write(audio_data.get_wav_data())
    return output_filename
