import os
from io import BytesIO
from PIL import Image
from egf_parser import extract_bitmaps_from_pe

# Set input and output directories
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

def convert_to_png_with_transparency(bmp_data, use_8_0_0_rule):
    """
    Converts BMP byte data to a PNG image with transparency based on custom rules:
    - If RGB(8,0,0) is present, it becomes transparent and RGB(0,0,0) remains.
    - Otherwise, RGB(0,0,0) becomes transparent.
    """
    with Image.open(BytesIO(bmp_data)) as img:
        img = img.convert("RGBA")
        pixels = img.load()
        width, height = img.size

        # Check if RGB(8,0,0) is present
        has_8_0_0 = any(
            pixels[x, y][:3] == (8, 0, 0)
            for y in range(height)
            for x in range(width)
        )

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if has_8_0_0 and use_8_0_0_rule:
                    if (r, g, b) == (8, 0, 0):
                        pixels[x, y] = (0, 0, 0, 0)
                else:
                    if (r, g, b) == (0, 0, 0):
                        pixels[x, y] = (0, 0, 0, 0)

        return img

def extract_images():
    """
    Iterates over all files in the INPUT_DIR, processes each file with an .egf extension,
    extracts bitmap images contained within, converts them to PNG with transparency, and
    saves them in a subdirectory within the OUTPUT_DIR named after the original .egf file.
    """
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".egf"):
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"Extracting images from: {file_path}")
            
            # Flag whether this file uses the (8, 0, 0) transparency rule
            use_8_0_0_rule = filename.lower() in {"gfx015.egf", "gfx016.egf"}

            extracted_data = extract_bitmaps_from_pe(file_path)
            print(f"Extracted {len(extracted_data)} BMP images from {filename}")

            file_name_without_ext = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(OUTPUT_DIR, file_name_without_ext)
            os.makedirs(file_output_dir, exist_ok=True)

            for resource_id, data in extracted_data.items():
                if resource_id is None:
                    continue

                png_filename = f"{resource_id}.png"
                png_path = os.path.join(file_output_dir, png_filename)

                try:
                    png_image = convert_to_png_with_transparency(data, use_8_0_0_rule)
                    png_image.save(png_path, "PNG")
                    print(f"Saved PNG image for resource ID: {resource_id} in {file_output_dir}")
                except Exception as e:
                    print(f"Failed to process image {resource_id}: {e}")

if __name__ == "__main__":
    extract_images()
