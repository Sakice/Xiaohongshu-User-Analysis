# This script was generated from the corresponding Jupyter notebook.
# Source notebook: HTML.ipynb

# %% [code]
import subprocess

notebook_file = "/Users/sakice/Library/Mobile Documents/com~apple~CloudDocs/Documents/DP/analysis_notebook/Coherence Score.ipynb"
html_file = "/Users/sakice/Library/Mobile Documents/com~apple~CloudDocs/Documents/DP/analysis_notebook/Coherence Score.html"


cmd = f'jupyter nbconvert --to html --execute "{notebook_file}"'
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# 打印转换过程中的输出（如果有错误，可以帮助调试）
print("STDOUT:", process.stdout)
print("STDERR:", process.stderr)

print(f"HTML file '{html_file}' has been generated successfully.")

# %% [code]
import os

# 定义 Notebook 文件名
notebook_file = "/Users/sakice/Library/Mobile Documents/com~apple~CloudDocs/Documents/DP/analysis_notebook/graphs.ipynb"
html_file = "/Users/sakice/Library/Mobile Documents/com~apple~CloudDocs/Documents/DP/analysis_notebook/graphs.html"

# 运行 Jupyter nbconvert 并执行 Notebook 以保留所有输出
os.system(f"jupyter nbconvert --to html --execute {notebook_file}")

print(f"HTML file '{html_file}' has been generated successfully.")
