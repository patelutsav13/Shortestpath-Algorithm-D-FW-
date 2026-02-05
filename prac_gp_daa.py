# ============================================================
# DAA GROUP PROJECT
# TITLE: Shortest Path Algorithms (User Input Based)
# ALGORITHMS: Dijkstra & Floyd-Warshall
# GRAPH VISUALIZATION: NetworkX
# LANGUAGE: Python
# ============================================================

import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt


# -------------------------------
# SAFE INPUT FUNCTIONS
# -------------------------------
def safe_int(msg):
    while True:
        val = input(msg)
        if val.isdigit():
            return int(val)
        print("<<<<===== INVALID INPUT! ENTER ONLY INTEGER =====>>>>")


def safe_str(msg):
    while True:
        val = input(msg)
        if val.isalpha():
            return val
        print("<<<<===== INVALID INPUT! ENTER ONLY STRING =====>>>>")


# -------------------------------
# GRAPH INPUT MODULE
# -------------------------------
def input_graph():
    print("\n=====> GRAPH INPUT MODULE <=====")

    n = safe_int("Enter number of vertices: ")
    vertices = []

    print("~~~~~>>>> ENTER VERTEX NAMES <<<<<~~~~~")
    for i in range(n):
        vertices.append(safe_str(f"Vertex {i+1}: "))

    graph = {v: {} for v in vertices}

    e = safe_int("Enter number of edges: ")
    print("~~~~~>>>> ENTER EDGES (source destination weight) <<<<<~~~~~")

    for _ in range(e):
        while True:
            data = input().split()
            if len(data) != 3:
                print("<<<<===== INVALID FORMAT! USE: src dest weight =====>>>>")
                continue

            u, v, w = data
            if u not in vertices or v not in vertices:
                print("<<<<===== INVALID VERTEX NAME =====>>>>")
                continue
            if not w.isdigit():
                print("<<<<===== WEIGHT MUST BE INTEGER =====>>>>")
                continue

            graph[u][v] = int(w)  # Directed graph
            break

    return graph, vertices


# -------------------------------
# DIJKSTRA ALGORITHM MODULE
# -------------------------------
def dijkstra(graph, start):
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)

        if current_dist > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances


# -------------------------------
# FLOYD-WARSHALL ALGORITHM MODULE
# -------------------------------
def floyd_warshall(graph, vertices):
    n = len(vertices)
    dist = [[sys.maxsize]*n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for i in range(n):
        for j in graph[vertices[i]]:
            dist[i][vertices.index(j)] = graph[vertices[i]][j]

    # Store all intermediate matrices
    all_matrices = []
    
    # D0 - Initial matrix
    import copy
    all_matrices.append(copy.deepcopy(dist))

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
        
        # Store matrix after considering vertex k
        all_matrices.append(copy.deepcopy(dist))

    return dist, all_matrices


# -------------------------------
# DISPLAY MODULE
# -------------------------------
def display_dijkstra(distances, source):
    print("\n=====> DIJKSTRA'S FINAL OUTPUT <=====")
    print(f"Source Vertex: {source}")
    for v in distances:
        print(f"Shortest distance from {source} to {v} = {distances[v]}")


def display_floyd(dist, vertices, all_matrices):
    print("\n=====> FLOYD-WARSHALL STEP-BY-STEP OUTPUT <=====")
    
    # Display all intermediate matrices
    for idx, matrix in enumerate(all_matrices):
        if idx == 0:
            print(f"\n*** D{idx} (Initial Distance Matrix) ***")
        else:
            print(f"\n*** D{idx} (After considering vertex '{vertices[idx-1]}' as intermediate) ***")
        
        print("     ", end="")
        for v in vertices:
            print(f"{v:>6}", end="")
        print()
        
        for i in range(len(vertices)):
            print(f"{vertices[i]:>5}", end="")
            for j in range(len(vertices)):
                if matrix[i][j] == sys.maxsize:
                    print("  INF ", end="")
                else:
                    print(f"{matrix[i][j]:6}", end="")
            print()
    
    print("\n=====> FLOYD-WARSHALL FINAL OUTPUT <=====")
    print("All Pairs Shortest Path Matrix:")
    print("     ", end="")
    for v in vertices:
        print(f"{v:>6}", end="")
    print()

    for i in range(len(vertices)):
        print(f"{vertices[i]:>5}", end="")
        for j in range(len(vertices)):
            if dist[i][j] == sys.maxsize:
                print("  INF ", end="")
            else:
                print(f"{dist[i][j]:6}", end="")
        print()


# -------------------------------
# GRAPH VISUALIZATION
# -------------------------------
def draw_main_graph(graph):
    print("\n~~~~~>>>> MAIN GRAPH (ORIGINAL) <<<<<~~~~~")
    G = nx.DiGraph()

    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v, weight=graph[u][v])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=2000, arrows=True)
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels=nx.get_edge_attributes(G, 'weight'))

    plt.title("Main Graph (Original User Input)")
    plt.show()


def draw_final_graph(distances, source):
    print("\n~~~~~>>>> FINAL GRAPH (AFTER SHORTEST PATH) <<<<<~~~~~")
    G = nx.DiGraph()

    for node, cost in distances.items():
        if node != source and cost != sys.maxsize:
            G.add_edge(source, node, weight=cost)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen',
            node_size=2000, arrows=True)
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels=nx.get_edge_attributes(G, 'weight'))

    plt.title("Final Graph After Shortest Path (Dijkstra Result)")
    plt.show()


# -------------------------------
# MAIN MENU
# -------------------------------
def main():
    print("<<<<===== DAA GROUP PROJECT: SHORTEST PATH ALGORITHMS =====>>>>")

    graph, vertices = input_graph()
    last_dijkstra = None
    last_source = None

    while True:
        print("\n~~~~~>>>> MAIN MENU <<<<<~~~~~")
        print("1. Dijkstra's Algorithm (Single Source)")
        print("2. Floyd-Warshall Algorithm (All Pairs)")
        print("3. Show Main Graph")
        print("4. Show Final Graph (After Shortest Path)")
        print("5. Exit")

        choice = safe_int("Enter choice: ")

        if choice == 1:
            source = safe_str("Enter source vertex: ")
            if source not in vertices:
                print("<<<<===== INVALID SOURCE VERTEX =====>>>>")
                continue
            last_source = source
            last_dijkstra = dijkstra(graph, source)
            display_dijkstra(last_dijkstra, source)

        elif choice == 2:
            fw_result, all_matrices = floyd_warshall(graph, vertices)
            display_floyd(fw_result, vertices, all_matrices)

        elif choice == 3:
            draw_main_graph(graph)

        elif choice == 4:
            if last_dijkstra is None:
                print("<<<<===== RUN DIJKSTRA FIRST =====>>>>")
            else:
                draw_final_graph(last_dijkstra, last_source)

        elif choice == 5:
            print("<<<<===== EXITING PROJECT =====>>>>")
            break

        else:
            print("<<<<===== INVALID MENU CHOICE =====>>>>")


# Program Execution Starts Here
main()
