"""
extract_egf_images.py
Extract Bitmap Images from EGF Files

This script is designed to extract bitmap images from .egf files.
It processes each .egf file located within the specified input directory and
saves the extracted images as .bmp files in the specified output directory.

Usage:
    Run the script with no arguments. Modify the INPUT_DIR and OUTPUT_DIR
    variables as necessary to point to the correct directories.
"""

import os
from egf_parser import extract_bitmaps_from_pe

# Set input and output directories
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

def extract_images():
    """
    Iterates over all files in the INPUT_DIR, processes each file with an .egf extension,
    extracts bitmap images contained within, and saves them as .bmp files in a subdirectory
    within the OUTPUT_DIR named after the original .egf file.
    """
    # Iterate over files in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".egf"):  # Check for .egf extension
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"Extracting images from: {file_path}")
            
            # Extract bitmap images from the .egf file
            extracted_data = extract_bitmaps_from_pe(file_path)
            print(f"Extracted {len(extracted_data)} BMP images from {filename}")

            # Create a directory named after the .egf file
            file_name_without_ext = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(OUTPUT_DIR, file_name_without_ext)
            os.makedirs(file_output_dir, exist_ok=True)

            # Process each extracted bitmap
            for resource_id, data in extracted_data.items():
                if resource_id is None:  # Skip if the resource_id is None
                    continue
                bmp_filename = f"{resource_id}.bmp"
                bmp_path = os.path.join(file_output_dir, bmp_filename)
                # Save the bitmap image as .bmp
                with open(bmp_path, 'wb') as bmp_file:
                    bmp_file.write(data)
                print(f"Saved BMP image for resource ID: {resource_id} in {file_output_dir}")

# Execute the extract_images function when the script is run
if __name__ == "__main__":
    extract_images()