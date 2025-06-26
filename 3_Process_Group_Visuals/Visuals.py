import matplotlib.pyplot as plt
import numpy as np

# Group distribution
groups = ['Group 1', 'Group 2', 'Group 3']
counts = [3, 5, 2]
colors = ['#FF9999', '#66B3FF', '#99FF99']

# Group distribution pie chart
plt.figure(figsize=(8, 6))
plt.pie(counts, labels=groups, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Workflow Group Distribution')
plt.tight_layout()
plt.show()

# FormKey sequence frequency
formkeys = ['252', '254', '256']
frequencies = [50, 30, 20]  # percentage

# Sequence frequency bar chart
plt.figure(figsize=(8, 5))
plt.bar(formkeys, frequencies, color='#4C72B0')
plt.xlabel('Third FormKey')
plt.ylabel('Frequency (%)')
plt.title('Third Task FormKey Distribution')
plt.ylim(0, 60)
for i, v in enumerate(frequencies):
    plt.text(i, v + 1, f"{v}%", ha='center')
plt.tight_layout()
plt.show()

# Duration comparison
tasks = ['165→173', '173→252', '173→254', '173→256']
durations = [5, 22, 18, 15]  # minutes

# Duration comparison chart
plt.figure(figsize=(10, 5))
plt.plot(tasks, durations, marker='o', linestyle='-', color='#55A868')
plt.xlabel('Task Transition')
plt.ylabel('Avg Duration (min)')
plt.title('Task Transition Durations')
plt.grid(alpha=0.3)
for i, v in enumerate(durations):
    plt.text(i, v + 0.5, f"{v}min", ha='center')
plt.tight_layout()
plt.show()
