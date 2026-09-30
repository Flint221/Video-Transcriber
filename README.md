# Video Transcriber

A Python script that transcribes MP4 video files to text using OpenAI Whisper, running entirely locally on your machine — no API keys or internet connection required after setup.

Explicit input paths also accept audio files such as `.m4a`. With no file argument,
the current default is `E:\School\2026-27\Fall\GEOG 301\Class Recordings\Geog 301 9-28.m4a`.
Transcripts are saved beside the input unless `--output-dir` is supplied.

## GPU or CPU processing

The default `--device auto` uses an available NVIDIA CUDA GPU, otherwise the CPU.
The script prints the selected device before loading the model. Use `--device cuda`
to require GPU processing or `--device cpu` to require CPU processing:

```powershell
python transcribe.py --model large --device cuda
python transcribe.py "E:\School\another-recording.m4a" --model large --device auto
python transcribe.py --model medium --device cpu
```

For the configured Python 3.13 installation and RTX 5080, install CUDA-enabled
PyTorch from the official CUDA 12.8 wheel index:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu128
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

The verification should report a CUDA build and `True`. The installed NVIDIA driver
and the PyTorch wheel supply what this setup needs; a separate CUDA Toolkit is
not required. GPU processing still uses some system RAM. Whisper's approximate
GPU memory requirements are 5 GB for `medium` and 10 GB for `large`; leave room
for other applications. GPU processing uses FP16, while CPU processing uses FP32.
Restart an existing Python session after changing PyTorch.

When `--model` is omitted, the script prompts for a model; it does not default to
`base` when launched interactively.

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
