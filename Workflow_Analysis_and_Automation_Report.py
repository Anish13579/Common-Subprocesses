# Updated Documentation with Analysis Results
documentation = """
# Workflow Analysis and Automation Report

## Problem Statement
Identify common process/subprocess workflows by analyzing event logs to automate workflows, improve operational efficiency, and reduce manual effort.

## Procedure

### Setup
- **Visual Studio Code**: Primary IDE for coding and configuration
- **MySQL Workbench**: Managed APS/Activiti databases
- **Apache Tomcat**: Hosted APS/Activiti applications
- **APS Configuration**: Established DB connectivity and API integration

### Data Collection
Collected event logs from 10 BPMN processes capturing:
- Task completion details
- FormKey sequences
- Process dependencies

### Workflow Sequence Analysis
Identified key patterns in starting sequences of user tasks:
- First 4 tasks determine workflow grouping
- Common starting patterns enable process standardization
- Discovered 3 distinct workflow groups based on initial formKeys

### Workflow Pattern Analysis
- Analyzed formKey sequences to identify recurring task patterns
- Discovered dependencies between tasks
- Identified optimization opportunities in repetitive tasks

### Model Selection
- **Decision Trees**: Classified workflows based on starting formKey patterns
- **Process Mining**: Reconstructed actual workflow paths
- **Markov Models**: Analyzed probabilistic transitions (future implementation)

### Solution
Built automated classification system using:
- FormKey sequence analysis
- Decision Tree classifier
- Process grouping algorithm

## Key Results

### Workflow Groups
Identified 3 distinct workflow groups based on first 4 formKey patterns:

| Group | Starting FormKeys | Processes | Count |
|-------|-------------------|-----------|-------|
| 1     | (165, 173, 254, 301) | Process 1-163, Process 5-260, Process 9-265 | 3 |
| 2     | (165, 173, 252, 300) | Process 2-257, Process 4-259, Process 6-261, Process 7-264, Process 8-262 | 5 |
| 3     | (165, 173, 256, 303) | Process 3-258, Process 10-263 | 2 |

### Automation Opportunities
- **Group 2 (5 processes)**: Highest automation potential
- **Common starting sequence**: 165 → 173 → 252 → 300
- Standardized subprocesses possible for first 4 tasks
"""

print(documentation)

# Visualization Code
import matplotlib.pyplot as plt
import numpy as np
import os

# Data for visualizations
bpmn_dir = r"C:\Users\ansarkar\Desktop\Presentation\bpmn_files"
groups = ['Group 1', 'Group 2', 'Group 3']
process_counts = [3, 5, 2]
formkey_patterns = ['(165,173,254,301)', '(165,173,252,300)', '(165,173,256,303)']
colors = ['#ff9999','#66b3ff','#99ff99']

# 1. Process Distribution Pie Chart
plt.figure(figsize=(9, 6))
plt.pie(process_counts, labels=groups, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Process Distribution Across Groups')
plt.axis('equal')
plt.show()

# 2. Group Comparison Bar Chart
plt.figure(figsize=(10, 6))
x = np.arange(len(groups))
plt.bar(x, process_counts, color=colors)
plt.xticks(x, groups)
plt.xlabel('Workflow Groups')
plt.ylabel('Number of Processes')
plt.title('Process Count per Workflow Group')
for i, v in enumerate(process_counts):
    plt.text(i, v + 0.1, str(v), ha='center')
plt.show()

# 3. FormKey Pattern Visualization
plt.figure(figsize=(12, 6))
plt.bar(groups, process_counts, color=colors)
plt.xlabel('Workflow Groups')
plt.ylabel('Number of Processes')
plt.title('FormKey Patterns in Workflow Groups')
for i, (count, pattern) in enumerate(zip(process_counts, formkey_patterns)):
    plt.text(i, count/2, pattern, ha='center', va='center', color='white', fontsize=12, fontweight='bold')
plt.show()

# 4. Process Timeline (Conceptual)
processes = [filename.replace(".bpmn20.xml", "") for filename in os.listdir(bpmn_dir) if filename.endswith(".bpmn20.xml")]
durations = np.random.randint(5, 30, size=len(processes))  # Simulated durations

plt.figure(figsize=(14, 8))
plt.barh(processes, durations, color='skyblue')
plt.xlabel('Processing Time (minutes)')
plt.ylabel('Processes')
plt.title('Simulated Process Durations')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()
