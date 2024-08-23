from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.detection_service import DetectionService
from services.classification_service import ClassificationService
import services.classification_service
from pydantic import BaseModel
import os
import shutil
import random

app = FastAPI()

GENERATED_IMAGES_DIR = os.path.join(os.path.dirname(__file__), "generated_images")


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes
    allow_headers=["*"],  # Permet tous les headers
)


# Configurez ce chemin pour servir les images statiques
static_path = "./static"
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/generated_images", StaticFiles(directory=GENERATED_IMAGES_DIR), name="generated_images")
# Initialisation du service de classification
detection_service = DetectionService()
classification_service = ClassificationService()

@app.post("/detect")
async def detect_text(file: UploadFile = File(...), model: str = Form(...)):
    temp_file = f"temp_{file.filename}"
    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = detection_service.detect(temp_file, model)
        
        if model == "Model e2e" or result.startswith("Erreur") or result == "Aucun résultat trouvé":
            return {"message": result}
        else:
            # Copier le fichier résultat dans le dossier static
            static_file = f"static/result_{os.path.basename(result)}"
            shutil.copy(os.path.join(detection_service.paddle_ocr_path, result), static_file)
            return {"image_url": f"/{static_file}"}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)



@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'analyse de plaques signalétiques"}


class ClassificationRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify_text(request: ClassificationRequest):
    result = classification_service.classify(request.text)
    return result

@app.get("/generate")
async def get_random_generated_image():
    images = [f for f in os.listdir(GENERATED_IMAGES_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        return {"error": "Aucune image générée disponible"}
    random_image = random.choice(images)
    return {"image_url": f"/generated_images/{random_image}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)