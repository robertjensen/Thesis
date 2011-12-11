# Import modules
import csv, sys
import matplotlib.pyplot as plt
import numpy as np


# Open the data
datafile = sys.argv[1]
f = open(datafile, 'r')

for i in range(0,20):
    f.readline()

reader = csv.reader(f,delimiter='\t')

print f.readline()

series_dict = {}
for row in reader:
	i = 0
	for column in row:
		i += 1
		if series_dict.has_key(i):
			try:
				series_dict[i].append(float(column))
			except ValueError:
				pass
		else:
			series_dict[i] = [float(column)]
# Plot each data series
num_cols = len(series_dict)
i = 1 
while i < num_cols:
	plt.plot(series_dict[i], series_dict[i+1], 'o')
	i += 2 

# Get axis labels
xaxis_label = "x"
yaxis_label = "y"

# Show the plot
plt.ylabel(yaxis_label)
plt.xlabel(xaxis_label)
plt.show()

# Enter loop for customizing appearance

# Stop
f.close()

