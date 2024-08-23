import json
import os

def filter_points(points):
    # Garder les points où soit l'abscisse soit l'ordonnée ne change pas
    filtered_points = []
    for i in range(len(points)):
        if len(filtered_points) >= 4:
            break
        if i > 0 and (points[i][0] == points[i - 1][0] or points[i][1] == points[i - 1][1]):
            filtered_points.append(points[i])
    
    # Si filtered_points est vide, on prend simplement les 4 premiers points
    if not filtered_points:
        filtered_points = points[:4]
    
    # Compléter à 4 points si nécessaire en prenant les plus proches
    while len(filtered_points) < 4:
        remaining_points = [pt for pt in points if pt not in filtered_points]
        if remaining_points:
            closest_point = min(remaining_points, key=lambda p: min([abs(p[0] - fp[0]) + abs(p[1] - fp[1]) for fp in filtered_points]))
            filtered_points.append(closest_point)
        else:
            break
    
    return filtered_points[:4]  # Retourner exactement 4 points

def adjust_train_list(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            image_path, annotation_str = line.strip().split('\t')
            annotations = json.loads(annotation_str)
            
            adjusted_annotations = []
            for annotation in annotations:
                points = annotation['points']
                if len(points) > 4:
                    annotation['points'] = filter_points(points)
                adjusted_annotations.append(annotation)
            
            # Écrire l'image et les annotations dans le fichier de sortie
            f_out.write(f"{image_path}\t{json.dumps(adjusted_annotations)}\n")

    print(f"Adjusted annotations saved to {output_file}")

if __name__ == "__main__":
    input_file = '../data/processed/train_list.txt'
    output_file = '../data/processed/train_list_adjusted.txt'
    
    adjust_train_list(input_file, output_file)
