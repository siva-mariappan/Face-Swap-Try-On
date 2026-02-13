import numpy as np
import os
import cv2
import insightface
from insightface.app import FaceAnalysis
from PIL import Image
import glob

assert insightface.__version__ >= '0.7'

def batch_face_swap(input_folder, source_folder, output_folder, model_path='inswapper_128.onnx'):
    """
    Batch process face swapping for all images in input folder

    Parameters:
    input_folder: Folder containing target images (faces to be replaced)
    source_folder: Folder containing the source face image
    output_folder: Folder to save results
    model_path: Path to the inswapper model file
    """
    print("Initializing face analysis and swapper model...")

    # Initialize face analysis
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))

    # Load face swapper model
    swapper = insightface.model_zoo.get_model(model_path, download=False, download_zip=False)

    # Get source face image (first image in source folder)
    source_images = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG', '*.bmp', '*.BMP', '*.webp', '*.WEBP']:
        source_images.extend(glob.glob(os.path.join(source_folder, ext)))
    if not source_images:
        raise ValueError(f"No images found in source folder: {source_folder}")

    source_face_path = source_images[0]
    print(f"Loading source face from: {source_face_path}")

    # Load source face image
    try:
        source_img = cv2.imread(source_face_path)
        if source_img is None:
            print(f"OpenCV couldn't read {source_face_path}, trying with PIL...")
            pil_img = Image.open(source_face_path)
            pil_img = pil_img.convert('RGB')
            source_img = np.array(pil_img)
            source_img = cv2.cvtColor(source_img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Failed to load source image: {e}")

    # Detect face in source image
    source_faces = app.get(source_img)
    if len(source_faces) == 0:
        raise ValueError("No face detected in the source image")

    source_face = source_faces[0]
    print(f"Source face detected successfully!")

    # Get all images from input folder
    input_images = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG', '*.bmp', '*.BMP', '*.webp', '*.WEBP']:
        input_images.extend(glob.glob(os.path.join(input_folder, ext)))

    if not input_images:
        raise ValueError(f"No images found in input folder: {input_folder}")

    print(f"\nFound {len(input_images)} image(s) to process\n")

    # Process each target image
    for idx, target_image_path in enumerate(input_images, 1):
        try:
            filename = os.path.basename(target_image_path)
            print(f"[{idx}/{len(input_images)}] Processing: {filename}")

            # Load target image
            target_img = cv2.imread(target_image_path)
            if target_img is None:
                print(f"  OpenCV couldn't read {filename}, trying with PIL...")
                pil_img = Image.open(target_image_path)
                pil_img = pil_img.convert('RGB')
                target_img = np.array(pil_img)
                target_img = cv2.cvtColor(target_img, cv2.COLOR_RGB2BGR)

            # Detect faces in target image
            target_faces = app.get(target_img)
            if len(target_faces) == 0:
                print(f"  ⚠️  No faces detected in {filename}, skipping...")
                continue

            print(f"  Detected {len(target_faces)} face(s)")

            # Create a copy of target image
            result = target_img.copy()

            # Replace each face with source face
            for face in target_faces:
                result = swapper.get(result, face, source_face, paste_back=True)

            # Save result
            output_filename = f"swapped_{filename}"
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, result)
            print(f"  ✓ Saved to: {output_filename}\n")

        except Exception as e:
            print(f"  ✗ Error processing {filename}: {str(e)}\n")
            continue

    print("=" * 50)
    print("Face swap batch processing completed!")
    print("=" * 50)

if __name__ == '__main__':
    # Define folder paths
    input_folder = "input person image"
    source_folder = "swap person image"
    output_folder = "Output folder"
    model_path = 'inswapper_128.onnx'

    print("=" * 50)
    print("BATCH FACE SWAP - Starting...")
    print("=" * 50)
    print(f"Input folder: {input_folder}")
    print(f"Source folder: {source_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Model: {model_path}")
    print("=" * 50 + "\n")

    batch_face_swap(input_folder, source_folder, output_folder, model_path)
