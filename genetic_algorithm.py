# genetic_algorithm.py
import random
from snake import Snake
from neural_network import NeuralNetwork
from game import Game
import pygame

class GeneticAlgorithm:
    def __init__(self, size=50, mutation_rate=0.1, crossover_rate=0.7, elitism_count=2):
        """
        Initialise l'algorithme génétique
        
        Args:
            size: Taille de la population
            mutation_rate: Probabilité de mutation (0.1 = 10%)
            crossover_rate: Probabilité de crossover (0.7 = 70%)
            elitism_count: Nombre des meilleurs individus à conserver
        """
        self.size = size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []

    def evaluate(self, screen=None, display=False):
        """
        Évalue tous les serpents de la population en les faisant jouer
        
        Args:
            screen: Surface pygame pour l'affichage (optionnel)
            display: Si True, affiche le jeu pendant l'évaluation
        
        Returns:
            float: Meilleure fitness de la génération
        """
        print(f"\n=== Génération {self.generation} ===")
        
        for i, snake in enumerate(self.population):
            # Réinitialiser le serpent
            snake.reset()
            
            # Créer un jeu pour ce serpent
            game = Game(snake)
            
            # Faire jouer le serpent jusqu'à sa mort
            while snake.alive:
                game.update()
                
                # Affichage optionnel
                if display and screen and i == 0:  # Afficher seulement le premier
                    game.draw(screen)
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)
            
            # Calculer la fitness
            snake.calculate_fitness()
            
            if (i + 1) % 10 == 0:
                print(f"  Évalué {i+1}/{self.size} serpents...")
        
        # Trier par fitness décroissante
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        
        # Mettre à jour la meilleure fitness
        best = self.population[0]
        self.best_fitness = best.fitness
        self.history.append(self.best_fitness)
        
        # Statistiques
        avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
        avg_score = sum(s.score for s in self.population) / len(self.population)
        
        print(f"  Meilleure fitness: {self.best_fitness:.2f} (Score: {best.score})")
        print(f"  Fitness moyenne: {avg_fitness:.2f}")
        print(f"  Score moyen: {avg_score:.2f}")
        
        return self.best_fitness

    def select(self, method="tournament", tournament_size=5):
        """
        Sélectionne les meilleurs individus pour la reproduction
        
        Args:
            method: Méthode de sélection ("tournament", "roulette", "rank")
            tournament_size: Taille du tournoi si method="tournament"
        
        Returns:
            list: Liste des serpents sélectionnés
        """
        selected = []
        
        # Toujours garder les meilleurs (élitisme)
        selected.extend(self.population[:self.elitism_count])
        
        # Sélectionner le reste selon la méthode choisie
        num_to_select = self.size - self.elitism_count
        
        if method == "tournament":
            # Sélection par tournoi
            for _ in range(num_to_select):
                # Choisir tournament_size individus au hasard
                tournament = random.sample(self.population, tournament_size)
                # Garder le meilleur
                winner = max(tournament, key=lambda s: s.fitness)
                selected.append(winner)
        
        elif method == "roulette":
            # Sélection par roulette
            total_fitness = sum(s.fitness for s in self.population)
            
            if total_fitness == 0:
                # Si toutes les fitness sont nulles, sélection aléatoire
                selected.extend(random.choices(self.population, k=num_to_select))
            else:
                # Probabilités proportionnelles à la fitness
                probabilities = [s.fitness / total_fitness for s in self.population]
                selected.extend(random.choices(
                    self.population, 
                    weights=probabilities, 
                    k=num_to_select
                ))
        
        elif method == "rank":
            # Sélection par rang (moins sensible aux outliers)
            ranks = list(range(len(self.population), 0, -1))
            total_rank = sum(ranks)
            probabilities = [r / total_rank for r in ranks]
            selected.extend(random.choices(
                self.population,
                weights=probabilities,
                k=num_to_select
            ))
        
        return selected

    def reproduce(self, selected):
        """
        Crée une nouvelle population à partir des individus sélectionnés
        
        Args:
            selected: Liste des serpents sélectionnés pour la reproduction
        
        Returns:
            list: Nouvelle population
        """
        new_population = []
        
        # Conserver les meilleurs (élitisme)
        for i in range(self.elitism_count):
            # Créer une copie du réseau neuronal
            elite_network = NeuralNetwork(weights=selected[i].network.get_weights())
            new_population.append(Snake(network=elite_network))
        
        # Créer le reste de la population
        while len(new_population) < self.size:
            # Sélectionner deux parents au hasard
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child_network = NeuralNetwork.crossover(
                    parent1.network, 
                    parent2.network
                )
            else:
                # Sinon, copier un parent
                child_network = NeuralNetwork(
                    weights=parent1.network.get_weights()
                )
            
            # Mutation
            child_network.mutate(self.mutation_rate)
            
            # Ajouter l'enfant à la nouvelle population
            new_population.append(Snake(network=child_network))
        
        # Mettre à jour la population et incrémenter la génération
        self.population = new_population
        self.generation += 1
        
        return new_population
    
    def run_generation(self, screen=None, display=False):
        """
        Exécute une génération complète: évaluation, sélection, reproduction
        
        Args:
            screen: Surface pygame pour l'affichage
            display: Si True, affiche le meilleur serpent
        
        Returns:
            float: Meilleure fitness de la génération
        """
        # 1. Évaluation
        best_fitness = self.evaluate(screen, display)
        
        # 2. Sélection
        selected = self.select(method="tournament")
        
        # 3. Reproduction
        self.reproduce(selected)
        
        return best_fitness