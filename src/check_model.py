import os
import paddle

def check_model(model_dir):
    # Conversion en chemin absolu
    model_dir = os.path.abspath(model_dir)
    print(f"Vérification du modèle dans le répertoire : {model_dir}")
    
    # Vérifier les fichiers présents
    files = os.listdir(model_dir)
    print("Fichiers présents :")
    for file in files:
        file_path = os.path.join(model_dir, file)
        print(f" - {file} ({os.path.getsize(file_path)} bytes)")
    
    # Essayer de charger le modèle
    try:
        model_path = os.path.join(model_dir, "inference.pdmodel")
        param_path = os.path.join(model_dir, "inference.pdiparams")
        
        print(f"\nChemin du modèle : {model_path}")
        print(f"Chemin des paramètres : {param_path}")
        
        if not os.path.exists(model_path):
            print(f"Le fichier {model_path} n'existe pas.")
            return
        if not os.path.exists(param_path):
            print(f"Le fichier {param_path} n'existe pas.")
            return
        
        model = paddle.jit.load(model_path)
        state_dict = paddle.load(param_path)
        
        print("\nStructure du modèle :")
        for name, param in model.state_dict().items():
            print(f" - {name}: {param.shape}")
        
        print("\nLe modèle a été chargé avec succès.")
    except Exception as e:
        print(f"\nErreur lors du chargement du modèle : {str(e)}")

if __name__ == "__main__":
    model_dir = "../output/inference"
    check_model(model_dir)