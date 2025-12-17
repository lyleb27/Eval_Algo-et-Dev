# Snake - Algorithme Génétique 🐍🧬

Implémentation d'un algorithme génétique pour entraîner un agent à jouer au Snake en utilisant des réseaux neuronaux.

## 📋 Structure du projet

```
snake-genetic-algorithm/
├── main.py                  # Point d'entrée du programme
├── genetic_algorithm.py     # Implémentation de l'AG
├── snake.py                # Logique du serpent
├── neural_network.py       # Réseau neuronal
├── game.py                 # Logique du jeu
├── config.py               # Configuration
└── utils.py                # Utilitaires (graphiques)
```

## 🚀 Installation

```bash
pip install pygame numpy matplotlib
```

## ▶️ Utilisation

### Lancer l'entraînement

```bash
python main.py
```

## 🧬 Algorithme Génétique

### 1. Évaluation (`evaluate`)

Chaque serpent joue une partie complète et calcule sa fitness :

```python
fitness = score² × 100 + steps × 0.1 - steps_without_food × 0.5
```

**Composantes** :
- **Score** : Récompense exponentielle pour manger (encourage fortement)
- **Survie** : Petite récompense pour rester en vie
- **Efficacité** : Pénalité pour tourner sans manger

### 3. Reproduction (`reproduce`)

**Crossover (70%)** :
```python
# Combine les poids de deux parents
mask = random > 0.5
child_weights = where(mask, parent1_weights, parent2_weights)
```

**Mutation (10%)** :
```python
# Modifie aléatoirement certains poids
if random < mutation_rate:
    weight += random_normal() × strength
```

## 🧠 Réseau Neuronal

### Architecture

```
Input Layer (12 neurones)
    ↓
Hidden Layer (16 neurones, Leaky ReLU)
    ↓
Output Layer (4 neurones, Softmax)
```

## ⚙️ Paramètres configurables

Dans `main.py` :

```python
POPULATION_SIZE = 50      # Taille de la population
NUM_GENERATIONS = 100     # Nombre de générations
MUTATION_RATE = 0.1       # Taux de mutation (10%)
CROSSOVER_RATE = 0.7      # Taux de crossover (70%)
ELITISM = 2               # Nombre d'élites conservés
```

Dans `config.py` :

```python
GRID_WIDTH = 30           # Largeur de la grille
GRID_HEIGHT = 20          # Hauteur de la grille
MAX_STEPS_WITHOUT_FOOD = 150  # Limite sans manger
```

## 📊 Résultats attendus

- **Générations 1-10** : Apprentissage de base (survie)
- **Générations 11-30** : Début de capture de nourriture
- **Générations 31-50** : Amélioration de l'efficacité
- **Générations 51+** : Optimisation fine

## 📈 Graphiques

Le programme génère automatiquement :
- Évolution de la meilleure fitness
- Moyenne mobile
- Statistiques finales
