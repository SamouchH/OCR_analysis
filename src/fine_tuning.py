import os
import sys
import subprocess
from paddleocr.tools.program import preprocess, train
from paddleocr.ppocr.modeling.architectures import build_model
from paddleocr.ppocr.losses import build_loss
from paddleocr.ppocr.optimizer import build_optimizer
from paddleocr.ppocr.postprocess import build_post_process
from paddleocr.ppocr.metrics import build_metric
from paddleocr.ppocr.data import build_dataloader
#from paddleocr.tools.export_model import main as export_model_main
#from paddleocr.tools.program import load_config, merge_config, ArgsParser
import paddle



def export_model(config):
    # Chemin vers le script export_model.py
    export_script = 'PaddleOCR/tools/export_model.py'
    
    # Chemin vers le fichier de configuration
    config_path = os.path.join(config['Global']['save_model_dir'], 'config.yml')
    
    # Chemin vers le modèle pré-entraîné
    pretrained_model = os.path.join(config['Global']['save_model_dir'], 'latest')
    
    # Chemin vers le répertoire d'exportation
    inference_dir = config['Global']['save_inference_dir']
    
    # Créez le répertoire d'exportation s'il n'existe pas
    os.makedirs(inference_dir, exist_ok=True)
    
    # Construisez la commande
    command = [
        sys.executable,  # Utilisez l'interpréteur Python actuel
        export_script,
        '-c', config_path,
        '-o', f"Global.pretrained_model={pretrained_model}",
        f"Global.save_inference_dir={inference_dir}"
    ]
    
    try:
        # Exécutez la commande
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Sortie de l'exportation du modèle:")
        print(result.stdout)
        print(f"Le modèle a été exporté avec succès dans : {inference_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de l'exportation du modèle:")
        print(e.stderr)

def fine_tune_paddleocr(config_file):
    # Ajouter le chemin du fichier de configuration aux arguments système
    sys.argv.extend(['--config', config_file])
    
    # Prétraitement et chargement de la configuration
    config, device, logger, log_writer = preprocess(is_train=True)
    
    # Construction du modèle
    model = build_model(config['Architecture'])
    
    # Chargement du modèle pré-entraîné
    if config['Global']['pretrained_model']:
        model.set_state_dict(paddle.load(config['Global']['pretrained_model']))
    
    # Construction de la fonction de perte
    loss_class = build_loss(config['Loss'])
    
    # Construction de l'optimiseur
    optimizer, lr_scheduler = build_optimizer(
        config['Optimizer'],
        epochs=config['Global']['epoch_num'],
        step_each_epoch=config['Global']['save_epoch_step'],
        model=model)
    
    # Construction du post-traitement
    post_process_class = build_post_process(config['PostProcess'])
    
    # Construction de la métrique d'évaluation
    eval_class = build_metric(config['Metric'])
    
    # Chargement des données
    train_dataloader = build_dataloader(config, 'Train', device, logger)
    
    if config['Eval']:
        eval_dataloader = build_dataloader(config, 'Eval', device, logger)
    else:
        eval_dataloader = None

    #Calcul de step_pre_epoch
    # step_pre_epoch = len(train_dataloader) // Config['Global']['epoch_num']
    step_pre_epoch = len(train_dataloader)    
    
    # Lancement de l'entraînement
    train(
        config,
        train_dataloader,
        valid_dataloader=eval_dataloader,
        device=device,
        model=model,
        loss_class=loss_class,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        post_process_class=post_process_class,
        eval_class=eval_class,
        pre_best_model_dict={},
        logger=logger,
        log_writer=log_writer,
        step_pre_epoch=step_pre_epoch)
    
    #Exportation du  modèle après l'entraînement
    export_model(config)


if __name__ == "__main__":
    config_file = '../config/fine_tuning_config.yml'
    fine_tune_paddleocr(config_file)
    