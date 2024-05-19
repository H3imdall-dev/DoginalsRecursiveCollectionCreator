import os
import itertools
import random
import json

# Helper functions
def update_title(html_template, collection_name, index):
    return html_template.replace("<title>Your Collection Name 001</title>", f"<title>{collection_name} #{index}</title>")

def update_canvas_size(html_template, width, height):
    html_template = html_template.replace("width: 100vw;", f"width: {width}px;")
    return html_template.replace("height: 100vh;", f"height: {height}px;")

def update_inscription_id(html_template, inscription_id):
    return html_template.replace('<script src="/content/stitched_image.png"></script>', f'<script src="/content/{inscription_id}"></script>')

def update_trait_index(html_template, trait_index):
    return html_template.replace('<div id="traitindex">010101</div>', f'<div id="traitindex">{trait_index}</div>')

def save_html_file(output_dir, index, html_content):
    file_name = f"{index:05}.html"
    with open(os.path.join(output_dir, file_name), "w") as file:
        file.write(html_content)

def generate_combinations(trait_counts, collection_size, randomize=False, exclusions=set()):
    all_combinations = list(itertools.product(*[range(1, count+1) for count in trait_counts]))
    valid_combinations = [comb for comb in all_combinations if comb not in exclusions]
    
    if randomize:
        random.shuffle(valid_combinations)
        return valid_combinations[:collection_size]
    else:
        return valid_combinations[:collection_size]

def generate_metadata_entry_ow(collection_name, index, traits):
    return {
        "id": "",
        "meta": {
            "name": f"{collection_name} #{index}",
            "attributes": [{"trait_type": trait_type, "value": trait_value} for trait_type, trait_value in traits.items()]
        }
    }

def generate_metadata_entry_dm(collection_name, index, traits):
    return {
        "inscriptionId": "",
        "name": f"{collection_name} #{index}",
        "attributes": {trait_type: trait_value for trait_type, trait_value in traits.items()}
    }

def get_trait_value(layer_dir, index):
    files = sorted([f for f in os.listdir(layer_dir) if os.path.isfile(os.path.join(layer_dir, f))])
    if index <= len(files):
        return os.path.splitext(files[index - 1])[0]
    return None

def parse_exclusions(exclusion_input, layer_dirs, layer_names):
    exclusions = set()
    exclusion_entries = exclusion_input.split(',')
    for entry in exclusion_entries:
        entry = entry.strip()
        parts = entry.split(' ')
        if len(parts) == 2:
            layer_num_str, trait_name = parts
            if not layer_num_str.isdigit():
                print(f"Invalid layer number: {layer_num_str}")
                continue

            layer_num = int(layer_num_str)
            if layer_num < 1 or layer_num > len(layer_dirs):
                print(f"Layer number out of range: {layer_num}")
                continue

            layer_dir = layer_dirs[layer_num - 1]
            layer_name = layer_names[layer_dir]
            trait_index = None
            for i, filename in enumerate(sorted(os.listdir(layer_dir))):
                if os.path.splitext(filename)[0] == trait_name:
                    trait_index = i + 1
                    break
            if trait_index is not None:
                exclusions.add((layer_num, trait_index))
        elif len(parts) == 3:
            layer_to_exclude_str, specific_layer_str, specific_trait_name = parts
            if not (layer_to_exclude_str.isdigit() and specific_layer_str.isdigit()):
                print(f"Invalid format for exclusion: {entry}")
                continue

            layer_to_exclude = int(layer_to_exclude_str)
            specific_layer = int(specific_layer_str)
            if layer_to_exclude < 1 or layer_to_exclude > len(layer_dirs) or specific_layer < 1 or specific_layer > len(layer_dirs):
                print(f"Layer number out of range: {entry}")
                continue

            specific_layer_dir = layer_dirs[specific_layer - 1]
            specific_layer_name = layer_names[specific_layer_dir]
            specific_trait_index = None
            for i, filename in enumerate(sorted(os.listdir(specific_layer_dir))):
                if os.path.splitext(filename)[0] == specific_trait_name:
                    specific_trait_index = i + 1
                    break

            if specific_trait_index is not None:
                layer_to_exclude_dir = layer_dirs[layer_to_exclude - 1]
                for trait_index in range(1, len(os.listdir(layer_to_exclude_dir)) + 1):
                    exclusions.add((layer_to_exclude, trait_index))
                    exclusions.add((specific_layer, specific_trait_index))
        else:
            print(f"Invalid exclusion format: {entry}")
    return exclusions

# Main script
def main():
    # Load the HTML template
    with open("index.html", "r") as file:
        html_template = file.read()

    # Prompt user for inputs
    collection_name = input("Enter the collection name: ")
    canvas_height = input("Enter the canvas height: ")
    canvas_width = input("Enter the canvas width: ")
    
    while True:
        inscription_id = input("Enter the inscription ID (must end with 'i0'): ")
        if inscription_id.endswith("i0"):
            break
        else:
            print("Invalid inscription ID. It must end with 'i0'.")

    # Identify layer directories and count files
    layer_dirs = sorted([d for d in os.listdir() if os.path.isdir(d) and d.split(' ', 1)[0].isdigit()])
    trait_counts = []
    layer_names = {}
    for layer_dir in layer_dirs:
        parts = layer_dir.split(' ', 1)
        if len(parts) > 1:
            layer_name = parts[1]
        else:
            print(f"Skipping invalid directory name: {layer_dir}")
            continue  # Skip directories without proper format
        layer_names[layer_dir] = layer_name
        num_files = len([f for f in os.listdir(layer_dir) if os.path.isfile(os.path.join(layer_dir, f))])
        trait_counts.append(num_files)
    
    print("Layer directories and trait counts:")
    for i, (layer_dir, count) in enumerate(zip(layer_dirs, trait_counts)):
        print(f"Layer {i + 1}: {layer_dir} -> {count} traits")

    # Calculate max collection size
    max_collection_size = 1
    for count in trait_counts:
        max_collection_size *= count
    
    print(f"The maximum possible collection size is {max_collection_size}.")

    # Prompt for exclusions
    print("Enter exclusions in the following format: ")
    print("For excluding specific trait interactions: layer_number trait_name")
    print("For excluding an entire layer from interacting with a specific trait in another layer: layer_number specific_layer_number specific_trait_name")
    exclusion_input = input("Enter exclusions (separated by commas): ")
    exclusions = parse_exclusions(exclusion_input, layer_dirs, layer_names)
    exclusion_count = len(exclusions)
    
    print(f"Exclusions: {exclusions}")
    print(f"Number of excluded combinations: {exclusion_count}")

    if exclusion_count > 0:
        total_excluded_combinations = 1
        for layer_num, trait_index in exclusions:
            total_excluded_combinations *= trait_counts[layer_num - 1]
        adjusted_max_collection_size = max_collection_size - total_excluded_combinations
    else:
        adjusted_max_collection_size = max_collection_size
    
    print(f"The adjusted maximum possible collection size is {adjusted_max_collection_size}.")
    continue_generation = input("Do you want to continue with generation? (y/n): ")
    if continue_generation.lower() != 'y':
        print("Generation cancelled.")
        return

    collection_size = input(f"How many would you like to generate? (Enter 'max' for {adjusted_max_collection_size} or a custom number): ")
    
    if collection_size.lower() == 'max':
        collection_size = adjusted_max_collection_size
        randomize = False
    else:
        collection_size = int(collection_size)
        randomize = True

    # Prepare the output directories
    output_dir = "collection"
    metadata_dir = "marketmetadata"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)

    ow_metadata = []
    dm_metadata = []
    generated_combinations = set()

    # Generate HTML files and metadata entries for the specified number of combinations
    index = 1
    combinations = generate_combinations(trait_counts, adjusted_max_collection_size, randomize, exclusions)
    for combination in combinations:
        if combination in generated_combinations:
            continue  # Skip duplicates
        generated_combinations.add(combination)

        trait_index = "".join([f"{value:02}" for value in combination])
        traits = {}
        for i in range(len(combination)):
            layer_dir = layer_dirs[i]
            layer_name = layer_names[layer_dir]
            trait_value = get_trait_value(layer_dir, combination[i])
            if trait_value:
                traits[layer_name] = trait_value
        
        print(f"Generating file #{index} with traits: {traits}")
        
        html_content = html_template
        html_content = update_title(html_content, collection_name, index)
        html_content = update_canvas_size(html_content, canvas_width, canvas_height)
        html_content = update_inscription_id(html_content, inscription_id)
        html_content = update_trait_index(html_content, trait_index)
        save_html_file(output_dir, index, html_content)
        
        ow_metadata.append(generate_metadata_entry_ow(collection_name, index, traits))
        dm_metadata.append(generate_metadata_entry_dm(collection_name, index, traits))
        
        index += 1
        if len(generated_combinations) >= collection_size:
            break

    # Save OW.json and DM.json
    with open(os.path.join(metadata_dir, "OW.json"), "w") as file:
        json.dump(ow_metadata, file, indent=2)
    
    with open(os.path.join(metadata_dir, "DM.json"), "w") as file:
        json.dump(dm_metadata, file, indent=2)

    print(f"Generated {index - 1} HTML files in the '{output_dir}' directory.")
    print(f"Generated OW.json and DM.json in the '{metadata_dir}' directory.")

if __name__ == "__main__":
    main()
