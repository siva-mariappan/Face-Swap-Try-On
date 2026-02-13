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

## Note

⚠️ This tool is for educational and creative purposes. Please use responsibly and respect privacy rights.

---

Built with ❤️ using Gradio and InsightFace
