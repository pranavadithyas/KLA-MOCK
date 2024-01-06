import networkx as nx
import json

data_path = "C:/Users/TEMP/Downloads/level0.json"
output_path = "C:/21pw18/level0_output.json"

# Load data
with open(data_path) as data_file:
    graph_data = json.load(data_file)

G = nx.Graph()

for neighborhood in graph_data["neighbourhoods"]:
    G.add_node(neighborhood)

restaurant = list(graph_data["restaurants"])[0]
G.add_node(restaurant)

for neighborhood, data in graph_data["neighbourhoods"].items():
    distances = data["distances"]
    for i, distance in enumerate(distances):
        G.add_edge(neighborhood, f"n{i}", weight=distance)

restaurant_distances = graph_data["restaurants"][restaurant]["neighbourhood_distance"]
for i, distance in enumerate(restaurant_distances):
    G.add_edge(restaurant, f"n{i}", weight=distance)

def nearest_neighbor_algorithm(graph, start_node):
    path = [start_node]
    current_node = start_node
    visited = set([start_node])

    while len(path) < graph.number_of_nodes():
        neighbors = list(graph.neighbors(current_node))
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in visited]
        
        if not unvisited_neighbors:
            # If all neighbors are visited, go back to the start
            current_node = start_node
        else:
            nearest_neighbor = min(unvisited_neighbors, key=lambda neighbor: graph[current_node][neighbor]['weight'])
            path.append(nearest_neighbor)
            visited.add(nearest_neighbor)
            current_node = nearest_neighbor

    return path

def total_path_length(graph, path):
    length = 0
    for i in range(len(path) - 1):
        length += graph[path[i]][path[i + 1]]['weight']
    return length

def two_opt_swap(path, i, k):
    new_path = path[:i] + path[i:k+1][::-1] + path[k+1:]
    return new_path

def two_opt_algorithm(graph, path):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for k in range(i + 1, len(path)):
                if k - i == 1:
                    continue
                new_path = two_opt_swap(path, i, k)
                if total_path_length(graph, new_path) < total_path_length(graph, path):
                    path = new_path
                    improved = True
    return path

start_node = graph_data["vehicles"]["v0"]["start_point"]
nearest_neighbor_path = nearest_neighbor_algorithm(G, start_node)

print("Nearest neighbor path:", nearest_neighbor_path)

# Apply 2-opt optimization
optimized_path = two_opt_algorithm(G, nearest_neighbor_path)

print("Optimized path:", optimized_path)

# Save the output JSON to a file
output_data = {"v0": {"path": optimized_path}}
with open(output_path, "w") as output_file:
    json.dump(output_data, output_file)
