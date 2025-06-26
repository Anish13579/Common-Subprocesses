from collections import defaultdict
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import time

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
print("FULL SEQUENCE ORDER ANALYSIS")
print("="*70)

# Function to find similar sequences based on patterns
def find_sequence_patterns(sequences):
    patterns = defaultdict(list)
    
    # Pattern 1: Exact sequence match
    for process, seq in sequences.items():
        patterns[tuple(seq)].append(process)
    
    return patterns

# Function to find common subsequences
def find_common_subsequences(sequences, min_length=3):
    subsequence_groups = defaultdict(list)
    
    for process, seq in sequences.items():
        # Generate subsequences of different lengths
        for length in range(min_length, len(seq) + 1):
            for i in range(len(seq) - length + 1):
                subseq = tuple(seq[i:i + length])
                subsequence_groups[subseq].append(process)
    
    # Filter to only include subsequences that appear in multiple processes
    common_subsequences = {k: v for k, v in subsequence_groups.items() if len(v) > 1}
    return common_subsequences

# Function to find similar starting patterns
def find_starting_patterns(sequences, pattern_length=3):
    starting_patterns = defaultdict(list)
    
    for process, seq in sequences.items():
        if len(seq) >= pattern_length:
            pattern = tuple(seq[:pattern_length])
            starting_patterns[pattern].append(process)
    
    return starting_patterns

# Function to find similar ending patterns
def find_ending_patterns(sequences, pattern_length=3):
    ending_patterns = defaultdict(list)
    
    for process, seq in sequences.items():
        if len(seq) >= pattern_length:
            pattern = tuple(seq[-pattern_length:])
            ending_patterns[pattern].append(process)
    
    return ending_patterns

print("1. EXACT SEQUENCE MATCHING")
print("-" * 30)
exact_patterns = find_sequence_patterns(bpmn_data)
for pattern, processes in exact_patterns.items():
    if len(processes) > 1:  # Only show groups with multiple processes
        print(f"Identical sequence {pattern}:")
        for process in processes:
            print(f"  - {process}")
        print()

if not any(len(processes) > 1 for processes in exact_patterns.values()):
    print("No exact sequence matches found - all processes have unique sequences")
    print()

print("2. COMMON SUBSEQUENCES (Length 3+)")
print("-" * 40)
common_subseq = find_common_subsequences(bpmn_data, min_length=3)
# Sort by frequency (most common first)
sorted_subseq = sorted(common_subseq.items(), key=lambda x: len(x[1]), reverse=True)

for subseq, processes in sorted_subseq[:10]:  # Show top 10 most common
    print(f"Subsequence {subseq} appears in {len(processes)} processes:")
    for process in processes:
        print(f"  - {process}")
    print()

print("3. SIMILAR STARTING PATTERNS (First 3)")
print("-" * 40)
starting_patterns = find_starting_patterns(bpmn_data, 3)
for pattern, processes in starting_patterns.items():
    if len(processes) > 1:
        print(f"Starting pattern {pattern}:")
        for process in processes:
            print(f"  - {process}")
        print()

print("4. SIMILAR ENDING PATTERNS (Last 3)")
print("-" * 40)
ending_patterns = find_ending_patterns(bpmn_data, 3)
for pattern, processes in ending_patterns.items():
    if len(processes) > 1:
        print(f"Ending pattern {pattern}:")
        for process in processes:
            print(f"  - {process}")
        print()

print("="*70)
print("DECISION TREE ON FULL SEQUENCES")
print("="*70)

# Prepare features using full formKey sequences (padded to same length)
max_len = max(len(formkeys) for formkeys in bpmn_data.values())

X_train = []
process_names = []
for process, formkeys in bpmn_data.items():
    process_names.append(process)
    # Pad sequences with 0 to make them uniform length
    padded = formkeys + [0] * (max_len - len(formkeys))
    X_train.append(padded)

X_train = np.array(X_train)

# Assign groups based on unique full sequences
unique_keys = {}
label_counter = 1
y_train = []

for formkeys in map(tuple, X_train):
    if formkeys not in unique_keys:
        unique_keys[formkeys] = label_counter
        label_counter += 1
    y_train.append(unique_keys[formkeys])

y_train = np.array(y_train)

# Train Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Measure prediction time
start_time = time.time()
predicted_labels = clf.predict(X_train)
prediction_time = time.time() - start_time

# Group results
grouped_processes_dt = defaultdict(list)
for label, process in zip(predicted_labels, process_names):
    grouped_processes_dt[label].append(process)

print("DECISION TREE RESULTS:")
print("-" * 25)
for group_id, processes in grouped_processes_dt.items():
    original_seq = [k for k, v in unique_keys.items() if v == group_id][0]
    # Remove padding zeros for display
    display_seq = [x for x in original_seq if x != 0]
    print(f"Group {group_id}: Sequence {display_seq}")
    for process in processes:
        print(f"  - {process}")
    print()

print(f"⏱️ Prediction time: {prediction_time:.6f} seconds")
print(f"📊 Total groups created: {len(grouped_processes_dt)}")

print("="*70)
print("SEQUENCE SIMILARITY ANALYSIS")
print("="*70)

# Advanced similarity analysis
def calculate_sequence_similarity(seq1, seq2):
    """Calculate similarity between two sequences using common elements"""
    set1, set2 = set(seq1), set(seq2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

# Find most similar process pairs
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

print(f"SIMILAR PROCESS PAIRS (similarity >= {similarity_threshold}):")
print("-" * 50)
if similar_pairs:
    similar_pairs.sort(key=lambda x: x[2], reverse=True)
    for proc1, proc2, similarity in similar_pairs:
        print(f"{proc1} ↔ {proc2}")
        print(f"  Similarity: {similarity:.2f}")
        print(f"  Seq1: {bpmn_data[proc1]}")
        print(f"  Seq2: {bpmn_data[proc2]}")
        print()
else:
    print("No process pairs found with similarity >= 0.6")

print("="*70)
print("SUMMARY")
print("="*70)
print(f"✓ All processes have unique exact sequences")
print(f"✓ Found {len([x for x in common_subseq.values() if len(x) > 1])} common subsequences")
print(f"✓ Found {len([x for x in starting_patterns.values() if len(x) > 1])} shared starting patterns")
print(f"✓ Found {len([x for x in ending_patterns.values() if len(x) > 1])} shared ending patterns")
print(f"✓ Found {len(similar_pairs)} process pairs with high similarity")
