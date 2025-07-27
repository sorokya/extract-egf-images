import os
import json
from io import BytesIO
from PIL import Image
from egf_parser import extract_bitmaps_from_pe

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
MAX_ATLAS_WIDTH = 4096

def convert_to_png_with_transparency(bmp_data, use_8_0_0_rule):
    with Image.open(BytesIO(bmp_data)) as img:
        img = img.convert("RGBA")
        pixels = img.load()
        width, height = img.size

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
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".egf"):
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"Extracting images from: {file_path}")
            
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

    generate_all_atlases(OUTPUT_DIR)

def generate_all_atlases(root_dir):
    for folder in os.listdir(root_dir):
        if not folder.lower().startswith("gfx"):
            continue

        folder_path = os.path.join(root_dir, folder)
        png_files = [
            f for f in os.listdir(folder_path) if f.endswith(".png") and not f.startswith("atlas")
        ]

        if not png_files:
            print(f"No PNGs in {folder}, skipping atlas.")
            continue

        print(f"Generating atlas for {folder}...")

        png_files.sort(key=lambda name: int(os.path.splitext(name)[0]))

        current_x = 0
        current_y = 0
        row_height = 0
        atlas_height = 0

        positions = {}
        images = []
        for filename in png_files:
            resource_id = int(os.path.splitext(filename)[0])
            if resource_id == 1:
                continue

            img_path = os.path.join(folder_path, filename)
            with Image.open(img_path) as img:
                w, h = img.size

                if current_x + w > MAX_ATLAS_WIDTH:
                    current_x = 0
                    current_y += row_height
                    row_height = 0

                # Copy the image so it stays valid after context closes
                images.append((img.copy(), current_x, current_y))

                positions[resource_id - 100] = {
                    "x": current_x, "y": current_y, "w": w, "h": h
                }

                current_x += w
                row_height = max(row_height, h)
                atlas_height = max(atlas_height, current_y + row_height)

        atlas_image = Image.new("RGBA", (MAX_ATLAS_WIDTH, max(1, atlas_height)), (0, 0, 0, 0))
        for img, x, y in images:
            atlas_image.paste(img, (x, y))

        atlas_path = os.path.join(folder_path, "atlas.png")
        atlas_image.save(atlas_path)
        print(f"Saved {atlas_path}")

        json_path = os.path.join(folder_path, "atlas.json")
        with open(json_path, "w") as f:
            json.dump(positions, f, indent=2)
        print(f"Saved {json_path}")

if __name__ == "__main__":
    extract_images()
