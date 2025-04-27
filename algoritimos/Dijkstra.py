import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = [] 
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

# Implementação do algoritmo de Dijkstra
def dijkstra(graph, start):

    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    predecessors = {node: None for node in graph}
    
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, predecessors

def shortest_path(graph, start, goal):
    distances, predecessors = dijkstra(graph, start)
    
    path = []
    current_node = goal
    while current_node is not None:
        path.insert(0, current_node)
        current_node = predecessors[current_node]
    
    if distances[goal] == float('infinity'):
        return None, float('infinity')
    
    return path, distances[goal]

def print_path(path):
    if path is None:
        print("Caminho não encontrado.")
    else:
        print(" -> ".join(path))

if __name__ == "__main__":
    # Criando um grafo
    g = Graph()

    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 1)

    path, distance = shortest_path(g.graph, 'A', 'D')
    print(f"Caminho mínimo de A a D: {path}, Distância: {distance}")
    print_path(path)
