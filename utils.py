# utils.py
import matplotlib.pyplot as plt
import numpy as np

def plot_fitness(history, save_path=None):
    """
    Affiche un graphique de l'évolution de la fitness
    
    Args:
        history: Liste des meilleures fitness par génération
        save_path: Chemin pour sauvegarder le graphique (optionnel)
    """
    if len(history) == 0:
        print("Aucune donnée à afficher")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Graphique principal
    plt.subplot(1, 2, 1)
    plt.plot(history, linewidth=2, color='blue', label='Meilleure fitness')
    
    # Ajouter une moyenne mobile si assez de données
    if len(history) > 10:
        window = min(10, len(history) // 5)
        moving_avg = np.convolve(history, np.ones(window)/window, mode='valid')
        plt.plot(range(window-1, len(history)), moving_avg, 
                linewidth=2, color='red', linestyle='--', label=f'Moyenne mobile ({window})')
    
    plt.title("Évolution de la fitness par génération", fontsize=14, fontweight='bold')
    plt.xlabel("Génération", fontsize=12)
    plt.ylabel("Fitness", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Statistiques
    plt.subplot(1, 2, 2)
    stats_text = f"""
    STATISTIQUES FINALES
    
    Nombre de générations: {len(history)}
    
    Meilleure fitness: {max(history):.2f}
    Génération optimale: {history.index(max(history)) + 1}
    
    Fitness initiale: {history[0]:.2f}
    Fitness finale: {history[-1]:.2f}
    Amélioration: {((history[-1] - history[0]) / history[0] * 100):.1f}%
    
    Fitness moyenne: {np.mean(history):.2f}
    Écart-type: {np.std(history):.2f}
    """
    
    plt.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', 
             facecolor='wheat', alpha=0.5))
    plt.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Graphique sauvegardé: {save_path}")
    
    plt.show()

def print_generation_summary(generation, best_fitness, avg_fitness, best_score, avg_score):
    """
    Affiche un résumé formaté d'une génération
    
    Args:
        generation: Numéro de la génération
        best_fitness: Meilleure fitness
        avg_fitness: Fitness moyenne
        best_score: Meilleur score
        avg_score: Score moyen
    """
    print(f"\n{'='*60}")
    print(f"GÉNÉRATION {generation}")
    print(f"{'='*60}")
    print(f"  Meilleure fitness: {best_fitness:>10.2f} | Score: {best_score:>3}")
    print(f"  Fitness moyenne:   {avg_fitness:>10.2f} | Score moyen: {avg_score:>6.2f}")
    print(f"{'='*60}")