   def _get_all_heuristics(self, goal):
        """
        Get heuristic values h(n) for ALL nodes before starting A*.
        For the goal node, h(goal) is automatically set to 0.
        """
        h = {}
        print("\nEnter heuristic values h(n) (estimated cost to goal):")
        for node in sorted(self.graph.keys()):
            if node == goal:
                h[node] = 0.0
                print(f"h({node}) = 0  (goal node)")
                continue

            while True:
                val = input(f"h({node}): ")
                try:
                    h[node] = float(val)
                    break
                except ValueError:
                    print("Please enter a numeric value.")
        return h

    # ---------- A* Search ----------

    def astar(self, start, goal):
        """
        A* Search using user-provided heuristic values (collected before search).
        Output format matches the UCS example:
        --- A* Search (A*) from A to F ---
        Iteration | Frontier (Node: Cost)                | Explored
        ----------------------------------------------------------------------
        """
        if start not in self.graph:
            print(f"Start node '{start}' not found in the graph.")
            return None, float("inf")
        if goal not in self.graph:
            print(f"Goal node '{goal}' not found in the graph.")
            return None, float("inf")

        # Get heuristic values for all nodes before starting the search
        h = self._get_all_heuristics(goal)

        # priority queue items: (f_cost, g_cost, node, path)
        frontier = []
        g_start = 0.0
        f_start = g_start + h[start]
        heapq.heappush(frontier, (f_start, g_start, start, [start]))

        explored = set()
        iteration = 0

        print(f"\n--- A* Search (A*) from {start} to {goal} ---")
        print("Iteration | Frontier (Node: Cost)                | Explored")
        print("-" * 70)

        while frontier:
            iteration += 1
            f_cost, g_cost, node, path = heapq.heappop(frontier)

            if node in explored:
                continue

            explored.add(node)

            # Show frontier as list of (node, f_cost)
            frontier_nodes = [(n, f) for (f, g, n, _) in frontier]
            print(f"{iteration:<9} | {str(frontier_nodes):<36} | {list(explored)}")

            if node == goal:
                print(f"\nGoal node '{goal}' reached!")
                print(f"Path: {' -> '.join(path)}")
                print(f"Total cost: {g_cost}")
                return path, g_cost

            for neighbor, weight in self.graph.get(node, []):
                if neighbor in explored:
                    continue

                new_g = g_cost + weight
                new_f = new_g + h[neighbor]  # f = g + h
                new_path = path + [neighbor]
                heapq.heappush(frontier, (new_f, new_g, neighbor, new_path))

        print(f"\nNo path found from '{start}' to '{goal}'.")
        return None, float("inf")


# ---------- Initial graph input ----------

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


# ---------- Menu ----------

def run_menu(graph_obj):
    while True:
        print("\nMENU")
        print("1  Add Node")
        print("2  Add Edge")
        print("3  Delete Node")
        print("4  Delete Edge")
        print("5  Display Graph")
        print("6  Display Adjacency List")
        print("7  A* Search")
        print("8  Exit")

        ch = input("Enter choice: ")

        if not ch.isdigit():
            print("Invalid input. Please enter a number between 1 and 8.")
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
        elif ch == 7:
            start_node = input("Enter start node: ")
            goal_node = input("Enter goal node: ")
            graph_obj.astar(start_node, goal_node)
        elif ch == 8:
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


# ---------------- Main ---------------- #

if __name__ == "__main__":
    g = Graph()
    get_graph_input_initial(g)
    run_menu(g)
