import json
from PIL import Image

def parse_metadata(image_path, output_path):
    with Image.open(image_path) as img:
        if "Metadata" in img.info:
            metadata = img.info["Metadata"]
            metadata_dict = json.loads(metadata)
            with open(output_path, 'w') as json_file:
                json.dump(metadata_dict, json_file, indent=2)
            print(f"Metadata saved to {output_path}")
        else:
            print("No metadata found in the image.")

# Example usage
image_path = "stitched_image.png"
output_path = "metadata.json"
parse_metadata(image_path, output_path)

