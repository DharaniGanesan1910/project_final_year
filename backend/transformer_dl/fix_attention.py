import numpy as np

MAX_LENGTH = 128  # same as used in transformer extraction

# Load your saved file
attention_object = np.load("attention_scores.npy", allow_pickle=True)

print("Original dtype:", attention_object.dtype)
print("Total samples:", len(attention_object))

fixed_attention = []

for att in attention_object:
    att = np.array(att)

    if len(att) < MAX_LENGTH:
        padded = np.pad(att, (0, MAX_LENGTH - len(att)))
    else:
        padded = att[:MAX_LENGTH]

    fixed_attention.append(padded)

fixed_attention = np.vstack(fixed_attention)

print("New Shape:", fixed_attention.shape)

# Save clean version
np.save("attention_scores_fixed.npy", fixed_attention)

print("Saved: attention_scores_fixed.npy")
