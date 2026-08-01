# Project-1-Video-Transcriber-API
An asynchronous FastAPI microservice that extracts audio from uploaded videos, generates precision timestamped transcripts using OpenAI's Whisper model (faster-whisper), and automatically exports .srt subtitle files.

# AI Dubbing Pipeline - Phase 1: Video Audio Extractor & Transcriber

An asynchronous FastAPI microservice that extracts audio from uploaded video files and generates timestamped transcripts alongside `.srt` subtitle files using `faster-whisper` and `FFmpeg`.

## 🚀 Features
- **Video Processing:** Extracts audio track from uploaded `.mp4`, `.mkv`, or `.mov` files using MoviePy/FFmpeg.
- **AI Speech-to-Text:** Generates precision timestamped transcripts using OpenAI's Whisper model (`faster-whisper`).
- **Subtitle Export:** Automatically generates formatted `.srt` subtitle files.
- **REST API Interface:** Live interactive Swagger UI endpoint (`/docs`) for quick testing and integration.

## 📁 Repository Structure
```text
ai_dubber_p1/
├── .gitignore
├── requirements.txt
├── main.py
└── core.py
```

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed and FFmpeg available on your system path.

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-dubber-phase1.git
cd ai-dubber-phase1
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Server
```bash
python main.py
```
The server will start running locally at `http://127.0.0.1:8000`.

## 🧪 Usage & Testing

1. Open your browser and navigate to `http://127.0.0.1:8000/docs`.
2. Expand the `POST /transcribe` endpoint.
3. Click **Try it out**, upload a video file (`.mp4`), and click **Execute**.
4. The API will return a structured JSON response containing timestamps and text, and generate a `.srt` subtitle file directly in your project root directory.

## 📄 License
This project is open-source and available under the MIT License.
