import os
from src.data_preparation import convert_annotations
from src.fine_tuning import fine_tune_paddleocr

def main():
    # Préparation des données
    label_file = os.path.abspath('data/raw/Label.txt')
    image_dir = os.path.abspath('data/raw/images')
    output_dir = os.path.abspath('data/processed/annotations')
    train_list_file = os.path.abspath('data/processed/train_list.txt')
    
    os.makedirs(output_dir, exist_ok=True)
    #convert_annotations(label_file, image_dir, output_dir, train_list_file)
    
    # Fine-tuning
    config_file = os.path.abspath('config/fine_tuning_config.yml')
    fine_tune_paddleocr(config_file)

if __name__ == "__main__":
    main()