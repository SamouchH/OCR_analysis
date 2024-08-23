import json

# Path to your train_list.txt
#file_path = '../data/processed/train_list_adjusted.txt'
file_path = '../data/processed/train_list.txt'

def check_annotations(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # Extract the annotation part (after the tab character)
        image_path, annotations_str = line.split('\t', 1)
        annotations = json.loads(annotations_str)

        for annotation in annotations:
            points = annotation['points']
            if len(points) > 4:
                print(f"Annotation with more than 4 points found in image {image_path}:")
                print(f"Points: {points}")
    print("Check completed.")

check_annotations(file_path)
