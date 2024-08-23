import json
import os

def process_label_file(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_path, json_data = parts
                image_name = os.path.basename(image_path)
                output_filename = os.path.splitext(image_name)[0] + '.txt'
                output_path = os.path.join(output_dir, output_filename)
                
                data = json.loads(json_data)
                
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    for item in data:
                        coords = [str(coord) for point in item['points'] for coord in point]
                        transcription = item['transcription']
                        output_line = f"{','.join(coords)},{transcription}\n"
                        outfile.write(output_line)

# Utilisation de la fonction

process_label_file('../data/processed/train_list.txt', './data/labels_train')
process_label_file('../data/processed/eval_list.txt', './data/labels_eval')
