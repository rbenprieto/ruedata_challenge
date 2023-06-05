from typing import List, Dict, Any
from collections import deque


def find_shortest_possible_key(attempts_login: List[str]) -> str:
    """
    Function to perform the validations and generate the code recursively
    """

    # Diccionarios para apendear data
    graph: Dict[str, List[str]] = {}
    in_degree: Dict[str, int] = {}

    # Iteracion sobre cada intento de login
    for attempt in attempts_login:
        # Iteracion sobre el index de cada intento de login
        for i in range(len(attempt) - 1):
            # Obtiene el número del actual index y el proximo
            node = attempt[i]
            adjacent_node = attempt[i + 1]

            # Evalua si el nodo no está en el grafo y lo asigna de ser necesario
            if node not in graph:
                graph[node] = []
                in_degree[node] = 0

            # Verifica que el nodo del proximo indice sea una relación del actual indice, se asigna como conexión y aumenta la cantidad de nodos adjacentes
            if adjacent_node not in graph[node]:
                graph[node].append(adjacent_node)
                in_degree[adjacent_node] = in_degree.get(adjacent_node, 0) + 1

    # Genera una lista de los nodos que no tengan conexiones de entrada
    node_list = [node for node in graph if in_degree[node] == 0]
    sorted_result = []

    while node_list:
        # Sacar el primer nodo de la lista para appendear
        node = node_list.pop(0)
        sorted_result.append(node)

        # Actualizar el grado de entrada de los nodos adyacentes y si es cero appendearlo a la lista
        for adjacent_node in graph.get(node, []):
            in_degree[adjacent_node] -= 1
            if in_degree[adjacent_node] == 0:
                node_list.append(adjacent_node)

    # Concatena el resultado y lo convierte a entero
    return int("".join(sorted_result))
