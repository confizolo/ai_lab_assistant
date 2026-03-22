import pyaudio
import numpy as np
import speech_recognition as sr
import wave

def listen_for_wakeword(wakeword="hey Assistant", trigger_event=None):
    """
    Listens continuously on the microphone until the custom wakeword is detected.
    Uses Google's free STT for quick flexible custom wake words on ARM devices.
    If trigger_event is provided and set, it activates instantly.
    Returns True when detected.
    """
    print(f"Loading '{wakeword}' wake word listener...", flush=True)
    
    r = sr.Recognizer()
    # Lower dynamic energy threshold to prevent waiting too long for silence
    r.dynamic_energy_threshold = True
    r.energy_threshold = 400
    
    with sr.Microphone(sample_rate=16000) as source:
        print("Adjusting for ambient noise...", flush=True)
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"\nListening for wake word: '{wakeword}' or Hotkey...", flush=True)
        
        while True:
            # Check parallel trigger
            if trigger_event and trigger_event.is_set():
                print("\n[DETECTED] Keybinder manually triggered!", flush=True)
                trigger_event.clear()
                return True
                
            try:
                # Listen in short bursts
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                # Use generalized free google transcription to catch the wake word
                text = r.recognize_google(audio).lower()
                
                # Check if 'Assistant' or 'hey Assistant' is in the text
                if "Assistant" in text or "slopper" in text or wakeword in text:
                    print(f"\n[DETECTED] Wake word heard! (Matched '{text}')", flush=True)
                    return True
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                # Speech was unintelligible, loop safely
                continue
            except sr.RequestError as e:
                print(f"Could not request results from STT service; {e}")
                # Fallback delay
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
        print("Adjusting for ambient noise...", flush=True)
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for your query...", flush=True)
        
        # We can add a simple beep here via print or pygame if desired
        try:
            # timeout=5s to initial timeout, phrase_time_limit=15s max question length
            audio_data = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("No speech detected.", flush=True)
            return None
        
    print("Recording finished.", flush=True)
    with open(output_filename, "wb") as f:
        f.write(audio_data.get_wav_data())
    return output_filename
