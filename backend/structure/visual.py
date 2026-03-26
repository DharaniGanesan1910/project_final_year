import matplotlib.pyplot as plt
import pandas as pd

# Load your processed file
df = pd.read_csv('pattern.csv')

# Get Top 5 patterns
pattern = df['predicted_structure'].value_counts().head(8)

# Plotting
plt.figure(figsize=(10, 6))
pattern.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Grammatical Structures in Tamil-English Code-Mixed Data', fontsize=14)
plt.xlabel('Grammatical Pattern (S-V-O-C-A)', fontsize=12)
plt.ylabel('Number of Sentences', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('structure_distribution.png')
print("Chart saved as structure_distribution.png")