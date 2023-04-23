import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Define the matrix
matrix = [['', 'C', 'P'], ['R', '', ''], ['', '', 'R']]

# Define the color map for the matrix values
color_dict = {'C': 'red', 'R': 'grey', 'P': 'green'}  # Rename the dictionary to "color_dict"
cmap = colors.ListedColormap([color_dict.get(val, 'white') for val in set(np.ravel(matrix))])

# Convert the matrix to a numerical array
data = np.zeros((3, 3), dtype=int)
for i in range(3):
    for j in range(3):
        if matrix[i][j] == 'C':
            data[i, j] = 3
        elif matrix[i][j] == 'R':
            data[i, j] = 2
        elif matrix[i][j] == 'P':
            data[i, j] = 1

# Plot the matrix
fig, ax = plt.subplots()
im = ax.imshow(data, cmap=cmap)

# Add color bar
cbar = ax.figure.colorbar(im, ax=ax, ticks=[0, 1, 2])
cbar.ax.set_yticklabels(['R', 'C', 'P'])

# Add grid lines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-0.5, 3.5, 1))
ax.set_yticks(np.arange(-0.5, 3.5, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])

# Add labels
for i in range(3):
    for j in range(3):
        ax.text(j, i, matrix[i][j], ha='center', va='center', color='w')

# Show the plot
plt.show()
