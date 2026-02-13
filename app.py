import gradio as gr
import numpy as np
import cv2
import insightface
from insightface.app import FaceAnalysis
from PIL import Image
import tempfile
import os
from tqdm import tqdm

# Initialize face analysis and model (loaded once at startup)
print("Loading models... This may take a moment...")
app = FaceAnalysis(name='buffalo_l')
# Increase detection size for better quality (640x640 -> 1024x1024)
app.prepare(ctx_id=0, det_size=(1024, 1024))
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)
print("Models loaded successfully!")


def face_swap(source_image, target_image):
    """
    Swap face from source image to target image
    Output maintains the same quality as target image input

    Args:
        source_image: PIL Image or numpy array (the face to use)
        target_image: PIL Image or numpy array (the image where face will be swapped)

    Returns:
        Swapped image as numpy array with same quality as input
    """
    try:
        # Convert PIL Images to numpy arrays if needed
        if isinstance(source_image, Image.Image):
            source_image = np.array(source_image)
        if isinstance(target_image, Image.Image):
            target_image = np.array(target_image)

        # Store original dimensions - output will be same size as input
        original_height, original_width = target_image.shape[:2]

        # Convert RGB to BGR for OpenCV
        source_img = cv2.cvtColor(source_image, cv2.COLOR_RGB2BGR)
        target_img = cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR)

        # No upscaling - process at original resolution to preserve input quality

        # Detect face in source image
        source_faces = app.get(source_img)
        if len(source_faces) == 0:
            return None, "❌ Error: No face detected in source image. Please upload an image with a clear face."

        # Use the largest/most confident face
        source_face = max(source_faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))

        # Detect faces in target image
        target_faces = app.get(target_img)
        if len(target_faces) == 0:
            return None, "❌ Error: No face detected in target image. Please upload an image with at least one face."

        # Perform face swap at original resolution
        result = target_img.copy()
        for face in target_faces:
            result = swapper.get(result, face, source_face, paste_back=True)

        # No enhancement - preserve original quality exactly as input

        # Convert BGR back to RGB for display
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        status_msg = f"✅ Success! Swapped {len(target_faces)} face(s). Output matches target image quality."

        return result, status_msg

    except Exception as e:
        return None, f"❌ Error during face swap: {str(e)}"


def face_swap_video(source_image, target_video, progress=gr.Progress()):
    """
    Swap face from source image to all faces in target video

    Args:
        source_image: PIL Image or numpy array (the face to use)
        target_video: Path to video file
        progress: Gradio progress tracker

    Returns:
        Path to output video file and status message
    """
    try:
        # Convert source image if needed
        if isinstance(source_image, Image.Image):
            source_image = np.array(source_image)

        # Convert RGB to BGR for OpenCV
        source_img = cv2.cvtColor(source_image, cv2.COLOR_RGB2BGR)

        # Detect face in source image
        progress(0, desc="Detecting source face...")
        source_faces = app.get(source_img)
        if len(source_faces) == 0:
            return None, "Error: No face detected in source image. Please upload an image with a clear face."

        # Use the largest/most confident face
        source_face = max(source_faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))

        # Open video file
        progress(0.05, desc="Opening video file...")
        cap = cv2.VideoCapture(target_video)

        if not cap.isOpened():
            return None, "Error: Could not open video file."

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create temporary output video file (without audio first)
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='_temp.mp4')
        temp_video_path = temp_video.name
        temp_video.close()

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video_path, fourcc, fps, (frame_width, frame_height))

        # Process each frame
        frame_count = 0
        faces_swapped = 0

        progress(0.1, desc=f"Processing frames (0/{total_frames})...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Detect faces in current frame
            target_faces = app.get(frame)

            # Swap faces if detected
            if len(target_faces) > 0:
                for face in target_faces:
                    frame = swapper.get(frame, face, source_face, paste_back=True)
                    faces_swapped += 1

            # Write frame to output
            out.write(frame)

            # Update progress
            if frame_count % 10 == 0:
                progress_val = 0.1 + (frame_count / total_frames) * 0.7
                progress(progress_val, desc=f"Processing frames ({frame_count}/{total_frames})...")

        # Release resources
        cap.release()
        out.release()

        # Create final output video file with audio
        progress(0.85, desc="Adding audio to video...")
        final_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        final_output_path = final_output.name
        final_output.close()

        # Use FFmpeg to merge audio from original video
        ffmpeg_cmd = f'ffmpeg -i "{temp_video_path}" -i "{target_video}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0? -shortest -y "{final_output_path}" 2>&1'
        os.system(ffmpeg_cmd)

        # Clean up temp video
        os.unlink(temp_video_path)

        progress(1.0, desc="Video processing complete!")

        status_msg = f"Success! Processed {frame_count} frames, swapped {faces_swapped} face instances."

        return final_output_path, status_msg

    except Exception as e:
        return None, f"Error during video face swap: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="Face-Swap-Try-On") as demo:
    gr.Markdown(
        """
        # Face-Swap-Try-On
        Upload a **source face** and swap it into **images or videos**!
        """
    )

    with gr.Tabs():
        # Image Face Swap Tab
        with gr.Tab("Image Face Swap"):
            with gr.Row():
                with gr.Column():
                    img_source_input = gr.Image(
                        label="Source Person Image",
                        type="pil",
                        height=300
                    )
                    gr.Markdown("*Upload the face you want to use for swapping*")

                with gr.Column():
                    img_target_input = gr.Image(
                        label="Target Person Face",
                        type="pil",
                        height=300
                    )
                    gr.Markdown("*Upload the image where you want to swap the face*")

            with gr.Row():
                img_swap_btn = gr.Button("Swap Faces", variant="primary", size="lg")
                img_clear_btn = gr.ClearButton(components=[img_source_input, img_target_input], value="Clear")

            img_status_output = gr.Textbox(label="Status", interactive=False)

            with gr.Row():
                img_output = gr.Image(
                    label="Output - Swapped Result",
                    type="numpy",
                    height=400
                )

            # Connect the swap button
            img_swap_btn.click(
                fn=face_swap,
                inputs=[img_source_input, img_target_input],
                outputs=[img_output, img_status_output]
            )

        # Video Face Swap Tab
        with gr.Tab("Video Face Swap"):
            with gr.Row():
                with gr.Column():
                    vid_source_input = gr.Image(
                        label="Source Person Image",
                        type="pil",
                        height=300
                    )
                    gr.Markdown("*Upload the face you want to use for swapping*")

                with gr.Column():
                    vid_target_input = gr.Video(
                        label="Target Video",
                        height=300
                    )
                    gr.Markdown("*Upload the video where you want to swap faces*")

            with gr.Row():
                vid_swap_btn = gr.Button("Swap Faces in Video", variant="primary", size="lg")
                vid_clear_btn = gr.ClearButton(components=[vid_source_input, vid_target_input], value="Clear")

            vid_status_output = gr.Textbox(label="Status", interactive=False)

            with gr.Row():
                vid_output = gr.Video(
                    label="Output - Swapped Video",
                    height=400
                )

            # Connect the swap button
            vid_swap_btn.click(
                fn=face_swap_video,
                inputs=[vid_source_input, vid_target_input],
                outputs=[vid_output, vid_status_output]
            )

    # Tips
    gr.Markdown("### Tips for Best Results:")
    gr.Markdown(
        """
        **For Images:**
        - Output quality matches your target image quality - no upscaling or downscaling
        - Use high resolution images for better results
        - Fast processing - output maintains original target image resolution

        **For Videos:**
        - Video processing takes longer depending on video length and resolution
        - Audio from original video is preserved
        - Supports MP4, AVI, MOV, MKV formats

        **General:**
        - Use clear, well-lit images/videos with frontal faces
        - PNG format preserves quality better than JPG for images
        - Avoid blurry, dark, or side-angle faces
        - The face from the source image will replace all faces in the target
        """
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        show_error=True,
        theme=gr.themes.Soft()
    )
