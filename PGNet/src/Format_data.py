import json
import os

def process_label_file(input_file, output_dir):
    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            # Sépare le nom de fichier et les données JSON
            filename, json_data = line.strip().split('\t')
            data = json.loads(json_data)
            
            # Créer un nom de fichier de sortie basé sur le nom de l'image
            output_filename = os.path.splitext(filename)[0] + '.txt'
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for item in data:
                    # Extrait les coordonnées et les aplatit
                    coords = [str(coord) for point in item['points'] for coord in point]
                    
                    # Formate la ligne de sortie
                    output_line = f"{','.join(coords)},{item['transcription']}\n"
                    
                    # Écrit la ligne dans le fichier de sortie
                    outfile.write(output_line)

# Utilisation de la fonction
process_label_file('../../data/processed/train_list.txt', '../data/train_labels')