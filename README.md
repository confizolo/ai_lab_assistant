# 🎙️ Voice-Activated Research Assistant

A completely lab-ready, hands-free assistant. It constantly listens for a wake word, processes spoken questions, performs real-time internet research using DuckDuckGo, and answers you concisely aloud using the OpenAI GPT-4 + TTS framework. 

It is designed to run seamlessly on both macOS and Raspberry Pi hardware.

---

## 🛠️ Installation & Setup

### 1. Audio Dependencies
This project requires system-level audio dependencies to listen to your microphone and play the HTTP TTS streams exactly.

**For MacOS (Apple Silicon & Intel):**
```bash
brew install portaudio
```
*(Pygame audio handling happens via built-in Mac drivers, so no extra output libraries are strictly required on MacOS)*

**For Raspberry Pi (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio flac
sudo apt install libsdl2-mixer-2.0-0  # Required for pygame audio mixing
```

### 2. Python Environment Setup
Navigate into the `voice_assistant` directory:
```bash
cd voice_assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```
*(If you haven't frozen dependencies yet, run `pip install pyaudio openai duckduckgo-search pygame openwakeword SpeechRecognition soundfile`)*

### 3. Set OpenAI key
The Assistant processes logic and voices via OpenAI's cloud API (Whisper for STT, GPT-4o-mini for reasoning, TTS-1 for speaking).
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

---

## 🚀 How to Run

Activate the environment, connect your microphone (or Pi Camera Mic/USB Mic on Raspberry Pi), and run:
```bash
cd voice_assistant
source venv/bin/activate
python3 src/main.py
```

### Flow of Execution:
1.  **Wake Word:** The terminal will show it is running the `openwakeword` loop. Say **"Hey Jarvis"**.
2.  **Listener:** The program will acknowledge the wake word and print `Listening for your query...`
3.  **Interaction:** Ask your question aloud (e.g., *"What were the key takeaways from the most recent SpaceX launch?"*) Let silence indicate you've finished speaking.
4.  **Processing:** It will transcribe via Whisper, Search the web, summarize via GPT, and then dynamically speak the answer out of your speakers.

---

## 🔧 Architecture & Modules

*   `audio_capture.py`: Orchestrates the `openwakeword` ONNX models and `SpeechRecognition`'s silence-detection algorithms to handle the exact recording limits of the microphone seamlessly.
*   `research_agent.py`: Bridges the audio transcription (`whisper-1`) string directly into the DuckDuckGo Search API, and then summarizes the web-context directly via a low-latency GPT model.
*   `audio_output.py`: Converts text directly into high-fidelity voice using `alloy` via `tts-1` model and plays back seamlessly without relying on `afplay` (MacOS specific) so the exact same repository works gracefully on a Raspberry Pi. 
*   `main.py`: The unbreakable loop that catches errors, plays alert tones, and stitches it all together.

*(Note: openwakeword processes strictly offline on-device; only the specific question query gets sent to the cloud, saving massive bandwidth and cost!)*
