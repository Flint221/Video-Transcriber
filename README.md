# Video Transcriber

A Python script that transcribes MP4 video files to text using OpenAI Whisper, running entirely locally on your machine — no API keys or internet connection required after setup.

---

## Requirements

- Windows 10/11 (x64 Intel/AMD — **not ARM**)
- Python 3.11 or 3.12 (x64) — [download here](https://www.python.org/downloads/)
- ffmpeg — [download here](https://ffmpeg.org/download.html)
- ~2GB free disk space for the Whisper model

---

## Step 1 — Install Python

Download and install **Python 3.12 (64-bit)** from [python.org](https://www.python.org/downloads/).

During installation, check the box that says **"Add Python to PATH"**.

Verify it installed correctly by opening a terminal and running:

```
python --version
```

You should see something like `Python 3.12.x`.

---

## Step 2 — Install ffmpeg

ffmpeg is used to extract audio from your video file before transcription.

1. Go to [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and download the Windows build (the "gyan.dev" release is recommended).
2. Extract the zip file to a permanent location, e.g. `C:\ffmpeg`.
3. Add ffmpeg to your PATH:
   - Open **Start**, search for **"Edit the system environment variables"**
   - Click **Environment Variables**
   - Under **System variables**, select **Path** and click **Edit**
   - Click **New** and add the path to the `bin` folder, e.g. `C:\ffmpeg\bin`
   - Click OK on all dialogs

Verify ffmpeg is working by opening a new terminal and running:

```
ffmpeg -version
```

---

## Step 3 — Download the project

Clone or download this repository to your machine.

Using git:
```
git clone https://github.com/your-username/Video-Transcriber.git
cd Video-Transcriber
```

Or download the ZIP from GitHub and extract it.

---

## Step 4 — Install Python dependencies

Open a terminal in the project folder and run:

```
pip install openai-whisper
```

This will also install PyTorch and other required packages automatically. It may take a few minutes.

---

## Step 5 — Configure your file paths

Open `transcribe.py` in any text editor and find the configuration block near the top of the file (around line 10):

```python
# Folder containing your input .mp4 video file(s)
INPUT_DIR = r"C:\Users\YourName\Videos"

# Folder where the transcript .txt file will be saved
OUTPUT_DIR = r"C:\Users\YourName\Videos\transcripts"
```

Change these two paths to match your setup. For example:

```python
INPUT_DIR = r"C:\Users\John\Desktop\My Videos"
OUTPUT_DIR = r"C:\Users\John\Desktop\My Videos\transcripts"
```

> **Note:** Use a raw string (the `r` prefix before the quotes) so backslashes are handled correctly on Windows.

---

## Step 6 — Run the script

Open a terminal in the project folder.

**Option A — Auto-pick the first .mp4 found in INPUT_DIR:**
```
python transcribe.py
```

**Option B — Specify a video file directly:**
```
python transcribe.py "C:\Users\John\Desktop\My Videos\lecture.mp4"
```

**Option C — Use a more accurate model (slower):**
```
python transcribe.py --model medium
```

**Option D — Save transcript to a different folder:**
```
python transcribe.py --output-dir "C:\Users\John\Desktop\output"
```

The transcript will be saved as a `.txt` file with the same name as the video, in your OUTPUT_DIR.

---

## Model sizes

The `--model` flag controls the Whisper model used. Larger models are more accurate but slower and require more RAM.

| Model  | Speed   | Accuracy | RAM needed |
|--------|---------|----------|------------|
| tiny   | Fastest | Low      | ~1 GB      |
| base   | Fast    | OK       | ~1 GB      |
| small  | Medium  | Good     | ~2 GB      |
| medium | Slow    | Great    | ~5 GB      |
| large  | Slowest | Best     | ~10 GB     |

The default is `base`, which works well for most videos. For a 300MB video file, `base` takes roughly 5–15 minutes on a standard CPU.

The model is downloaded automatically the first time you run the script (~140MB for `base`).

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'whisper'`**
Run `pip install openai-whisper` and make sure you're using the same Python that pip installed it into.

**`ffmpeg is not recognized`**
ffmpeg is not on your PATH. Re-do Step 2, open a new terminal window, and try again.

**`No .mp4 files found in INPUT_DIR`**
The INPUT_DIR path in `transcribe.py` doesn't match where your video is. Update it and save the file.

**Script runs but transcript is empty or garbled**
Try a larger model with `--model small` or `--model medium`.

**Out of memory error**
Your machine doesn't have enough RAM for the selected model. Use a smaller model (e.g. `--model tiny`).
