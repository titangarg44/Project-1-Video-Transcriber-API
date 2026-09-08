from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

# Import the functions you just tested in core.py
from core import extract_audio, transcribe_audio, generate_srt

app = FastAPI(title="AI Dubbing Pipeline - Phase 1")

@app.post("/transcribe")
async def process_video(file: UploadFile = File(...)):
    """
    API Endpoint: Receives a video file, extracts audio, 
    and returns timestamped transcription data.
    """
    # 1. Ensure the uploaded file is actually a video
    if not file.filename.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a video file.")

    # 2. Save the uploaded stream temporarily to disk
    temp_video_path = f"temp_{file.filename}"
    try:
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Run your core engineering pipeline
        audio_path = extract_audio(temp_video_path)
        transcript_data = transcribe_audio(audio_path)
        srt_path = generate_srt(transcript_data, f"{file.filename}.srt")
        
        # 4. Clean up the temporary files so you don't clog up your server storage
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # 5. Return the clean structural JSON array
        return JSONResponse(content={
            "filename": file.filename,
            "status": "success",
            "data": transcript_data
        })

    except Exception as e:
        # If anything crashes, clean up files and raise a proper server error
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)