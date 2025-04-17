# gen_pages.py
import mkdocs_gen_files
from pathlib import Path
import logging

log = logging.getLogger(f"mkdocs.plugins.{__name__}")
DOCS_DIR = Path("docs")

log.info("Scanning for Python files to generate Markdown pages...")

# Iterate through all .py files within the docs directory
for py_file in DOCS_DIR.rglob("*.py"):
    # Create the corresponding .md path relative to the docs directory
    relative_py_path = py_file.relative_to(DOCS_DIR)
    md_path = relative_py_path.with_suffix(".md")

    # Define the full path for checking existence (relative to project root)
    full_md_path = DOCS_DIR / md_path

    # Avoid overwriting existing Markdown files
    # Useful if you have manually created docs alongside generated ones
    # Note: mkdocs-gen-files works virtually, so Path.exists() checks the real filesystem.
    if full_md_path.exists():
        log.warning(f"Skipping generation for {py_file}: Corresponding Markdown file {full_md_path} already exists.")
        continue

    log.info(f"Generating Markdown for: {py_file} -> {md_path}")

    # Read the content of the Python file
    try:
        with open(py_file, "r", encoding="utf-8") as f_py:
            py_content = f_py.read()
    except Exception as e:
        log.error(f"Error reading file {py_file}: {e}")
        continue # Skip this file if reading fails

    # Use mkdocs_gen_files to create the Markdown file virtually
    # The 'edit_path' should point back to the original .py source file
    # relative to the docs directory.
    with mkdocs_gen_files.open(md_path, "w") as f_md:
        filename = py_file.name
        # Create a title using the filename
        f_md.write(f"# `{filename}`\n\n")
        # Embed the Python code in a fenced code block
        f_md.write("```python\n")
        f_md.write(py_content)
        f_md.write("\n```\n")

    # Set the edit path for the generated file to link back to the original .py file
    mkdocs_gen_files.set_edit_path(md_path, relative_py_path)

log.info("Finished generating Markdown pages for Python files.")