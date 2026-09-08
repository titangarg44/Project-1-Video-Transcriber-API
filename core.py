import os
from moviepy import VideoFileClip
from faster_whisper import WhisperModel

def extract_audio(video_path, output_audio_path="temp_audio.wav"):
    """
    Step 1: Extract audio track from target video.
    AI audio models prefer uncompressed .wav files at 16kHz or 24kHz.
    """
    print(f"[+] Extracting audio from {video_path}...")
    clip = VideoFileClip(video_path)
    
    # Write audio file out to disk explicitly at 16000Hz mono channel
    clip.audio.write_audiofile(output_audio_path, fps=16000, nbytes=2, ffmpeg_params=["-ac", "1"])
    clip.close()
    print(f"[✓] Audio successfully written to {output_audio_path}")
    return output_audio_path

def transcribe_audio(audio_path, model_size="base"):
    """
    Step 2: Run local AI model engine on the extracted file.
    'base' model balances performance and resource consumption on general laptops.
    """
    print(f"[+] Loading Whisper Model ({model_size})...")
    # Change device to "cuda" if your computer has an NVIDIA GPU
    model = WhisperModel(model_size, device="cpu", compute_type="float32")
    
    print("[+] Processing audio speech-to-text pipeline...")
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    print(f"[✓] Detected language: '{info.language}' with confidence {info.language_probability:.2f}")
    
    transcript_data = []
    for segment in segments:
        # Pull raw text alongside explicit timing metrics
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        transcript_data.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
        
    return transcript_data

if __name__ == "__main__":
    # Test execution block: Put a sample video named 'test.mp4' in this directory
    TEST_VIDEO = "test.mp4"
    
    if os.path.exists(TEST_VIDEO):
        extracted_audio = extract_audio(TEST_VIDEO)
        results = transcribe_audio(extracted_audio)
        print("\n[✓] Pipeline complete! Data array structure ready for Phase 2.")
    else:
        print(f"[!] Please place a video file named '{TEST_VIDEO}' in this directory to run tests.")

def format_timestamp(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

def generate_srt(transcript_data: list, output_filename: str = "subtitles.srt"):
    with open(output_filename, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(transcript_data, start=1):
            start_str = format_timestamp(segment["start"])
            end_str = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{idx}\n{start_str} --> {end_str}\n{text}\n\n")
            
    print(f"[✓] Subtitle file generated: {output_filename}")
    return output_filename