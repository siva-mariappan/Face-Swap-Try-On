---
title: Face Swap Try On
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
license: mit
---

# Face-Swap-Try-On 🎭

A powerful face swapping application that can swap faces in both **images** and **videos**!

## Features

✨ **Image Face Swap**
- Swap faces between any two images
- High-quality results maintaining original resolution
- Fast processing with insightface models

🎬 **Video Face Swap**
- Swap faces in videos with audio preservation
- Supports MP4, AVI, MOV, MKV formats
- Real-time progress tracking
- Processes all faces in every frame

## Examples

### Input Images
**Source Face (Swap Person):**

![Source Face](swap%20person%20image/swapinput01.png)

**Target Images (Input Person):**

![Target Image 1](input%20person%20image/Inputperson01.png)
![Target Image 2](input%20person%20image/input02.jpg)

### Output Results

![Output Result 1](Output%20folder/Output01.png)
![Output Result 2](Output%20folder/Output02.jpg)

## How to Run This Project

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- ffmpeg (for video processing)

### Installation & Setup

#### Step 1: Clone the Repository
```bash
git clone https://github.com/siva-mariappan/Face-Swap-Try-On.git
cd Face-Swap-Try-On
```

#### Step 2: Create Virtual Environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install System Dependencies
```bash
# On macOS (using Homebrew):
brew install ffmpeg

# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install ffmpeg libgl1 libglib2.0-0

# On Windows:
# Download ffmpeg from https://ffmpeg.org/download.html and add to PATH
```

#### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
pip install gradio
```

#### Step 5: Download the Face Swap Model
```bash
pip install -U insightface
pip install onnxruntime
```

The `inswapper_128.onnx` model file (529MB) should already be included in the repository. If not, you can download it from the pip install -U insightface.

#### Step 6: Run the Application
```bash
python app.py
```

The application will start and display a local URL (usually `http://127.0.0.1:7860`). Open this URL in your web browser.

### Quick Start (One-Liner)
```bash
git clone https://github.com/siva-mariappan/Face-Swap-Try-On.git && cd Face-Swap-Try-On && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python app.py
```

---

## How to Use

### Image Face Swap
1. Go to the **"Image Face Swap"** tab
2. Upload a source image (the face you want to use)
3. Upload a target image (where the face will be swapped)
4. Click **"Swap Faces"**
5. Download your result!

### Video Face Swap
1. Go to the **"Video Face Swap"** tab
2. Upload a source image (the face you want to use)
3. Upload a target video (the video where faces will be swapped)
4. Click **"Swap Faces in Video"**
5. Wait for processing (shows progress)
6. Download your video with preserved audio!

### Batch Processing
For processing multiple images at once:
```bash
python batch_face_swap.py
```
- Place source face image in `swap person image/` folder
- Place target images in `input person image/` folder
- Results will be saved in `Output folder/`

## Tips for Best Results

**For Images:**
- Use high-resolution images for better results
- Ensure faces are well-lit and clearly visible
- Frontal faces work best

**For Videos:**
- Processing time depends on video length and resolution
- Audio from original video is automatically preserved
- All detected faces in the video will be swapped

**General:**
- Use clear, well-lit images/videos
- Avoid blurry, dark, or extreme side-angle faces
- PNG format preserves quality better than JPG

## Technology

- **InsightFace** - Face detection and recognition
- **ONNX Runtime** - Optimized model inference
- **Gradio** - Beautiful web interface
- **OpenCV** - Image and video processing

## Models

This application uses the `inswapper_128.onnx` model for high-quality face swapping.

## Troubleshooting

### Common Issues

**Issue: "No module named 'insightface'"**
```bash
pip install insightface==0.7.3
```

**Issue: "ONNX Runtime not found"**
```bash
pip install onnxruntime==1.18.0
```

**Issue: "cv2 not found"**
```bash
pip install opencv-python-headless==4.9.0.80
```

**Issue: Model file not found**
- Ensure `inswapper_128.onnx` is in the project root directory
- File size should be approximately 529MB

**Issue: FFmpeg not found**
- Install ffmpeg using your system package manager
- Verify installation: `ffmpeg -version`

**Issue: Slow processing**
- Use GPU acceleration by installing `onnxruntime-gpu` instead of `onnxruntime`
- Reduce image/video resolution before processing

---

## Project Structure
```
Face-Swap-Try-On/
├── app.py                      # Main Gradio application
├── batch_face_swap.py          # Batch processing script
├── inswapper_128.onnx          # Face swap model (529MB)
├── requirements.txt            # Python dependencies
├── packages.txt                # System dependencies
├── runtime.txt                 # Python version
├── README.md                   # This file
├── input person image/         # Sample input images
├── swap person image/          # Source face images
└── Output folder/              # Generated results
```

---

## Note

⚠️ This tool is for educational and creative purposes. Please use responsibly and respect privacy rights.

Built with ❤️ using Gradio and InsightFace
