import numpy as np
import random
import csv
from collections import Counter, defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

# Load CSV file
bpmn_data = {}
csv_file_path = "Generated_1000_Processes.csv"  # Hardcoded for direct run
try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        for idx, row in enumerate(reader):
            if row:
                process_name = row[0]
                form_keys = list(map(int, row[1:]))
                bpmn_data[process_name] = form_keys
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# Convert sequences to features and labels
X = []
y = []
unique_keys = {}
label_counter = 0

for process_name, sequence in bpmn_data.items():
    key = tuple(sequence)
    if key not in unique_keys:
        unique_keys[key] = label_counter
        label_counter += 1
    X.append(sequence)
    y.append(unique_keys[key])

X = np.array(X)
y = np.array(y)

"""
import random
noise_ratio = 0.1  # 12% of samples will be noised
noise_level = 1     # Change 1 form key per sequence
noise_magnitude = [1, 2, 3]

num_samples = len(X)
num_noisy = int(noise_ratio * num_samples)
noisy_indices = random.sample(range(num_samples), num_noisy)

for i in noisy_indices:
    change_index = random.randint(0, len(X[i]) - 1)
    change = random.choice(noise_magnitude)
    X[i][change_index] += change

"""

# Remove classes with only one sample
label_counts = Counter(y)
valid_indices = [i for i, label in enumerate(y) if label_counts[label] > 1]
X = X[valid_indices]
y = y[valid_indices]

# Map filtered process names to their labels
# Re-map labels to sequential group numbers: 1, 2, 3, ...
label_remap = {}
current_label = 1
for old_label in sorted(set(y)):
    label_remap[old_label] = current_label
    current_label += 1

# Apply remapped labels
y = np.array([label_remap[label] for label in y])
#print(y)
# Map filtered process names to their new labels
filtered_process_names = [proc for proc, seq in bpmn_data.items() if tuple(seq) in unique_keys and label_counts[unique_keys[tuple(seq)]] > 1]
filtered_labels = [label_remap[unique_keys[tuple(bpmn_data[proc])]] for proc in filtered_process_names]
filtered_process_to_label = dict(zip(filtered_process_names, filtered_labels))

# Split data
min_test_size = max(len(set(y)) / len(y), 0.3)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=min_test_size, stratify=y, random_state=42
)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
start_time = time.time()
predictions = clf.predict(X_test)
prediction_time = time.time() - start_time
accuracy = accuracy_score(y_test, predictions)


groups = defaultdict(list)
for process, label in filtered_process_to_label.items():
    groups[label].append(process)

print("=== Process Groups ===")
for group_id, processes in groups.items():
    print(f"Group {group_id} ({len(processes)} processes):")
    for p in processes:
        print(f"  - {p}")
    print()

    
# print("NOISED DATASET EXPERIMENT")
print(f"Prediction Accuracy: {accuracy * 100:.2f}%")
print(f"Prediction Time: {prediction_time:.4f} seconds")
print(f"Total Groups Created: {len(set(y))}")
print()