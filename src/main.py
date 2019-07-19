from BUStoolsPython import *
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Generates pretty pictures")
parser.add_argument("--b", help="busfile")
args = parser.parse_args()

# Process file
print('Processing file...')

f = BUSFile(args.b)
h = f.readheader()

knee = set()

for rec in f:
#for i in range(200):
#    rec = f.readline()
    k = (rec.bc, rec.umi)
    knee.add(k)

f.close()

# Process data
print('Processing data...')

knee = pd.DataFrame(([bc, umi] for bc, umi in knee),
        columns = ['bc', 'umi'])
knee = knee.groupby('bc', as_index = False).count()
knee = knee.sort_values(by = ['umi'], ascending = False)

# Plot things
print('Plotting dastardly things...')

fig, ax = plt.subplots(figsize=(10, 7))
ax.loglog(knee['umi'].tolist(), range(len(knee)), linewidth=5)

ax.set_xlabel("UMI Counts")
ax.set_ylabel("Set of Barcodes")

plt.grid(True, which="both")

plt.savefig("figures.pdf", bbox_inches='tight')

