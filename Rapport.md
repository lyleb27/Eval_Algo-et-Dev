# 3. Partie 2 : Architecture de l’agent IA

## 3.1 Choix de l’architecture

### Architecture retenue : Agent apprenant (Q-learning / DQN)

**Justification du choix :**  
Le jeu Snake est un environnement séquentiel, dynamique et partiellement observable.  
L’agent doit prendre des décisions à long terme afin de maximiser le score tout en évitant les situations dangereuses.

Comparaison avec les autres architectures :
- **Agent réactif simple** : décisions locales, pas d’anticipation.
- **Agent à buts** : le but (atteindre la nourriture) peut mener à des situations mortelles.
- **Agent basé sur l’utilité** : difficile de définir une fonction d’utilité précise.
- **Agent apprenant** : apprend par interaction et optimise les décisions à long terme.

L’agent apprenant est donc le plus adapté pour gérer la complexité du jeu Snake.

---

### Composants de l’architecture

1. **Perception (état)**
   - Position de la tête du serpent  
   - Direction actuelle  
   - Position de la nourriture  
   - Présence d’obstacles (mur, corps)  
   - Informations locales (danger devant/gauche/droite)

2. **Espace d’actions**
   - Avancer tout droit  
   - Tourner à gauche  
   - Tourner à droite  

3. **Fonction de récompense**
   - +10 : manger une pomme  
   - −10 ou −100 : collision  
   - −0.01 : pénalité par pas (efficacité)

4. **Fonction de décision**
   - Politique ε-greedy  
   - Sélection de l’action maximisant la valeur Q

5. **Mécanisme d’apprentissage**
   - Q-learning (Q-table)  
   - ou Deep Q-Network (réseau de neurones)

---

## 3.2 Problématique d’apprentissage

### Problématique choisie : Exploration vs exploitation

**Formulation :**  
L’agent doit trouver un compromis entre :
- **explorer** de nouvelles actions pour améliorer ses connaissances,
- **exploiter** les stratégies déjà apprises pour maximiser le score.

Dans Snake, une mauvaise décision peut avoir des conséquences plusieurs coups plus tard.

---

### Intérêt et difficulté

Cette problématique est intéressante car :
- l’environnement est déterministe,
- les erreurs sont souvent irréversibles,
- l’espace d’états augmente avec la longueur du serpent.

Elle est difficile car :
- trop d’exploitation mène à des impasses,
- trop d’exploration réduit les performances,
- le réglage du paramètre ε est critique.

---

## 3.3 Intégration avec l’algorithme génétique

### Combinaison agent IA / algorithme génétique

L’algorithme génétique (AG) est utilisé pour optimiser les paramètres globaux de l’agent, tandis que le Q-learning/DQN gère l’apprentissage par interaction.

---

### Éléments optimisés par l’algorithme génétique

- Taux d’apprentissage (α)  
- Facteur d’actualisation (γ)  
- Paramètre d’exploration (ε)  
- Pondérations de la fonction de récompense  
- Poids initiaux du réseau de neurones (DQN)

---

### Schéma d’interaction

1. Génération d’une population d’agents (AG)
2. Évaluation de chaque agent sur plusieurs parties de Snake
3. Calcul de la fitness (score moyen)
4. Sélection, croisement et mutation
5. Entraînement fin des meilleurs agents par Q-learning/DQN

### Schéma d’interaction entre l’algorithme génétique et l’agent IA

Le schéma suivant illustre la combinaison entre l’algorithme génétique (optimisation globale)
et l’agent apprenant par Q-learning (apprentissage local).

```
┌─────────────────────────────────────────────────────┐
│          ALGORITHME GÉNÉTIQUE (méta-niveau)         │
│  Génome = [α, γ, ε_decay, poids_récompenses, ...]   │
└─────────────────────────────────────────────────────┘
                         │
                         ↓ Initialise
        ┌────────────────────────────────────┐
        │  Population d'agents Q-learning    │
        │  - Agent₁ (gènes₁) → joue N parties│
        │  - Agent₂ (gènes₂) → joue N parties│
        │  - Agent₃ (gènes₃) → joue N parties│
        └────────────────────────────────────┘
                         │
                         ↓ Évalue fitness
        ┌────────────────────────────────────┐
        │ Fitness = moyenne(score) + bonus   │
        │ bonus = parties longues + stabilité│
        └────────────────────────────────────┘
                         │
                         ↓ Sélection / Croisement / Mutation
                      Nouvelle génération

```
Le schéma met en évidence :
- le rôle de l’algorithme génétique comme optimiseur de paramètres,
- l’apprentissage par interaction réalisé par chaque agent,
- la boucle évolutive permettant d’améliorer progressivement la population.

---

### Compromis temps d’apprentissage / performance

Pour réduire le temps de calcul :
- limiter le nombre d’épisodes par agent,
- utiliser l’AG uniquement pour l’optimisation globale,
- confier l’apprentissage long terme au Q-learning,
- paralléliser les évaluations si possible.

---

## Conclusion

L’architecture basée sur un **agent apprenant couplé à un algorithme génétique** est la mieu adaptée au jeu Snake.  
Elle permet de combiner :
- une exploration globale efficace,
- un apprentissage progressif et précis,
- de bonnes performances à long terme.
  
  
Lebourcq Lyse