import whisper
import ffmpeg
import os
import shutil

def extract_audio_from_video(video_path, output_audio_path="temp_audio.wav"):
    """
    Extracts the audio track from a video file using FFmpeg.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, format='wav', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        return output_audio_path
    except ffmpeg.Error as e:
        print("Error extracting audio:", e)
        return None

def move_video_to_generateImages(video_path):
    """
    Moves the video file to the backend/generateImages folder after transcription.
    """
    try:
        # Get the current directory (backend/transcribe)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Navigate to backend/generateImages folder
        target_dir = os.path.join(os.path.dirname(current_dir), "generateImages")
        
        # Create the target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Get the filename from the video path
        filename = os.path.basename(video_path)
        target_path = os.path.join(target_dir, filename)
        
        # Move the file
        shutil.move(video_path, target_path)
        print(f"✅ Video file moved to: {target_path}")
        
    except Exception as e:
        print(f"❌ Error moving video file: {e}")

def transcribe_video(video_path, model_name="base"):
    """
    Transcribes speech from a video using OpenAI Whisper.
    """
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    print(f"Extracting audio from {video_path} ...")
    audio_path = extract_audio_from_video(video_path)

    if not audio_path:
        print("Audio extraction failed.")
        return

    print("Transcribing...")
    result = model.transcribe(audio_path)

    text = result["text"].strip()
    print("\n✅ Transcription Complete:\n")
    print(text)

    # Optionally, save the text to a file
    output_file = os.path.splitext(video_path)[0] + "_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nTranscript saved to: {output_file}")
    
    # Clean up temporary audio file
    try:
        os.remove(audio_path)
        print("🧹 Cleaned up temporary audio file")
    except OSError:
        pass
    
    # Move the video file to backend/generateImages folder after transcription
    move_video_to_generateImages(video_path)
    
    return text

if __name__ == "__main__":
    video_file = input("Enter path to your video file: ").strip()
    transcribe_video(video_file, model_name="small")  # You can use "tiny", "base", "small", "medium", or "large"
