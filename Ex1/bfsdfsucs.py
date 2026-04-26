from collections import deque
import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")

    def add_edge(self, u, v, cost=0):
        if u in self.graph and v in self.graph:
            # Check if edge (u, v) already exists
            if any(neighbor == v for neighbor, _ in self.graph[u]):
                print(f"Edge from '{u}' to '{v}' already exists.")
            else:
                self.graph[u].append((v, cost))
                self.graph[v].append((u, cost))  # Assuming undirected graph
                print(f"Edge added between '{u}' and '{v}' with cost {cost}.")
        else:
            print("Add nodes first for edge creation.")

    def delete_node(self, node):
        if node in self.graph:
            del self.graph[node]
            # Remove all edges connected to the deleted node
            for n in self.graph:
                self.graph[n] = [(x, c) for x, c in self.graph[n] if x != node]
            print(f"Node '{node}' deleted.")
        else:
            print(f"Node '{node}' not found.")

    def delete_edge(self, u, v):
        edge_deleted = False
        if u in self.graph:
            initial_len_u = len(self.graph[u])
            self.graph[u] = [(x, c) for x, c in self.graph[u] if x != v]
            if len(self.graph[u]) < initial_len_u:  # Check if u->v was removed
                edge_deleted = True

        if v in self.graph:  # Remove v->u for undirected graph
            initial_len_v = len(self.graph[v])
            self.graph[v] = [(x, c) for x, c in self.graph[v] if x != u]
            if len(self.graph[v]) < initial_len_v:  # Check if v->u was removed
                edge_deleted = True

        if edge_deleted:
            print(f"Edge between '{u}' and '{v}' deleted.")
        else:
            print(f"Edge between '{u}' and '{v}' not found.")

    def display(self):
        print("\nGraph Adjacency List:")
        if not self.graph:
            print("Graph is empty.")
            return
        for node in sorted(self.graph.keys()):  # Display nodes in sorted order
            print(f"{node}: {self.graph[node]}")

    def display_adj_list(self, node):
        if node in self.graph:
            print(f"Adjacency list for '{node}': {self.graph[node]}")
        else:
            print(f"Node '{node}' not found.")

    def _print_table_header(self):
        print("\n" + "=" * 80)
        print(
            f"{'Iteration':<10} | {'Fringe (Nodes)':<30} | "
            f"{'Explored (Nodes)':<20} | {'Current Node':<15}"
        )
        print("-" * 80)

    def _print_table_row(self, iteration, fringe, explored, current_node):
        fringe_str = ", ".join([n for n, _ in fringe])  # Only display nodes in fringe
        explored_str = ", ".join(explored)
        print(
            f"{iteration:<10} | {fringe_str:<30} | "
            f"{explored_str:<20} | {current_node:<15}"
        )

    # ---------------- BFS ---------------- #

    def bfs_lr(self, start, goal_node=None):
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return

        explored = set()
        fringe = deque([(start, [start])])  # (node, path)
        found_goal = False
        iteration = 0

        print(f"\n--- BFS (Left-to-Right) from {start} ---")
        self._print_table_header()

        traversal_order = []

        while fringe:
            iteration += 1
            current_fringe_snapshot = list(fringe)  # For table display
            current_explored_snapshot = set(explored)  # For table display

            node, path = fringe.popleft()

            if node not in explored:
                explored.add(node)
                traversal_order.append(node)

                self._print_table_row(
                    iteration, current_fringe_snapshot, current_explored_snapshot, node
                )

                if node == goal_node:
                    found_goal = True
                    print(
                        f"\nGoal node '{goal_node}' reached! "
                        f"Path: {' -> '.join(path)}"
                    )
                    break

                # Neighbors in L-R order (as stored)
                for neigh, _ in self.graph[node]:
                    if neigh not in explored and all(neigh != p for p, _ in fringe):
                        new_path = list(path)
                        new_path.append(neigh)
                        fringe.append((neigh, new_path))
            else:
                self._print_table_row(
                    iteration,
                    current_fringe_snapshot,
                    current_explored_snapshot,
                    f"{node} (already explored)",
                )

        print("\n" + "=" * 80)
        print(f"BFS (L-R) Traversal Order: {' '.join(traversal_order)}")
        if goal_node and not found_goal:
            print(f"Goal node '{goal_node}' not found in traversal.")
        print("--------------------------------------------------")

    def bfs_rl(self, start, goal_node=None):
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return

        explored = set()
        fringe = deque([(start, [start])])
        found_goal = False
        iteration = 0

        print(f"\n--- BFS (Right-to-Left) from {start} ---")
        self._print_table_header()

        traversal_order = []

        while fringe:
            iteration += 1
            current_fringe_snapshot = list(fringe)
            current_explored_snapshot = set(explored)

            node, path = fringe.popleft()

            if node not in explored:
                explored.add(node)
                traversal_order.append(node)

                self._print_table_row(
                    iteration, current_fringe_snapshot, current_explored_snapshot, node
                )

                if node == goal_node:
                    found_goal = True
                    print(
                        f"\nGoal node '{goal_node}' reached! "
                        f"Path: {' -> '.join(path)}"
                    )
                    break

                # Neighbors in reverse order (R-L)
                for neigh, _ in reversed(self.graph[node]):
                    if neigh not in explored and all(neigh != p for p, _ in fringe):
                        new_path = list(path)
                        new_path.append(neigh)
                        fringe.append((neigh, new_path))
            else:
                self._print_table_row(
                    iteration,
                    current_fringe_snapshot,
                    current_explored_snapshot,
                    f"{node} (already explored)",
                )

        print("\n" + "=" * 80)
        print(f"BFS (R-L) Traversal Order: {' '.join(traversal_order)}")
        if goal_node and not found_goal:
            print(f"Goal node '{goal_node}' not found in traversal.")
        print("--------------------------------------------------")

    # ---------------- DFS ---------------- #

    def dfs_lr(self, start, goal_node=None):
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return

        explored = set()
        fringe = [(start, [start])]  # Stack: (node, path)
        found_goal = False
        iteration = 0

        print(f"\n--- DFS (Left-to-Right) from {start} ---")
        self._print_table_header()

        traversal_order = []

        while fringe:
            iteration += 1
            current_fringe_snapshot = list(fringe)
            current_explored_snapshot = set(explored)

            node, path = fringe.pop()  # LIFO

            if node not in explored:
                explored.add(node)
                traversal_order.append(node)

                self._print_table_row(
                    iteration, current_fringe_snapshot, current_explored_snapshot, node
                )

                if node == goal_node:
                    found_goal = True
                    print(
                        f"\nGoal node '{goal_node}' reached! "
                        f"Path: {' -> '.join(path)}"
                    )
                    break

                # For L-R processing, push neighbors in reverse order
                for neigh, _ in reversed(self.graph[node]):
                    if neigh not in explored and all(neigh != p for p, _ in fringe):
                        new_path = list(path)
                        new_path.append(neigh)
                        fringe.append((neigh, new_path))
            else:
                self._print_table_row(
                    iteration,
                    current_fringe_snapshot,
                    current_explored_snapshot,
                    f"{node} (already explored)",
                )

        print("\n" + "=" * 80)
        print(f"DFS (L-R) Traversal Order: {' '.join(traversal_order)}")
        if goal_node and not found_goal:
            print(f"Goal node '{goal_node}' not found in traversal.")
        print("--------------------------------------------------")

    def dfs_rl(self, start, goal_node=None):
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return

        explored = set()
        fringe = [(start, [start])]  # Stack: (node, path)
        found_goal = False
        iteration = 0

        print(f"\n--- DFS (Right-to-Left) from {start} ---")
        self._print_table_header()

        traversal_order = []

        while fringe:
            iteration += 1
            current_fringe_snapshot = list(fringe)
            current_explored_snapshot = set(explored)

            node, path = fringe.pop()  # LIFO

            if node not in explored:
                explored.add(node)
                traversal_order.append(node)

                self._print_table_row(
                    iteration, current_fringe_snapshot, current_explored_snapshot, node
                )

                if node == goal_node:
                    found_goal = True
                    print(
                        f"\nGoal node '{goal_node}' reached! "
                        f"Path: {' -> '.join(path)}"
                    )
                    break

                # For R-L processing, push neighbors in original order
                for neigh, _ in self.graph[node]:
                    if neigh not in explored and all(neigh != p for p, _ in fringe):
                        new_path = list(path)
                        new_path.append(neigh)
                        fringe.append((neigh, new_path))
            else:
                self._print_table_row(
                    iteration,
                    current_fringe_snapshot,
                    current_explored_snapshot,
                    f"{node} (already explored)",
                )

        print("\n" + "=" * 80)
        print(f"DFS (R-L) Traversal Order: {' '.join(traversal_order)}")
        if goal_node and not found_goal:
            print(f"Goal node '{goal_node}' not found in traversal.")
        print("--------------------------------------------------")

    # ---------------- UCS ---------------- #

    def ucs(self, start, goal):
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return None, float("inf")
        if goal not in self.graph:
            print(f"Goal node '{goal}' not found in the graph.")
            return None, float("inf")

        frontier = []
        heapq.heappush(frontier, (0, start, [start]))  # (cost, node, path)
        explored = set()
        iteration = 0

        print(f"\n--- Uniform Cost Search (UCS) from {start} to {goal} ---")
        print("Iteration | Frontier (Node: Cost)                | Explored")
        print("-" * 70)

        while frontier:
            iteration += 1
            cost, node, path = heapq.heappop(frontier)

            if node in explored:
                continue

            explored.add(node)

            # Current frontier contents (node, cost)
            frontier_nodes = [(n, c) for c, n, _ in frontier]
            print(f"{iteration:<9} | {str(frontier_nodes):<36} | {list(explored)}")

            if node == goal:
                print(f"\nGoal node '{goal}' reached!")
                print(f"Path: {' -> '.join(path)}")
                print(f"Total cost: {cost}")
                return path, cost

            for child, weight in self.graph.get(node, []):
                new_cost = cost + weight
                new_path = path + [child]
                if child not in explored:
                    heapq.heappush(frontier, (new_cost, child, new_path))

        print(f"\nNo path found from '{start}' to '{goal}'.")
        return None, float("inf")


# ---------------- Input & Menu ---------------- #

def get_graph_input_initial(graph_obj):
    num_nodes = int(input("Enter the number of nodes: "))
    for i in range(num_nodes):
        node_name = input(f"Enter name for Node {i + 1}: ")
        graph_obj.add_node(node_name)

    num_edges = int(input("Enter the number of edges: "))
    for i in range(num_edges):
        u = input(f"Enter 'from' node for Edge {i + 1}: ")
        v = input(f"Enter 'to' node for Edge {i + 1}: ")
        cost_str = input(f"Enter cost for Edge {i + 1} (press Enter for 0): ")
        cost = int(cost_str) if cost_str else 0
        graph_obj.add_edge(u, v, cost)

    print("\nInitial graph setup complete!")


def run_menu(graph_obj):
    while True:
        print("\nMENU")
        print("1  Add Node")
        print("2  Add Edge")
        print("3  Delete Node")
        print("4  Delete Edge")
        print("5  Display Graph")
        print("6  Display Adjacency List")
        print("7  BFS Left to Right")
        print("8  BFS Right to Left")
        print("9  DFS Left to Right")
        print("10 DFS Right to Left")
        print("11 Uniform Cost Search (UCS)")
        print("12 Exit")

        ch = input("Enter choice: ")

        if not ch.isdigit():
            print("Invalid input. Please enter a number between 1 and 12.")
            continue
        ch = int(ch)

        if ch == 1:
            graph_obj.add_node(input("Node: "))
        elif ch == 2:
            u = input("From: ")
            v = input("To: ")
            cost_str = input("Cost (press Enter for 0): ")
            cost = int(cost_str) if cost_str else 0
            graph_obj.add_edge(u, v, cost)
        elif ch == 3:
            node_to_delete = input("Node: ")
            graph_obj.delete_node(node_to_delete)
        elif ch == 4:
            u = input("From: ")
            v = input("To: ")
            graph_obj.delete_edge(u, v)
        elif ch == 5:
            graph_obj.display()
        elif ch == 6:
            graph_obj.display_adj_list(input("Node: "))
        elif ch in [7, 8, 9, 10]:
            start_node = input("Enter start node: ")
            goal_input = input("Enter goal node (optional, press Enter to skip): ")
            goal_node = goal_input if goal_input else None

            if ch == 7:
                graph_obj.bfs_lr(start_node, goal_node)
            elif ch == 8:
                graph_obj.bfs_rl(start_node, goal_node)
            elif ch == 9:
                graph_obj.dfs_lr(start_node, goal_node)
            elif ch == 10:
                graph_obj.dfs_rl(start_node, goal_node)
        elif ch == 11:
            start_node = input("Enter start node: ")
            goal_node = input("Enter goal node: ")
            graph_obj.ucs(start_node, goal_node)
        elif ch == 12:
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 12.")


# ---------------- Main ---------------- #

if __name__ == "__main__":
    g = Graph()
    get_graph_input_initial(g)
    run_menu(g)
