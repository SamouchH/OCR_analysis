import json
import os

def combine_label_and_train_list(label_file, train_list_file, output_file):
    # Lire le fichier Label.txt et créer un dictionnaire des difficultés
    difficulty_dict = {}
    with open(label_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_name = parts[0]
                annotations = json.loads(parts[1])
                difficulty_dict[image_name] = {ann['transcription']: ann.get('difficult', False) for ann in annotations}

    # Lire train_list.txt et ajouter les informations de difficulté
    with open(train_list_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_path = parts[0]
                image_name = os.path.basename(image_path)
                annotations = json.loads(parts[1])

                # Ajouter l'information de difficulté à chaque annotation
                for ann in annotations:
                    transcription = ann['transcription']
                    if image_name in difficulty_dict and transcription in difficulty_dict[image_name]:
                        ann['difficult'] = difficulty_dict[image_name][transcription]
                    else:
                        ann['difficult'] = False  # Par défaut, mettre à False si l'information n'est pas trouvée

                # Écrire la nouvelle ligne dans le fichier de sortie
                f_out.write(f"{image_path}\t{json.dumps(annotations)}\n")

    print(f"Nouveau fichier créé : {output_file}")

# Chemins des fichiers
label_file = '../data/raw/Label.txt'
train_list_file = '../data/processed/train_list.txt'
output_file = '../data/processed/train_list_with_difficulty.txt'

# Exécuter la fonction
combine_label_and_train_list(label_file, train_list_file, output_file)