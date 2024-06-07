import argparse

import matplotlib.pyplot as plt
import heapq
from k_means_constrained import KMeansConstrained
import numpy as np

# Define classes to represent pins and taps
# Initialize variables to store problem parameters
max_runtime = None
max_load = None
grid_size = None
capacity = None
pins = []
taps = []


#plot
def plot_assigned_pins_taps(grid_size, pins, taps):
    plt.figure(figsize=(8, 8))

    # Plot grid lines
    for i in range(grid_size + 1):
        plt.plot([0, grid_size], [i, i], 'k-', linewidth=0.5)  # Horizontal lines
        plt.plot([i, i], [0, grid_size], 'k-', linewidth=0.5)  # Vertical lines

    # Plot pins and assigned taps
    for pin in pins:
        plt.scatter(pin.x, pin.y, color='blue')
        for tap in taps:
            if pin in tap.pins:
                plt.plot([pin.x, tap.x], [pin.y, tap.y], 'r--')  # Draw connection from pin to tap

    # Plot taps
    tap_x = [tap.x for tap in taps]
    tap_y = [tap.y for tap in taps]
    plt.scatter(tap_x, tap_y, color='red', marker='s', s=100)

    plt.title('Grid with Assigned Pins and Taps')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()



class Pin:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

class Tap:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.pins = []
        self.edges = []
        self.load = 0

# Define a function to parse input file
def parse_input(input_file):

    with open(args.input) as f:
        line = f.readline()
        while len(line) > 0:
            data = line.strip().split(' ')
            if data[0] == 'MAX_RUNTIME':
                max_runtime = int(data[1])
            elif data[0] == 'MAX_LOAD':
                max_load = int(data[1])
            elif data[0] == 'GRID_SIZE':
                grid_size = int(data[1])
            elif data[0] == 'CAPACITY':
                capacity = int(data[1])
            elif data[0] == 'PINS':
                num_pins = int(data[1])
                for i in range(num_pins):
                    data = f.readline().strip().split(' ')
                    pins.append(Pin(i,int(data[2]), int(data[3])))
            elif data[0] == 'TAPS':
                num_taps = int(data[1])
                for i in range(num_taps):
                    data = f.readline().strip().split(' ')
                    taps.append(Tap(i,int(data[2]), int(data[3])))
            
            line = f.readline()

    return max_runtime, max_load, grid_size, capacity, pins, taps


# Define a function to assign pins to taps base on constraints
def calculate_manhattan_distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)

def assign_pins_to_taps(pins, taps, max_load):
    # Initialize the load of each tap and their pins list
    for tap in taps:
        tap.pins = []
        tap.load = 0  # Reset load of each tap

    # Assign each pin to the closest tap based on Manhattan distance
    for pin in pins:
        # List to hold potential taps sorted by distance, then by load
        possible_taps = []
        
        # Calculate distance for each tap and add to the list
        for tap in taps:
            distance = calculate_manhattan_distance(pin, tap)
            possible_taps.append((distance, tap.load, tap))
        
        # Sort taps first by distance, then by load
        possible_taps.sort(key=lambda x: (x[0], x[1]))

        # Try to assign the pin to the closest available tap
        for distance, load, tap in possible_taps:
            if tap.load < max_load:
                tap.pins.append(pin)
                tap.load += 1
                print(f"Assigned Pin {pin.index} to Tap {tap.index} (Distance: {distance}, Load after assignment: {tap.load})")
                break
        else:
            # If all nearby taps are full, handle error or consider expanding tap capacity
            print(f"Could not assign Pin {pin.index} as all nearby taps are full.")


def assign_pins_to_taps2(pins, taps, max_load):
    # Extract coordinates of pins
    pin_coordinates = np.array([[pin.x, pin.y] for pin in pins])

    # Initialize KMeansConstrained with constraints
    clf = KMeansConstrained(
        n_clusters=len(taps),  # Number of taps
        size_min=0,     # Minimum size for each cluster
        size_max=max_load,     # Maximum size for each cluster
        random_state=0,
        n_jobs = -1
    )
    
    # Fit KMeans and obtain centroids
    clf.fit_predict(pin_coordinates)

    # center of each cluster
    center = clf.cluster_centers_
    # Assign pins to taps based on KMeans clustering
    for pin_index, tap_index in enumerate(clf.labels_):
        tap = taps[tap_index]
        if tap.load < max_load:
            tap.pins.append(pins[pin_index])
            tap.load += 1
            print(f"Assigned Pin {pins[pin_index].index} to Tap {tap.index} (Load after assignment: {tap.load})")
        else:
            print(f"Could not assign Pin {pins[pin_index].index} as Tap {tap.index} is full.")

    
    # Plot clusters
    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab20b(np.linspace(0, 1, len(taps)))
    for tap, color in zip(taps, colors):
        tap_pins = np.array([[pin.x, pin.y] for pin in tap.pins])
        plt.scatter(tap_pins[:, 0], tap_pins[:, 1], c=[color], alpha=0.6, edgecolors='w')
        plt.scatter(tap.x, tap.y, c=[color], s=100, alpha=0.9, marker='X')  # mark tap
        #for pin in tap.pins:
            #plt.plot([pin.x, tap.x], [pin.y, tap.y], c=color, alpha=0.5)  # draw line from pin to tap

    plt.title('Assignment of Pins to Taps with Connections')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()

    return center
   



def prim_mst(pins, tap):
    import heapq

    # Map pins and tap to indices
    pin_index = {pin: i for i, pin in enumerate(pins, 1)}  # Starting from 1 for pins
    pin_index[tap] = 0  # Tap gets index 0

    # Initial edge setup with indices to avoid direct object comparison
    edges = []
    for i, pin1 in enumerate(pins):
        for j, pin2 in enumerate(pins[i + 1:], i + 1):
            dist = calculate_manhattan_distance(pin1, pin2)
            edges.append((dist, pin_index[pin1], pin_index[pin2]))
    for pin in pins:
        dist = calculate_manhattan_distance(pin, tap)
        edges.append((dist, pin_index[tap], pin_index[pin]))

    # Sorting edges by distance
    edges.sort(key=lambda x: x[0])

    # Prim's algorithm implementation
    mst = []
    connected = set([pin_index[tap]])  # Start from tap
    priority_queue = [edge for edge in edges if pin_index[tap] in edge[1:3]]

    heapq.heapify(priority_queue)
    parent = {pin_index[tap]: None}  # Parent map to reconstruct paths

    while priority_queue:
        cost, u_idx, v_idx = heapq.heappop(priority_queue)
        if v_idx not in connected:
            connected.add(v_idx)
            parent[v_idx] = u_idx
            mst.append((u_idx, v_idx, cost))
            for edge in edges:
                if (edge[1] == v_idx and edge[2] not in connected) or (edge[2] == v_idx and edge[1] not in connected):
                    heapq.heappush(priority_queue, edge)

    # Convert indices back to coordinates
    mst_with_coords = []
    for u_idx, v_idx, cost in mst:
        u = pins[u_idx-1] if u_idx != 0 else tap
        v = pins[v_idx-1] if v_idx != 0 else tap
        mst_with_coords.append(((u.x, u.y), (v.x, v.y)))

    return mst_with_coords, parent



def perform_routing(taps):
    # Assume each tap has a list of pins assigned to it
    for tap in taps:
        # Get the pins assigned to this tap
        assigned_pins = tap.pins
        if assigned_pins:
            # Compute the MST
            mst_with_coords, _ = prim_mst(assigned_pins, tap)
            
            # Initialize the edges list for each tap
            tap.edges = []

            # Generate rectilinear routing (edges) from the MST
            for (u, v) in mst_with_coords:
                # Check if a direct horizontal or vertical connection is possible
                if u[0] == v[0] or u[1] == v[1]:
                    # Direct connection
                    tap.edges.append((u, v))
                else:
                    # Rectilinear connection with an intermediate point
                    intermediate_point = (u[0], v[1])
                    tap.edges.append((u, intermediate_point))
                    tap.edges.append((intermediate_point, v))
            
            print(f"Tap {tap.index}: {len(mst_with_coords)} edges in MST connected with rectilinear paths")
            for edge in tap.edges:
                (x1, y1), (x2, y2) = edge
                if (x1 == x2 or y1 == y2):  # Checking if the segment is straight
                    print(f"  Direct segment from ({x1}, {y1}) to ({x2}, {y2})")
                else:  # This case won't actually happen due to rectilinear path logic above
                    print(f"  Segment from ({x1}, {y1}) via intermediate to ({x2}, {y2})")

## RSA
class Node:
    def __init__(self, x, y, pin=None):
        self.x = x
        self.y = y
        self.parent = None  # Parent node
        self.children = []  # Children nodes
        self.pin = pin  # Associate this node with a pin if any

    def set_parent(self, parent_node):
        self.parent = parent_node
        parent_node.children.append(self)


class Tree:
    def __init__(self, node):
        self.root = node

    def __lt__(self, other):
        # For max-heap based on sum of coordinates
        return (self.root.x + self.root.y) > (other.root.x + other.root.y)

def perform_rsa_routing_optimized(pins, tap):
    nodes = [Node(pin.x, pin.y, pin) for pin in pins] + [Node(tap.x, tap.y)]
    trees = [Tree(node) for node in nodes]
    heapq.heapify(trees)  # Organize trees in a heap based on the sum of their coordinates

    while len(trees) > 1:
        tree1 = heapq.heappop(trees)  # Automatically gets the tree with the highest x+y
        tree2 = heapq.heappop(trees)  # Gets the second highest x+y
        new_tree = merge_trees(tree1.root, tree2.root)  # Merges trees
        heapq.heappush(trees, Tree(new_tree))  # Pushes new tree back into heap

    rsa_tree = trees[0].root
    return rsa_tree

def merge_trees(tree1, tree2):
    # Calculate centroid of the roots of the two trees
    new_root_x = (tree1.x + tree2.x) / 2
    new_root_y = (tree1.y + tree2.y) / 2

    # Round or adjust these coordinates as required by your grid or routing constraints
    new_root_x = round(new_root_x)
    new_root_y = round(new_root_y)

    new_root = Node(new_root_x, new_root_y)

    # Connect the new root to the original trees' roots using the nearest points
    intermediate_node1 = Node(tree1.x, new_root_y)
    intermediate_node1.set_parent(new_root)
    tree1.set_parent(intermediate_node1)

    intermediate_node2 = Node(tree2.x, new_root_y)
    intermediate_node2.set_parent(new_root)
    tree2.set_parent(intermediate_node2)

    return new_root


def find_highest_rightmost_trees(trees):
    # Find the two trees to merge based on the RSA algorithm
    max_sum = float('-inf')
    trees_to_merge = None, None

    for i, ti in enumerate(trees):
        for j, tj in enumerate(trees):
            if i != j:
                # Calculate sum of root coordinates
                sum_coords = ti.x + ti.y + tj.x + tj.y
                if sum_coords > max_sum:
                    max_sum = sum_coords
                    trees_to_merge = ti, tj
    return trees_to_merge

def extract_edges_from_tree(node):
    # Extract the edges from the RSA tree for plotting or further processing
    edges = []
    # Use a stack for the iterative traversal of the tree
    stack = [node]

    while stack:
        current_node = stack.pop()
        # Since we are creating rectilinear paths, check if we need an intermediate point
        if current_node.parent:
            parent = current_node.parent
            if current_node.x != parent.x and current_node.y != parent.y:
                # Insert an intermediate point for rectilinear path
                intermediate_point = (current_node.x, parent.y)
                edges.append(((current_node.x, current_node.y), intermediate_point))
                edges.append((intermediate_point, (parent.x, parent.y)))
            else:
                # Directly connect if it is a straight line
                edges.append(((current_node.x, current_node.y), (parent.x, parent.y)))
        stack.extend(current_node.children)

    return edges


def perform_routing2(taps):
    for tap in taps:
        # Call the RSA routing for this tap's pins
        rsa_tree = perform_rsa_routing_optimized(tap.pins, tap)

        # Extract rectilinear edges from the RSA tree for this tap
        tap.edges = extract_edges_from_tree(rsa_tree)

        # Debugging: Print out the connections
        print(f"Tap {tap.index} connected with RSA routing.")
        for edge in tap.edges:
            print(f"  Edge from {edge[0]} to {edge[1]}")


# hierarchical

import heapq

class Node:
    def __init__(self, x, y, pin=None):
        self.x = x
        self.y = y
        self.parent = None  # Parent node
        self.children = []  # Children nodes
        self.pin = pin  # Associate this node with a pin if any

    def set_parent(self, parent_node):
        self.parent = parent_node
        parent_node.children.append(self)

class Tree:
    def __init__(self, node):
        self.root = node

    def __lt__(self, other):
        # For max-heap based on sum of coordinates
        return (self.root.x + self.root.y) > (other.root.x + other.root.y)

def manhattan_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def find_nearest_nodes(nodes):
    min_dist = float('inf')
    nearest_pair = None, None
    for i, node1 in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            node2 = nodes[j]
            dist = manhattan_distance(node1, node2)
            if dist < min_dist:
                min_dist = dist
                nearest_pair = node1, node2
    return nearest_pair

def merge_trees(node1, node2):
    new_root_x = (node1.x + node2.x) // 2
    new_root_y = (node1.y + node2.y) // 2

    new_root = Node(new_root_x, new_root_y)

    intermediate_node1 = Node(node1.x, new_root_y)
    intermediate_node1.set_parent(new_root)
    node1.set_parent(intermediate_node1)

    intermediate_node2 = Node(node2.x, new_root_y)
    intermediate_node2.set_parent(new_root)
    node2.set_parent(intermediate_node2)

    return new_root

def perform_hierarchical_routing_optimized(pins, tap):
    nodes = [Node(pin.x, pin.y, pin) for pin in pins] + [Node(tap.x, tap.y)]
    trees = [Tree(node) for node in nodes]

    # Initialize a priority queue with initial distances between all trees
    pq = []
    for i in range(len(trees)):
        for j in range(i + 1, len(trees)):
            dist = manhattan_distance(trees[i].root, trees[j].root)
            heapq.heappush(pq, (dist, trees[i], trees[j]))

    while len(trees) > 1:
        # Get the smallest distance pair, check if both trees are still in the trees list
        while pq:
            dist, tree1, tree2 = heapq.heappop(pq)
            if tree1 in trees and tree2 in trees:
                break
        else:
            # If the loop exhausts the priority queue without finding valid trees, we're done
            break

        # Merge the trees and create a new Tree instance for the new root
        new_root = merge_trees(tree1.root, tree2.root)
        new_tree = Tree(new_root)
        
        # Update the trees list: Remove old trees and add the new tree
        trees.remove(tree1)
        trees.remove(tree2)
        trees.append(new_tree)

        # Rebuild the priority queue with the new tree distances to remaining trees
        new_pq = []
        for tree in trees:
            if tree is not new_tree:  # Don't compare the tree with itself
                dist = manhattan_distance(new_tree.root, tree.root)
                heapq.heappush(new_pq, (dist, tree, new_tree))
        pq = new_pq

    rsa_tree = trees[0].root
    return rsa_tree


def extract_edges_from_tree(node):
    edges = []
    stack = [node]
    while stack:
        current_node = stack.pop()
        if current_node.parent:
            parent = current_node.parent
            if current_node.x != parent.x and current_node.y != parent.y:
                intermediate_point = (current_node.x, parent.y)
                edges.append(((current_node.x, current_node.y), intermediate_point))
                edges.append((intermediate_point, (parent.x, parent.y)))
            else:
                edges.append(((current_node.x, current_node.y), (parent.x, parent.y)))
        stack.extend(current_node.children)
    return edges


def perform_routing3(taps):
    for tap in taps:
        rsa_tree = perform_hierarchical_routing_optimized(tap.pins, tap)
        tap.edges = extract_edges_from_tree(rsa_tree)
        print(f"Tap {tap.index} connected with hierarchical routing.")
        for edge in tap.edges:
            print(f"  Edge from {edge[0]} to {edge[1]}")

            

# Define a function to write output file
def write_output_file(taps, filename):
    with open(filename, 'w') as file:
        for tap in taps:
            file.write(f"TAP {tap.index}\n")
            file.write(f"PINS {len(tap.pins)}\n")
            for pin in tap.pins:
                file.write(f"PIN {pin.index}\n")
            
            file.write(f"ROUTING {len(tap.edges)}\n")
            for segment in tap.edges:
                (x1, y1), (x2, y2) = segment
                file.write(f"EDGE {x1} {y1} {x2} {y2} \n")
            



def plot_connections(taps):
    plt.figure(figsize=(10, 10))
    for tap in taps:
        plt.scatter(tap.x, tap.y, color='red', marker='s', label='Tap' if 'Tap' not in plt.gca().get_legend_handles_labels()[1] else "")
        for pin in tap.pins:
            plt.scatter(pin.x, pin.y, color='blue', label='Pin' if 'Pin' not in plt.gca().get_legend_handles_labels()[1] else "")

        # Draw the RMST connections
        for (x1, y1), (x2, y2) in tap.edges:  # Correct unpacking of edge tuples
            # Plot vertical line
            plt.plot([x1, x1], [y1, y2], 'green')  # From (x1, y1) to (x1, y2)
            # Plot horizontal line
            plt.plot([x1, x2], [y2, y2], 'green')  # From (x1, y2) to (x2, y2)

    plt.title('Grid with RMST Connections')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clock Tree Synthesis")
    parser.add_argument("--input", type=str, help="Input file path")
    parser.add_argument("--output", type=str, help="Output file path")
    args = parser.parse_args()

    # Parse input file
    input_file = args.input
    max_runtime, max_load, grid_size, capacity, pins, taps = parse_input(input_file)
    
    #plot
    #plot_grid_pins_taps(grid_size, pins, taps)

    # Assign pins to taps
    #assign_pins_to_taps(pins, taps, max_load)

    center = assign_pins_to_taps2(pins, taps, max_load)
    #plot_assigned_pins_taps(grid_size, pins, taps)


    #MST
    #perform_routing(taps)

    #RSA
    #perform_routing2(taps)
    
    #hierarchical
    #perform_routing3(taps)
    #plot_connections(taps)

    # Write output file
    output_file = args.output
    write_output_file(taps, output_file)



#py cts.py --input test2.in --output test2.out
    
