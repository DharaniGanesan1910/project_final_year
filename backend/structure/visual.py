import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load dataset
df = pd.read_csv("pattern.csv")

# Get top patterns
pattern_counts = df['predicted_structure'].value_counts().head(8)

# Convert to 2D format (required for heatmap)
heatmap_data = pd.DataFrame(pattern_counts).T

# Plot heatmap
plt.figure(figsize=(12, 4))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt="d",
    cmap="Blues",
    linewidths=0.5,
    cbar=True
)

plt.title("Grammatical Structures Heatmap (Tamil-English Code-Mixed)")
plt.xlabel("Grammatical Pattern (S-V-O-C-A)")
plt.ylabel("Frequency Row")

plt.tight_layout()
plt.savefig("structure_heatmap.png", dpi=300)
plt.show()

print("Heatmap saved as structure_heatmap.png")