import matplotlib.pyplot as plt
import networkx as nx
from multiprocessing import Pool

def sum_pairs(pair):
    return sum(pair)

def visualize_tree(levels):
    G = nx.Graph()
    pos = {}
    labels = {}
    node_counter = 0
    
    for i, level in enumerate(levels):
        level_width = len(level)
        for j, value in enumerate(level):
            G.add_node(node_counter)
            pos[node_counter] = (j - level_width / 2, -i)
            labels[node_counter] = value
            node_counter += 1
    
    node_counter = 0
    next_node_counter = len(levels[0])
    
    for i in range(len(levels) - 1):
        for j in range(len(levels[i])):
            G.add_edge(node_counter, next_node_counter + j // 2)
            node_counter += 1
        next_node_counter += len(levels[i + 1])
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color='lightblue', font_size=10, font_weight='bold')

    # Add level annotations
    for i, level in enumerate(levels):
        plt.text(-len(level) / 2 - 1, -i, f"Step {i}", horizontalalignment='right', fontsize=12)
    
    plt.show()

def create_tree(base_layer):
    current_layer = base_layer
    levels = [current_layer[:]]
    
    while len(current_layer) > 1:
        # Form pairs of the current layer
        pairs = [(current_layer[i], current_layer[i + 1]) for i in range(0, len(current_layer), 2)]
        
        # Use multiprocessing to sum the pairs
        with Pool() as pool:
            next_layer = pool.map(sum_pairs, pairs)
        
        current_layer = next_layer
        levels.append(current_layer[:])
        visualize_tree(levels)
    
    return current_layer[0]

# Example usage:
if __name__ == '__main__':
    N = 8  # Example value, must be a power of 2
    base_layer = [i for i in range(1, N + 1)]  # Example base layer

    print("Base Layer:", base_layer)
    root_value = create_tree(base_layer)
    print("Root Value:", root_value)
