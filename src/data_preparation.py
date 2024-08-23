import json
import os

def convert_annotations(image_dir, annotation_dir, output_dir, train_list_file):
    os.makedirs(output_dir, exist_ok=True)
    
    train_list = []
    
    for image_file in os.listdir(image_dir):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):
            image_name = os.path.splitext(image_file)[0]
            annotation_file = f"{image_name}.txt"
            annotation_path = os.path.join(annotation_dir, annotation_file)
            
            if os.path.exists(annotation_path):
                with open(annotation_path, 'r', encoding='utf-8') as f:
                    annotations = json.load(f)
                
                image_path = os.path.abspath(os.path.join(image_dir, image_file))
                output_file = os.path.abspath(os.path.join(output_dir, f"{image_name}.txt"))
                
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    for ann in annotations:
                        points = ann['points']
                        transcription = ann['transcription']
                        difficult = '0'  # Assumons que tous ne sont pas difficiles par défaut
                        
                        line = f"{','.join([str(p) for point in points for p in point])}\t{transcription}\t{difficult}\n"
                        out_f.write(line)
                
                # Créer l'entrée pour train_list.txt
                train_list_entry = f"{image_path}\t{json.dumps(annotations)}\n"
                train_list.append(train_list_entry)
    
    # Écrire train_list.txt
    with open(train_list_file, 'w', encoding='utf-8') as f:
        f.writelines(train_list)

if __name__ == "__main__":
    image_dir = os.path.abspath('../data/raw/images')
    annotation_dir = os.path.abspath('../data/processed/output_annotations_json')
    output_dir = os.path.abspath('../data/processed/annotations')
    train_list_file = os.path.abspath('../data/processed/train_list.txt')
    
    convert_annotations(image_dir, annotation_dir, output_dir, train_list_file)
