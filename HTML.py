"""Convert project notebooks to HTML when the source notebooks are available."""

import subprocess
from pathlib import Path


NOTEBOOKS = [
    ("Coherence Score.ipynb", "Coherence Score.html"),
    ("graphs.ipynb", "graphs.html"),
]


def convert_notebook(notebook_file, html_file):
    notebook_path = Path(notebook_file)
    if not notebook_path.exists():
        print(f"Skipped {notebook_file}: source notebook is not present.")
        return

    command = [
        "jupyter",
        "nbconvert",
        "--to",
        "html",
        "--execute",
        str(notebook_path),
        "--output",
        html_file,
    ]
    process = subprocess.run(command, capture_output=True, text=True, check=False)

    if process.stdout:
        print("STDOUT:", process.stdout)
    if process.stderr:
        print("STDERR:", process.stderr)

    if process.returncode != 0:
        raise RuntimeError(f"Failed to generate {html_file} from {notebook_file}.")

    print(f"HTML file '{html_file}' has been generated successfully.")


def main():
    for notebook_file, html_file in NOTEBOOKS:
        convert_notebook(notebook_file, html_file)


if __name__ == "__main__":
    main()
