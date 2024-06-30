import math
from concurrent.futures import ThreadPoolExecutor, as_completed

class TreeNode:
    def __init__(self, value, edge):
        self.value = value
        self.left = None
        self.right = None
        self.edge = edge

def process_parent_node(parent):
    parent.value = (parent.left.edge + parent.right.edge) // 2
    parent.edge = (parent.left.edge + parent.right.edge) % 2

    if parent.left and not parent.left.left and not parent.left.right:
        parent.left.edge = parent.left.value
    if parent.right and not parent.right.left and not parent.right.right:
        parent.right.edge = parent.right.value  

    if parent.left and parent.left.left and parent.left.right:
        left_value = parent.left.value if parent.left.value is not None else 0
        parent.left.edge = (parent.left.left.edge + parent.left.right.edge + left_value) % 2
        parent.left.value = (parent.left.left.edge + parent.left.right.edge + left_value) // 2
        parent.left.left.edge = parent.left.left.value
        parent.left.right.edge = parent.left.right.value

    if parent.right and parent.right.left and parent.right.right:
        right_value = parent.right.value if parent.right.value is not None else 0
        parent.right.edge = (parent.right.left.edge + parent.right.right.edge + right_value) % 2
        parent.right.value = (parent.right.left.edge + parent.right.right.edge + right_value) // 2
        parent.right.left.edge = parent.right.left.value
        parent.right.right.edge = parent.right.right.value
    
    return parent

def build_tree_from_bottom_to_top(leaf_values):
    if not leaf_values:
        return None, []

    leaf_nodes = [TreeNode(0, value) for value in leaf_values]
    print(f"Initial leaf nodes: {[node.value for node in leaf_nodes]}")
    print(f"Initial leaf nodes edges: {[node.edge for node in leaf_nodes]}")
    
    result = []
    steps = 0
    j = 1
    total_steps = 2 * int(math.log(len(leaf_nodes), 2))
    print(f"Total steps needed: {total_steps}")

    with ThreadPoolExecutor() as executor:  # Default max_workers=None, uses CPU count
        while steps < total_steps:
            print(f"\nStep {steps + 1}:")
            parents = []
            i = 1 - j
            futures = []
            while i < len(leaf_nodes):
                parent = TreeNode(None, None)  # Create a parent node
                parent.left = leaf_nodes[i]
                parent.right = leaf_nodes[i + 1]
                
                # Submitting each parent node processing as a separate task
                futures.append(executor.submit(process_parent_node, parent))
                i += 2
            
            # Wait for all tasks to complete
            for future in as_completed(futures):
                parent = future.result()
                parents.append(parent)
            
            steps += 1
            leaf_nodes = parents
            print(f"Parents after step {steps}: {[{'value': node.value, 'edge': node.edge} for node in leaf_nodes]}")

            if len(leaf_nodes) == 1:
                j = 0
                result.append(parent.edge)
                result.append((parent.left.edge + parent.right.edge + parent.value) % 2)
                parent.value = (parent.left.edge + parent.right.edge + parent.value) // 2
                result.append((parent.left.value + parent.right.value + parent.value) % 2)
                print(f"Final parent value and edges appended to result: {result}")
                steps = total_steps

    return leaf_nodes[0], result  # Return the root of the tree and the result array

def binary_array_to_number(binary_array):
    # Reverse the binary array
    binary_array = binary_array[::-1]
    # Convert the binary array to a string
    binary_string = ''.join(map(str, binary_array))
    # Convert the binary string to a decimal number
    return int(binary_string, 2)

def main():
    leaf_values = [0, 1, 0, 1, 0, 1, 1, 0]  # Initial unsorted array
    root, result = build_tree_from_bottom_to_top(leaf_values)
    number = binary_array_to_number(result)
    complement_number = len(leaf_values) - number
    
    print(f"Binary result: {result[::-1]}")  # Print the reversed binary result
    print(f"Decimal number: {number}")
    print(f"Complement number: {complement_number}")  

    # Generate sorted array based on complement number
    sorted_array = [0] * complement_number + [1] * (len(leaf_values) - complement_number)
    print(f"Sorted array based on complement number: {sorted_array}")

if __name__ == "__main__":
    main()
