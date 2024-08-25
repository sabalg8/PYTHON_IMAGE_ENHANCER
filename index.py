import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm
import os
from tkinter import Tk, filedialog

def enhance_image(image_path, output_path, sharpness_factor=2.0, contrast_factor=1.1, blur_radius=0):
    # Load the image using PIL
    image = Image.open(image_path)

    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness_factor)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    # Apply Unsharp Mask instead of Gaussian Blur to increase sharpness
    if blur_radius > 0:
        image = image.filter(ImageFilter.UnsharpMask(radius=blur_radius, percent=150, threshold=3))

    # Convert to OpenCV format
    image_cv = np.array(image)

    # Convert back to PIL format
    image = Image.fromarray(image_cv)

    # Save the enhanced image
    image.save(output_path)

def process_directory(input_directory, output_directory, sharpness_factor=2.0, contrast_factor=1.5, blur_radius=0):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in tqdm(os.listdir(input_directory)):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            enhance_image(input_path, output_path, sharpness_factor, contrast_factor, blur_radius)

def select_directory(title):
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title=title)
    return directory

if __name__ == "__main__":
    input_dir = select_directory("Select Input Directory")
    output_dir = select_directory("Select Output Directory")

    if input_dir and output_dir:
        process_directory(input_dir, output_dir)
    else:
        print("Directory selection cancelled.")
