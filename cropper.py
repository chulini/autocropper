import os
import sys
import argparse
from PIL import Image

def crop_and_resize_image(image_path, output_path, size):
    # Open the image
    with Image.open(image_path) as img:
        # Check if the image has an alpha channel (transparency)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Convert image to RGBA if it isn't already
            img = img.convert("RGBA")
            
            # Get bounding box of the non-transparent part
            bbox = img.getbbox()
            
            if bbox:
                # Crop the image to the bounding box
                img_cropped = img.crop(bbox)
                
                # Resize the image while maintaining aspect ratio
                img_cropped.thumbnail((size, size), Image.Resampling.LANCZOS)
                
                # Create a new square image with transparent background
                square_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                
                # Calculate position to paste the resized image in the center of the square canvas
                offset = ((size - img_cropped.width) // 2, (size - img_cropped.height) // 2)
                square_img.paste(img_cropped, offset)
                
                # Save the resulting image
                square_img.save(output_path)

def process_images_in_directory(input_dir, output_dir, size):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Filter image files
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Process each image
            crop_and_resize_image(input_path, output_path, size)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Crop and resize images")
    parser.add_argument("size", type=int, help="The size to resize the cropped images to (e.g., 1024 for 1024x1024)")
    
    # Parse arguments
    args = parser.parse_args()
    output_size = args.size  # The size for both width and height
    
    # Directories
    current_directory = os.path.dirname(__file__)  # Gets the current directory where the script is located
    input_directory = os.path.join(current_directory, "input")
    output_directory = os.path.join(current_directory, "output")

    # Process the images with the specified output size
    process_images_in_directory(input_directory, output_directory, output_size)
