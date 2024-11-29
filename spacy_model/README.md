# Project README

## **Entraînez et Traitez les Données des Gares avec spaCy NER**

Ce projet est conçu pour entraîner un modèle de traitement du langage naturel (NLP) avec spaCy afin de reconnaître les noms de gares dans des textes en français. Il inclut des fonctionnalités pour générer des données d’entraînement, entraîner un modèle personnalisé de reconnaissance d’entités nommées (NER) et utiliser ce modèle pour extraire les gares dans un texte donné.

---

## **Fonctionnalités**

1. **Entraînement d’un modèle NER personnalisé** :
   - Génère des ensembles de données d’entraînement et de validation basés sur des noms de gares réels.
   - Utilise spaCy pour entraîner un modèle qui reconnaît les noms de gares.

2. **Traitement de texte utilisateur** :
   - Permet d’extraire les noms de gares d’un texte donné en utilisant le modèle entraîné.
   - Étiquette les gares comme `start` (départ), `intermediate` (intermédiaire) ou `end` (arrivée) selon leur ordre dans le texte.

3. **Métriques et Résultats** :
   - Affiche les métriques d’entraînement et de validation à chaque itération.
   - Sauvegarde les métriques (e.g., précision, perte) dans un fichier Excel pour analyse.

---

## **Prérequis**

### **Version de Python** :
- Python 3.8 ou supérieur

### **Dépendances** :
Les bibliothèques suivantes sont nécessaires :
- `spacy`
- `pandas`
- `argparse`
- `openpyxl` (pour exporter les métriques au format Excel)

Installez les dépendances avec la commande suivante :
```bash
pip install -r requirements.txt
```

---

## **Structure du projet**

```
project/
│
├── main.py                        # Point d’entrée pour l’entraînement et le traitement de texte
│
├── helpers/
│   ├── text_processor.py          # Traite le texte et extrait les entités de type gare
│   ├── sentence_generator.py      # Génère les phrases pour l’entraînement et la validation
│   ├── __init__.py
│
├── train/
│   ├── train_model.py             # Gère l’entraînement et l’évaluation du modèle
│   ├── __init__.py
│
├── utils/
│   ├── file_handler.py            # Charge les données des gares depuis un fichier CSV
│   ├── data_converter.py          # Convertit les données au format spaCy
│   ├── __init__.py
│
├── config/
│   ├── constants.py               # Définit les chemins et configurations
│   ├── __init__.py
│
├── data/
│   ├── liste-des-gares.csv        # Fichier CSV contenant les noms des gares
│   ├── sentence_templates.txt     # Templates de phrases pour générer les données d’entraînement
│
├── output/
│   ├── data/
│   │   ├── training_data.spacy    # Données d’entraînement sérialisées
│   │   ├── validation_data.spacy  # Données de validation sérialisées
│   │
│   ├── training_metrics.xlsx      # Fichier Excel contenant les métriques d’entraînement
│
├── model/                         # Répertoire pour le modèle spaCy entraîné
```

---

## **Utilisation**

### **1. Entraîner le modèle**
Exécutez la commande suivante pour entraîner le modèle NER :
```bash
python main.py
```

Cela effectue les étapes suivantes :
1. Charge les données des gares depuis `liste-des-gares.csv`.
2. Génère les ensembles de données d’entraînement et de validation à l’aide de `sentence_templates.txt`.
3. Entraîne le modèle pendant un certain nombre d’itérations (epochs).
4. Sauvegarde le modèle entraîné dans le répertoire `model/`.
5. Sauvegarde les métriques d’entraînement (e.g., précision, perte) dans `training_metrics.xlsx`.

---

### **2. Traiter un texte utilisateur**
Exécutez la commande suivante pour extraire les noms des gares d’un texte donné :
```bash
python main.py -t "Je veux aller de Paris à Lyon en passant par Marseille."
```

**Exemple de sortie** :
```
Traitement du texte : Je veux aller de Paris à Lyon en passant par Marseille.
Résultat :
[
    {"status": "start", "station": "paris"},
    {"status": "intermediate", "station": "marseille"},
    {"status": "end", "station": "lyon"}
]
```

---

## **Configuration**

Modifiez `config/constants.py` pour personnaliser les paramètres du projet :

| Constante              | Description                                            | Valeur par défaut                     |
|------------------------|--------------------------------------------------------|---------------------------------------|
| `CSV_PATH`             | Chemin vers le fichier CSV contenant les noms des gares. | `../data/liste-des-gares.csv`         |
| `TEMPLATES_PATH`       | Chemin vers le fichier de templates de phrases.         | `../data/sentence_templates.txt`      |
| `TRAIN_SPACY_PATH`     | Chemin pour sauvegarder les données d’entraînement sérialisées. | `./output/data/training_data.spacy` |
| `VAL_SPACY_PATH`       | Chemin pour sauvegarder les données de validation sérialisées. | `./output/data/validation_data.spacy` |
| `OUTPUT_MODEL_DIR`     | Répertoire pour sauvegarder le modèle entraîné.         | `./model/`                            |
| `METRIC_OUTPUT`        | Chemin pour sauvegarder les métriques d’entraînement au format Excel. | `./output/training_metrics.xlsx`  |
| `N_ITER`               | Nombre d’itérations d’entraînement (epochs).           | `10`                                  |

---

## **Développement**

### **Ajouter plus de templates de phrases**
Pour améliorer la précision du modèle, ajoutez des phrases plus diversifiées et complexes dans `data/sentence_templates.txt`. Chaque ligne doit suivre le format :
```plaintext
Je veux aller de {station1} à {station2}.
De {station1}, je prends le train pour {station2}.
```

### **Augmenter la taille des ensembles de données**
Vous pouvez augmenter le nombre d’échantillons d’entraînement et de validation en modifiant le paramètre `n` dans les appels à la fonction `generate_training_data` dans `main.py`.

---

## **Métriques de sortie**

Le processus d’entraînement sauvegarde les métriques dans un fichier Excel (`training_metrics.xlsx`) avec les colonnes suivantes :

| **Colonne**            | **Description**                                        |
|------------------------|--------------------------------------------------------|
| `Epoch`                | L’itération actuelle d’entraînement.                   |
| `training_precision`  | Score de précision sur les données d’entraînement.     |
| `training_loss`       | Valeur de la perte sur les données d’entraînement.     |
| `validation_precision` | Score de précision sur les données de validation.      |
| `validation_loss`     | Valeur de la perte sur les données de validation.      |

