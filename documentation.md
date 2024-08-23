# Documentation du Projet d'Analyse de Plaques Signalétiques

## Vue d'ensemble

Ce projet vise à développer une application web pour l'analyse automatique de plaques signalétiques. L'application utilise des techniques de vision par ordinateur et d'apprentissage automatique pour extraire des informations clés des images de plaques signalétiques.

## Architecture

Le projet est divisé en trois parties principales :

1. Frontend (React)
2. Backend (FastAPI)
3. Modèles d'apprentissage automatique

### Structure du Projet
projet/
│
├── App/
│   ├── backend/
│   │   ├── models/
│   │   ├── main.py
│   │   └── classification_service.py
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   └── App.js
│   │   └── package.json
│   ├── data/
│   └── config/
│
├── classifier/
│   └── train_model.py
│
└── README.md

## Frontend

Le frontend est développé avec React et comprend les fonctionnalités suivantes :

- Menu latéral pour la navigation
- Pages pour la détection d'objets, la classification de texte et la génération d'images
- Interface utilisateur réactive et moderne

## Backend

Le backend est construit avec FastAPI et gère les fonctionnalités suivantes :

- API pour la détection d'objets
- API pour la classification de texte
- API pour la génération d'images (à implémenter)

## Modèles d'Apprentissage Automatique

### Modèle de Classification de Texte

- Entraîné séparément dans le dossier `classifier`
- Utilise TF-IDF et SVM pour la classification multi-labels
- Extrait le fabricant, le modèle, le numéro de série et la date des plaques signalétiques

### Modèle de Détection d'Objets (à implémenter)

- Prévu pour détecter et localiser les éléments clés sur les plaques signalétiques

### Modèle de Génération d'Images (à implémenter)

- Prévu pour générer de nouvelles images de plaques signalétiques

## Utilisation

1. Entraînement du modèle de classification :
cd classifier
python train_model.py

2. Lancement du backend :
cd App/backend
uvicorn main:app --reload

3. Lancement du frontend :

cd App/frontend
npm start

## Prochaines Étapes

1. Finaliser l'intégration du modèle de classification dans le backend
2. Développer et intégrer le modèle de détection d'objets
3. Créer et intégrer le modèle de génération d'images
4. Améliorer l'interface utilisateur du frontend
5. Tester et optimiser l'ensemble du système

## Conclusion

Ce projet combine des technologies de pointe en vision par ordinateur, traitement du langage naturel et développement web pour créer une solution complète d'analyse de plaques signalétiques. Une fois terminé, il offrira une plateforme puissante et flexible pour l'extraction automatique d'informations à partir d'images de plaques signalétiques.