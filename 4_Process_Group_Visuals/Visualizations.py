from collections import defaultdict
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import time
import matplotlib.pyplot as plt

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
output += f"⏱️ Prediction time: {prediction_time:.6f} seconds\n"
print(output)

# ========== VISUALIZATIONS ==========
# Prepare data for visualizations
group_ids = sorted(grouped_processes.keys())
group_counts = [len(grouped_processes[gid]) for gid in group_ids]
group_labels = [f"Group {gid}" for gid in group_ids]
group_formkeys = [str([k for k,v in unique_keys.items() if v==gid][0]) for gid in group_ids]

# Simulated duration data (would come from real event logs)
durations = np.random.randint(10, 30, size=len(group_ids))  # Simulated avg durations

# 1. Pie Chart - Process Distribution
plt.figure(figsize=(10, 7))
plt.pie(group_counts, labels=group_labels, autopct='%1.1f%%', 
        startangle=90, colors=plt.cm.Pastel1(np.arange(len(group_ids))))
plt.title('BPMN Process Distribution by Groups\n(Based on Starting 4 FormKeys)', fontsize=14)
plt.tight_layout()
plt.savefig('process_distribution_pie.png')
plt.show()

# 2. Bar Chart - Process Counts
plt.figure(figsize=(10, 6))
bars = plt.bar(group_labels, group_counts, color=plt.cm.Set2(np.arange(len(group_ids))))
plt.xlabel('Workflow Groups', fontsize=12)
plt.ylabel('Number of Processes', fontsize=12)
plt.title('BPMN Process Counts by Group\n(Based on Starting 4 FormKeys)', fontsize=14)
plt.xticks(rotation=15)
plt.grid(axis='y', alpha=0.3)

# Add formKey labels to bars
for bar, formkey in zip(bars, group_formkeys):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'Keys: {formkey}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('process_counts_bar.png')
plt.show()

# 3. Line Chart - Task Transition Durations
plt.figure(figsize=(12, 6))
plt.plot(group_labels, durations, marker='o', linestyle='-', 
         color='#2c7bb6', linewidth=2.5, markersize=10)

plt.xlabel('Workflow Groups', fontsize=12)
plt.ylabel('Average Duration (minutes)', fontsize=12)
plt.title('Average Task Transition Durations\n(Based on FormKey Sequences)', fontsize=14)
plt.ylim(0, max(durations)*1.2)
plt.grid(alpha=0.4)

# Add duration values to points
for i, dur in enumerate(durations):
    plt.text(i, dur+1, f'{dur} min', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('task_durations_line.png')
plt.show()
