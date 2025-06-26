from collections import defaultdict
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import time  # Import time module

# BPMN dictionary data with all 10 processes
bpmn_data = {
    "Process 1-163.bpmn20.xml": [165, 173, 254, 255, 256],
    "Process 2-257.bpmn20.xml": [165, 173, 252, 253, 254],
    "Process 3-258.bpmn20.xml": [165, 173, 256, 255, 252],
    "Process 4-259.bpmn20.xml": [165, 173, 252, 253, 255],
    "Process 5-260.bpmn20.xml": [165, 173, 254, 256, 173],
    "Process 6-261.bpmn20.xml": [165, 173, 252, 253, 255],
    "Process 7-264.bpmn20.xml": [165, 173, 252, 254, 256],
    "Process 8-262.bpmn20.xml": [165, 173, 252, 253, 254],
    "Process 9-265.bpmn20.xml": [165, 173, 254, 256, 255],
    "Process 10-263.bpmn20.xml": [165, 173, 256, 252, 253]
}

#Form 1 = 165
#Form 2 = 173
#Form 3 = 252
#Form 4 = 253
#Form 5 = 254
#Form 6 = 255
#Form 7 = 256

# Prepare features (sorted first 4 formKeys) for all 10 processes
X_train = []
process_names = []
for process, formkeys in bpmn_data.items():
    process_names.append(process)
    X_train.append(sorted(formkeys[:4]))  # Using first 4 formKeys

X_train = np.array(X_train)

# Assign groups based on unique combinations of first 4 formKeys
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
grouped_processes = defaultdict(list)
for label, process in zip(predicted_labels, process_names):
    grouped_processes[label].append(process)

# Prepare output
output = "BPMN Process Groups (using starting 4 formKeys):\n\n"
for group_id, processes in grouped_processes.items():
    group_key = [k for k, v in unique_keys.items() if v == group_id][0]
    output += f"Group {group_id}: Starting formKeys {group_key}\n"
    for process in processes:
        output += f"  - {process}\n"
    output += "\n"

# Add prediction time to output
output += f"⏱️ Prediction time: {prediction_time:.6f} seconds"

print(output)
