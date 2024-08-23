import os
import subprocess

class DetectionService:
    def __init__(self):
        self.paddle_ocr_path = '../PaddleOCR'
        self.configs = {
            "Model EAST + Mobile": {
                "config": "../../EAST/config/det_mv3_east.yml",
                "model": "../../EAST/models/det_mv3_east_v2.0_train/best_accuracy.pdparams",
                "output": "../../EAST/output/det_east_mobile/det_results"
            },
            "Model EAST + RESNet": {
                "config": "../../EAST/config/det_r50_vd_east.yml",
                "model": "../../EAST/models/det_r50_vd_east_v2.0_trai/best_accuracy.pdparams",
                "output": "../../EAST/output/det_east_resnet/det_results"
            }
        }

    def detect(self, image_path: str, model_name: str):
        if model_name == "Model e2e":
            return "Détection en cours..."

        config = self.configs.get(model_name)
        if not config:
            return "Modèle non reconnu"

        command = [
            "python", 
            os.path.join(self.paddle_ocr_path, "tools", "infer_det.py"),
            "-c", os.path.join(self.paddle_ocr_path, config['config']),
            "-o", f"Global.infer_img={image_path}",
            f"Global.pretrained_model={os.path.join(self.paddle_ocr_path, config['model'])}",
            "PostProcess.box_thresh=0.6",
            "PostProcess.unclip_ratio=2.0"
        ]

        try:
            #subprocess.run(command, check=True, cwd=self.paddle_ocr_path)
            
            # Trouver le fichier de résultat le plus récent
            result_dir = os.path.join(self.paddle_ocr_path, config['output'])
            result_files = [f for f in os.listdir(result_dir) if f.endswith('.jpg')]
            if not result_files:
                return "Aucun résultat trouvé"
            
            latest_file = max(result_files, key=lambda f: os.path.getmtime(os.path.join(result_dir, f)))
            result_path = os.path.join(config['output'], latest_file)

            return result_path
        except subprocess.CalledProcessError as e:
            return f"Erreur lors de la détection : {str(e)}"

detection_service = DetectionService()