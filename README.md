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
1.  **Wake Word:** The terminal will actively listen using energy limits to discard silence. Say **"Hey assistant"** (or press ENTER in the terminal manually).
2.  **Listener:** The program will acknowledge the wake word and prompt you to start speaking. 
3.  **Interaction:** Ask your question aloud (e.g., *"What were the key takeaways from the most recent SpaceX launch?"* or *"What does the PDF say about project deadlines?"*). Let silence indicate you've finished speaking.
4.  **Processing:** It will transcribe via Whisper, Search the web AND your local PDF collection, summarize via GPT, and then dynamically speak the combined answer out of your speakers.

---

## 💻 Tech Stack & Tools

This assistant utilizes a heavily optimized combination of libraries to ensure purely generalized ARM functionality without heavy compiled C-binding requirements:

- **OpenAI APIs**: Built via `openai` python library. Uses `whisper-1` for highly accurate acoustic transcription, `gpt-4o-mini` for fast multi-context reasoning, `tts-1` (`alloy`) for conversational playback, and `text-embedding-3-small` for vectorizing local data.
- **Microphone Capture**: Powered by `PyAudio` (binding `PortAudio`/`ALSA` streams) and `SpeechRecognition` implementing smart silence-chunking thresholds.
- **Search (Internet)**: Live intelligence via the `duckduckgo-search` (DDGS) headless web API.
- **Search (Local PDF Vector RAG)**: Powered completely offline using `pypdf` for fast extraction and `numpy` dot-products for memory-safe Cosine Similarity generation, specifically optimized to avoid heavy vector-databases on Raspberry Pi microchip architectures.
- **Audio Output**: Synced entirely across OS audio drivers asynchronously utilizing `pygame`.
- **Command Line UI**: Driven by Textualize's `rich` library to draw aesthetic panels, spinners, and colors inside standard Bash terminals.
- **Environment Flow**: `python-dotenv` for encrypted, cross-platform local key management.

---

> **Built by Artificial Intelligence**  
> *This entire application, architecture, and documentation logic was generated exclusively through **Gemini 3.1 Pro**.*
