# Extract EGF Images

Extract EGF Images is a tool for extracting bitmap images from EGF files.

## Features

- Extract bitmap images from `.egf` files.
- Save extracted images into a structured directory format.

## Setup

Before you can run the script, you need to have Python installed on your system. This project is tested with Python 3.10 and above. To set up the project:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/ExileStudios/extract-egf-images.git
cd extract-egf-images
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To use the Extract EGF Images tool, follow these steps:

1. Place your `.egf` files in the `data/input` directory.

2. Run the script from the project root:

```bash
python src/extract_egf_images.py
```

3. Extracted `.bmp` images will be placed in the `data/output` directory, in subdirectories named after the original `.egf` files.

## Disclaimer

This script is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## Author

**Exile Studios**

- Website: [https://exile-studios.com](https://exile-studios.com)
- Github: [@ExileStudios](https://github.com/ExileStudios)
