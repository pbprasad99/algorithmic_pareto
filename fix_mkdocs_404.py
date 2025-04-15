#!/usr/bin/env python3
import os
import sys
import argparse

def create_index_files(docs_dir):
    """Create index.md files in all directories without them."""
    print(f"Creating index.md files in {docs_dir} subdirectories...")
    
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            index_path = os.path.join(dir_path, "index.md")
            
            if not os.path.exists(index_path):
                # Create the directory title
                title = dir_name.replace('-', ' ').replace('_', ' ').title()
                
                # Create a list of markdown files in this directory
                md_files = []
                for file in os.listdir(dir_path):
                    if file.endswith('.md') and file != 'index.md':
                        file_name = os.path.splitext(file)[0]
                        file_title = file_name.replace('-', ' ').replace('_', ' ').title()
                        md_files.append((file_name, file_title))
                
                # Create index.md with links to all markdown files
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(f"""---
title: {title}
---

# {title}

""")
                    # Add links to child directories
                    child_dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
                    if child_dirs:
                        f.write("## Sections\n\n")
                        for child_dir in child_dirs:
                            child_title = child_dir.replace('-', ' ').replace('_', ' ').title()
                            f.write(f"- [{child_title}]({child_dir}/)\n")
                        f.write("\n")
                    
                    # Add links to markdown files
                    if md_files:
                        f.write("## Topics\n\n")
                        for file_name, file_title in md_files:
                            f.write(f"- [{file_title}]({file_name}.md)\n")
                
                print(f"Created index.md in {dir_path}")
                count += 1
    
    print(f"Created {count} index.md files")

def main():
    parser = argparse.ArgumentParser(description="Fix MkDocs 404 errors by creating index files")
    parser.add_argument("--docs-dir", default="docs", help="Path to the docs directory")
    args = parser.parse_args()
    
    docs_dir = os.path.abspath(args.docs_dir)
    
    if not os.path.isdir(docs_dir):
        print(f"Error: Directory {docs_dir} does not exist.")
        sys.exit(1)
    
    create_index_files(docs_dir)
    
    print("""
✅ Fix completed!

Next steps:
1. Run 'mkdocs serve' to preview the changes
2. If everything looks good, commit and push the changes
3. GitHub Actions will automatically deploy the updated site
""")

if __name__ == "__main__":
    main()