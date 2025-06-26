from collections import defaultdict, deque
import numpy as np

# BPMN dictionary data with all 10 processes
bpmn_data = {
    "Process 1-163.bpmn20.xml": [173, 252, 253, 165, 254],
    "Process 2-257.bpmn20.xml": [254, 252, 165, 173, 253],
    "Process 3-258.bpmn20.xml": [252, 173, 165, 254, 253],
    "Process 4-259.bpmn20.xml": [253, 165, 173, 252, 254],
    "Process 5-260.bpmn20.xml": [165, 252, 173, 254, 253],
    "Process 6-261.bpmn20.xml": [252, 255, 173, 165, 256],
    "Process 7-264.bpmn20.xml": [255, 173, 252, 256, 165],
    "Process 8-262.bpmn20.xml": [173, 165, 255, 256, 252],
    "Process 9-265.bpmn20.xml": [256, 165, 255, 173, 252],
    "Process 10-263.bpmn20.xml": [165, 252, 255, 256, 173]
}

print("="*70)
print("SEQUENCE SIMILARITY ANALYSIS (Ignoring Order)")
print("="*70)

def calculate_sequence_similarity(seq1, seq2):
    """Calculate Jaccard similarity between two sequences (order ignored)"""
    set1, set2 = set(seq1), set(seq2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

# Find similar process pairs with similarity >= 0.6
similarity_threshold = 0.6
similar_pairs = []

processes = list(bpmn_data.keys())
for i in range(len(processes)):
    for j in range(i+1, len(processes)):
        proc1, proc2 = processes[i], processes[j]
        seq1, seq2 = bpmn_data[proc1], bpmn_data[proc2]
        similarity = calculate_sequence_similarity(seq1, seq2)
        if similarity >= similarity_threshold:
            similar_pairs.append((proc1, proc2, similarity))

# Build similarity graph
graph = defaultdict(set)
for proc1, proc2, _ in similar_pairs:
    graph[proc1].add(proc2)
    graph[proc2].add(proc1)

# Find connected components (groups)
visited = set()
groups = []

for process in processes:
    if process not in visited:
        queue = deque([process])
        group = set()
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                group.add(current)
                # Add all connected neighbors
                queue.extend(graph[current] - visited)
        groups.append(group)

# Prepare and print results
print(f"SIMILAR PROCESS PAIRS (similarity >= {similarity_threshold}):")
print("-" * 70)
if similar_pairs:
    # Sort by similarity descending
    similar_pairs.sort(key=lambda x: x[2], reverse=True)
    for proc1, proc2, similarity in similar_pairs:
        print(f"{proc1} ↔ {proc2}")
        print(f"  Similarity: {similarity:.2f}")
        print(f"  FormKeys 1: {bpmn_data[proc1]}")
        print(f"  FormKeys 2: {bpmn_data[proc2]}")
        print()
else:
    print("No process pairs found with similarity >= 0.6")

print("\n" + "="*70)
print("PROCESS GROUPS BASED ON SIMILARITY")
print("="*70)
for i, group in enumerate(groups, 1):
    print(f"Group {i}:")
    for process in sorted(group):
        print(f"  - {process}")
    print()

print("="*70)
print("SUMMARY")
print("="*70)
print(f"Total similar pairs found: {len(similar_pairs)}")
print(f"Total groups formed: {len(groups)}")
print(f"Group sizes: {[len(group) for group in groups]}")
