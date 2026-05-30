# This script was generated from the corresponding Jupyter notebook.
# Source notebook: HTML.ipynb

# %% [code]
import subprocess

notebook_file = "Coherence Score.ipynb"
html_file = "Coherence Score.html"


cmd = f'jupyter nbconvert --to html --execute "{notebook_file}"'
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Print conversion output to help debug errors
print("STDOUT:", process.stdout)
print("STDERR:", process.stderr)

print(f"HTML file '{html_file}' has been generated successfully.")

# %% [code]
import os

# Define notebook file names
notebook_file = "graphs.ipynb"
html_file = "graphs.html"

# Run Jupyter nbconvert and execute notebooks to preserve all outputs
os.system(f"jupyter nbconvert --to html --execute {notebook_file}")

print(f"HTML file '{html_file}' has been generated successfully.")
