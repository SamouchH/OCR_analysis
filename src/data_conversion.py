import os
import json
from tqdm import tqdm

def convert_annotations_to_json(annotation_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for annotation_file in os.listdir(annotation_dir):
        if annotation_file.endswith(".txt"):
            # Chemin complet du fichier d'annotation
            annotation_path = os.path.join(annotation_dir, annotation_file)
            
            with open(annotation_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            json_annotations = []

            for line in lines:
                parts = line.strip().split('\t')
                
                if len(parts) < 2:
                    continue  # Ignore les lignes mal formatées
                
                # Gestion des coordonnées avec des virgules
                coords = parts[0].replace(',', ' ').split()
                
                # On s'assure qu'il y a un nombre pair de coordonnées
                if len(coords) % 2 != 0:
                    continue
                
                # Extraction des points de la boîte de délimitation
                points = []
                for i in range(0, len(coords), 2):
                    try:
                        x = int(coords[i])
                        y = int(coords[i + 1])
                        points.append([x, y])
                    except ValueError:
                        print(f"Erreur de conversion des coordonnées dans le fichier : {annotation_file}, ligne : {line}")
                        continue

                transcription = parts[1]  # Le texte à reconnaître

                # Création de la structure JSON pour cette annotation
                json_annotations.append({
                    "transcription": transcription,
                    "points": points
                })

            # Sauvegarde des annotations JSON
            output_path = os.path.join(output_dir, annotation_file)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(json_annotations, output_file, ensure_ascii=False, indent=2)

            print(f"Annotations JSON sauvegardées dans : {output_path}")

if __name__ == "__main__":
    # Dossier contenant vos fichiers d'annotations actuels
    annotation_dir = "../data/processed/annotations"
    # Dossier où les fichiers JSON seront sauvegardés
    output_dir = "../data/processed/output_annotations_json"

    convert_annotations_to_json(annotation_dir, output_dir)
