import sys
import os
import subprocess
import tempfile
import argparse
from pathlib import Path

# ============================================================
# CONFIGURATION — edit these two lines to match your setup
# ============================================================

# Folder containing your input .mp4 video file(s)
INPUT_DIR = r"C:\Users\Mihir\Videos\w13 WIR.mp4"

# Folder where the transcript .txt file will be saved
OUTPUT_DIR = r"C:\Users\Mihir\Videos"

# ============================================================


def extract_audio(video_path: str, audio_path: str) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")


def transcribe(video_path: str, output_dir: str, model_size: str = "base") -> str:
    import whisper

    video_path = os.path.abspath(video_path)
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    os.makedirs(output_dir, exist_ok=True)

    stem = Path(video_path).stem
    output_path = os.path.join(output_dir, f"{stem}.txt")

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name

    try:
        print("Extracting audio...")
        extract_audio(video_path, audio_path)

        print("Transcribing (this may take a while for large files)...")
        result = model.transcribe(audio_path, verbose=False)
        transcript = result["text"].strip()
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
        f.write("\n")

    print(f"Transcript saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Transcribe an MP4 video to text using Whisper.")
    parser.add_argument(
        "video",
        nargs="?",
        help="Path to the video file. If omitted, scans INPUT_DIR for the first .mp4 file.",
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size. Larger = more accurate but slower.",
    )
    parser.add_argument(
        "--output-dir",
        default=OUTPUT_DIR,
        help=f"Directory for transcript output (default: {OUTPUT_DIR})",
    )
    args = parser.parse_args()

    if not args.model:
        models = ["tiny", "small", "medium", "large"]
        print("Select a Whisper model:")
        for i, m in enumerate(models, 1):
            print(f"  {i}. {m}")
        while True:
            choice = input("Enter number (1-4): ").strip()
            if choice in {"1", "2", "3", "4"}:
                args.model = models[int(choice) - 1]
                break
            print("Please enter 1, 2, 3, or 4.")

    if args.video:
        video_path = args.video
    else:
        input_path = Path(INPUT_DIR)
        if input_path.is_file():
            video_path = str(input_path)
        else:
            candidates = list(input_path.glob("*.mp4"))
            if not candidates:
                print(f"No .mp4 files found in {INPUT_DIR}")
                sys.exit(1)
            video_path = str(candidates[0])
        print(f"No video specified — using: {video_path}")

    transcribe(video_path, args.output_dir, args.model)


if __name__ == "__main__":
    main()
