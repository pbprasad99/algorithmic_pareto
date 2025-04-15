#!/usr/bin/env python3
"""
python convert_to_mkdocs.py --repo-dir . --username pbprasad99 --repo-name algorithmic_pareto
"""
import os
import subprocess
import sys
import yaml
import argparse
import re
from pathlib import Path
import shutil

def run_command(command, error_message="An error occurred"):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def check_prerequisites():
    """Check if required tools are installed."""
    # Check for Python 3.6+
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)
        
    # Check for pip
    try:
        run_command("pip --version", "pip is not installed")
        print("✓ pip is installed")
    except:
        print("Error: pip is not installed")
        sys.exit(1)
        
    # Check for git
    try:
        run_command("git --version", "git is not installed")
        print("✓ git is installed")
    except:
        print("Error: git is not installed")
        sys.exit(1)

def setup_virtual_env(project_dir):
    """Create and activate a virtual environment."""
    print("\n🔧 Setting up virtual environment...")
    venv_dir = os.path.join(project_dir, "venv")
    
    # Check if venv already exists
    if os.path.exists(venv_dir):
        print("Virtual environment already exists. Skipping creation.")
    else:
        # Create virtual environment
        run_command(f"python -m venv {venv_dir}", 
                    "Failed to create virtual environment")
    
    # Determine the activate script based on the OS
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        # For Windows, return the command to activate
        return f"call {activate_script}"
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
        # For Unix, return the command to activate
        return f"source {activate_script}"

def install_dependencies(activate_cmd):
    """Install MkDocs and required plugins."""
    print("\n📦 Installing MkDocs and plugins...")
    
    # List of packages to install
    packages = [
        "mkdocs",
        "mkdocs-material",
        "mkdocs-awesome-pages-plugin",
        "mkdocs-git-revision-date-localized-plugin",
        "mkdocs-minify-plugin",
        "pymdown-extensions",
        "pillow",
        "cairosvg"
    ]
    
    # Install packages
    packages_str = " ".join(packages)
    run_command(f"{activate_cmd} && pip install {packages_str}",
               "Failed to install dependencies")
    
    print("✓ All dependencies installed successfully")

def create_custom_styles(project_dir):
    """Create custom CSS for MkDocs."""
    print("\n🎨 Creating custom styles...")
    
    assets_dir = os.path.join(project_dir, "docs", "assets")
    css_dir = os.path.join(assets_dir, "css")
    
    # Create directories if they don't exist
    os.makedirs(css_dir, exist_ok=True)
    
    # Create custom CSS file
    with open(os.path.join(css_dir, "extra.css"), "w") as f:
        f.write("""
/* Custom styling for algorithmic pareto */
.md-typeset h1 {
    font-weight: 700;
    color: var(--md-primary-fg-color);
}

.md-typeset a {
    text-decoration: none;
    border-bottom: 1px dotted;
}

.md-typeset a:hover {
    border-bottom: 1px solid;
}

/* Custom dark theme adjustments */
[data-md-color-scheme="slate"] {
    --md-hue: 210; 
    --md-default-bg-color: hsla(var(--md-hue), 15%, 12%, 1);
    --md-code-bg-color: hsla(var(--md-hue), 15%, 15%, 1);
}

/* Improve code readability in dark mode */
[data-md-color-scheme="slate"] .md-typeset code {
    background-color: hsla(var(--md-hue), 15%, 18%, 1);
    color: #e6e6e6;
}

/* Algorithm styles */
.algorithm {
    border-left: 4px solid var(--md-primary-fg-color);
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

.algorithm h3 {
    color: var(--md-primary-fg-color);
    margin-top: 0;
}

/* Improve table readability in dark mode */
[data-md-color-scheme="slate"] .md-typeset table:not([class]) {
    background-color: hsla(var(--md-hue), 15%, 15%, 1);
    border: 1px solid hsla(var(--md-hue), 15%, 20%, 1);
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) th {
    background-color: hsla(var(--md-hue), 15%, 18%, 1);
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) tr:hover {
    background-color: hsla(var(--md-hue), 15%, 17%, 1);
}

/* Complexity badge styles */
.complexity-badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 0.5rem;
}

.time-complexity {
    background-color: rgba(76, 175, 80, 0.2);
    color: #4CAF50;
}

.space-complexity {
    background-color: rgba(33, 150, 243, 0.2);
    color: #2196F3;
}
""")

def process_markdown_files(project_dir):
    """Process existing markdown files to make them MkDocs compatible."""
    print("\n📄 Processing existing markdown files...")
    
    # Create docs directory if it doesn't exist
    docs_dir = os.path.join(project_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Create a copy of README.md as index.md if it exists
    readme_path = os.path.join(project_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # Create index.md with modified content
        with open(os.path.join(docs_dir, "index.md"), "w", encoding="utf-8") as f:
            # Add title metadata
            f.write("---\n")
            f.write("title: Home\n")
            f.write("---\n\n")
            f.write(readme_content)
    
    # Walk through the repo and copy all markdown files to docs directory
    # maintaining the same structure
    for root, dirs, files in os.walk(project_dir):
        # Skip the .git directory, venv directory, and docs directory itself
        if '.git' in dirs:
            dirs.remove('.git')
        if 'venv' in dirs:
            dirs.remove('venv')
        if 'site' in dirs:
            dirs.remove('site')
        if root == project_dir and 'docs' in dirs:
            dirs.remove('docs')
        
        # Process all markdown files
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                original_path = os.path.join(root, file)
                
                # Calculate relative path from project_dir
                rel_path = os.path.relpath(original_path, project_dir)
                
                # Create the corresponding path in docs directory
                target_dir = os.path.dirname(os.path.join(docs_dir, rel_path))
                os.makedirs(target_dir, exist_ok=True)
                
                # For directories that should be pages, create an index.md file
                if file == 'README.md' and root != project_dir:
                    rel_dir_path = os.path.relpath(root, project_dir)
                    target_dir = os.path.join(docs_dir, rel_dir_path)
                    target_path = os.path.join(target_dir, "index.md")
                else:
                    # Regular markdown file
                    target_path = os.path.join(docs_dir, rel_path)
                
                # Read the original file
                with open(original_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                
                # Add title metadata if not already present
                if not content.startswith('---'):
                    title = os.path.splitext(file)[0].replace('-', ' ').replace('_', ' ').title()
                    content = f"---\ntitle: {title}\n---\n\n{content}"
                
                # Write to the new location
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(content)
    
    # Now, for each directory in docs, create an index.md if it doesn't exist
    for root, dirs, files in os.walk(docs_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            index_path = os.path.join(dir_path, "index.md")
            
            if not os.path.exists(index_path):
                title = dir_name.replace('-', ' ').replace('_', ' ').title()
                
                # Create a simple index.md
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(f"""---
title: {title}
---

# {title}

This section contains content related to {title.lower()}.
""")

    # Also copy all images/assets to docs directory
    assets_dir = os.path.join(docs_dir, "assets", "images")
    os.makedirs(assets_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(project_dir):
        # Skip the same directories as before
        if '.git' in dirs:
            dirs.remove('.git')
        if 'venv' in dirs:
            dirs.remove('venv')
        if 'site' in dirs:
            dirs.remove('site')
        if root == project_dir and 'docs' in dirs:
            dirs.remove('docs')
        
        # Process image and asset files
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                original_path = os.path.join(root, file)
                
                # Copy the file to assets directory
                shutil.copy2(original_path, os.path.join(assets_dir, file))

# def process_markdown_files(project_dir):
#     """Process existing markdown files to make them MkDocs compatible."""
#     print("\n📄 Processing existing markdown files...")
    
#     # Create docs directory if it doesn't exist
#     docs_dir = os.path.join(project_dir, "docs")
#     os.makedirs(docs_dir, exist_ok=True)
    
#     # Create a copy of README.md as index.md if it exists
#     readme_path = os.path.join(project_dir, "README.md")
#     if os.path.exists(readme_path):
#         with open(readme_path, "r", encoding="utf-8") as f:
#             readme_content = f.read()
        
#         # Create index.md with modified content
#         with open(os.path.join(docs_dir, "index.md"), "w", encoding="utf-8") as f:
#             # Add title metadata
#             f.write("---\n")
#             f.write("title: Home\n")
#             f.write("---\n\n")
#             f.write(readme_content)
    
#     # Walk through the repo and copy all markdown files to docs directory
#     # maintaining the same structure
#     for root, dirs, files in os.walk(project_dir):
#         # Skip the .git directory, venv directory, and docs directory itself
#         if '.git' in dirs:
#             dirs.remove('.git')
#         if 'venv' in dirs:
#             dirs.remove('venv')
#         if root == project_dir and 'docs' in dirs:
#             dirs.remove('docs')
        
#         # Process all markdown files
#         for file in files:
#             if file.endswith('.md') and file != 'README.md':
#                 original_path = os.path.join(root, file)
                
#                 # Calculate relative path from project_dir
#                 rel_path = os.path.relpath(original_path, project_dir)
                
#                 # Create the corresponding path in docs directory
#                 target_dir = os.path.dirname(os.path.join(docs_dir, rel_path))
#                 os.makedirs(target_dir, exist_ok=True)
                
#                 # Read the original file
#                 with open(original_path, "r", encoding="utf-8", errors="replace") as f:
#                     content = f.read()
                
#                 # Add title metadata if not already present
#                 if not content.startswith('---'):
#                     title = os.path.splitext(file)[0].replace('-', ' ').replace('_', ' ').title()
#                     content = f"---\ntitle: {title}\n---\n\n{content}"
                
#                 # Write to the new location
#                 with open(os.path.join(docs_dir, rel_path), "w", encoding="utf-8") as f:
#                     f.write(content)
    
#     # Also copy all images/assets to docs directory
#     for root, dirs, files in os.walk(project_dir):
#         # Skip the same directories as before
#         if '.git' in dirs:
#             dirs.remove('.git')
#         if 'venv' in dirs:
#             dirs.remove('venv')
#         if root == project_dir and 'docs' in dirs:
#             dirs.remove('docs')
        
#         # Process image and asset files
#         for file in files:
#             if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
#                 original_path = os.path.join(root, file)
                
#                 # Calculate relative path from project_dir
#                 rel_path = os.path.relpath(original_path, project_dir)
                
#                 # Create assets directory in docs
#                 assets_dir = os.path.join(docs_dir, "assets", "images")
#                 os.makedirs(assets_dir, exist_ok=True)
                
#                 # Copy the file to assets directory
#                 shutil.copy2(original_path, os.path.join(assets_dir, file))
                
#                 # Note: You might want to update image references in markdown files
#                 # to point to the new location, but that would require parsing and
#                 # modifying markdown content, which is more complex

def create_mkdocs_config(project_dir, github_username, repo_name, blog_title):
    """Create the MkDocs configuration file."""
    print("\n📝 Creating MkDocs configuration...")
    
    config = {
        "site_name": blog_title,
        "site_url": f"https://{github_username}.github.io/{repo_name}/",
        "site_author": github_username,
        "site_description": f"{blog_title} - Algorithmic techniques and implementations",
        "repo_name": f"{github_username}/{repo_name}",
        "repo_url": f"https://github.com/{github_username}/{repo_name}",
        "edit_uri": "edit/main/docs/",
        
        "theme": {
            "name": "material",
            "palette": [
                {
                    "media": "(prefers-color-scheme: dark)",
                    "scheme": "slate",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {
                        "icon": "material/weather-sunny",
                        "name": "Switch to light mode"
                    }
                },
                {
                    "media": "(prefers-color-scheme: light)",
                    "scheme": "default",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {
                        "icon": "material/weather-night",
                        "name": "Switch to dark mode"
                    }
                }
            ],
            "features": [
                "navigation.instant",
                "navigation.tracking",
                "navigation.tabs",
                "navigation.sections",
                "navigation.expand",
                "navigation.indexes",
                "search.suggest",
                "search.highlight",
                "content.tabs.link",
                "content.code.copy",
                "content.code.annotate"
            ],
            "icon": {
                "repo": "fontawesome/brands/github"
            }
        },
        
        "extra_css": [
            "assets/css/extra.css"
        ],
        
        "markdown_extensions": [
            "pymdownx.highlight",
            "pymdownx.superfences",
            "pymdownx.inlinehilite",
            "pymdownx.tabbed",
            "pymdownx.critic",
            "pymdownx.tasklist",
            "pymdownx.emoji",
            "admonition",
            "footnotes",
            "toc",
            {"toc": {"permalink": True}}
        ],
        
        "plugins": [
            "search",
            "minify",
            "awesome-pages",
            {"git-revision-date-localized": {"enable_creation_date": True}}
        ]
    }
    
    with open(os.path.join(project_dir, "mkdocs.yml"), "w") as f:
        yaml.dump(config, f, sort_keys=False, default_flow_style=False)

def setup_github_pages(project_dir):
    """Set up GitHub Pages deployment."""
    print("\n🚀 Setting up GitHub Pages deployment...")
    
    # Create GitHub workflow directory
    workflows_dir = os.path.join(project_dir, ".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Create GitHub Actions workflow file
    with open(os.path.join(workflows_dir, "deploy.yml"), "w") as f:
        f.write("""name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin pymdown-extensions pillow cairosvg
      
      - name: Deploy
        run: mkdocs gh-deploy --force
""")
    
    # Create requirements.txt if it doesn't exist
    req_path = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(req_path):
        with open(req_path, "w") as f:
            f.write("""mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocs-awesome-pages-plugin>=2.9.0
mkdocs-git-revision-date-localized-plugin>=1.2.0
mkdocs-minify-plugin>=0.6.0
pymdown-extensions>=10.0.0
pillow>=9.5.0
cairosvg>=2.7.0
""")

def create_index_page(project_dir):
    """Create or update the index page with additional information."""
    index_path = os.path.join(project_dir, "docs", "index.md")
    
    # Read existing content if file exists
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = """---
title: Home
---

# Algorithmic Pareto

A collection of algorithms and data structures for efficient problem-solving.
"""
    
    # Add additional information if not already present
    if "## Algorithm Categories" not in content:
        content += """

## Algorithm Categories

This repository contains implementations and explanations of various algorithms categorized by approach:

- **Iterative**: Algorithms that use loops and iterations
- **Recursive**: Algorithms that call themselves to solve subproblems
- **Dynamic Programming**: Algorithms that break down problems into simpler subproblems
- **Greedy**: Algorithms that make locally optimal choices at each step

## How to Use This Resource

Navigate through the sections to find detailed explanations, implementations, and complexity analysis for each algorithm.

"""
    
    # Write updated content
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

def run_mkdocs_serve(project_dir, activate_cmd):
    """Run MkDocs serve to preview the site."""
    print("\n🌐 Starting MkDocs server for preview...")
    print("   (Press Ctrl+C to stop the server when done)")
    
    os.chdir(project_dir)
    subprocess.run(f"{activate_cmd} && mkdocs serve", shell=True)

def main():
    parser = argparse.ArgumentParser(description="Convert a GitHub repository to MkDocs blog")
    parser.add_argument("--repo-dir", required=True, help="Path to the repository directory")
    parser.add_argument("--username", required=True, help="Your GitHub username")
    parser.add_argument("--repo-name", required=True, help="Repository name")
    parser.add_argument("--title", default="Algorithmic Pareto", help="Blog title")
    parser.add_argument("--no-serve", action="store_true", help="Skip running MkDocs serve after setup")
    args = parser.parse_args()
    
    project_dir = os.path.abspath(args.repo_dir)
    
    print(f"🚀 Converting repository to MkDocs blog: {project_dir}")
    
    # Check if the directory exists and is a git repository
    if not os.path.isdir(project_dir):
        print(f"Error: Directory {project_dir} does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(os.path.join(project_dir, ".git")):
        print(f"Warning: {project_dir} does not appear to be a git repository.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Check prerequisites
    check_prerequisites()
    
    # Setup virtual environment
    activate_cmd = setup_virtual_env(project_dir)
    
    # Install dependencies
    install_dependencies(activate_cmd)
    
    # Process existing markdown files
    process_markdown_files(project_dir)
    
    # Create custom styles
    create_custom_styles(project_dir)
    
    # Create or update index page
    create_index_page(project_dir)
    
    # Create MkDocs configuration
    create_mkdocs_config(project_dir, args.username, args.repo_name, args.title)
    
    # Setup GitHub Pages deployment
    setup_github_pages(project_dir)
    
    print(f"\n✅ Repository successfully converted to MkDocs blog!")
    print(f"   Location: {project_dir}")
    print(f"   Blog title: {args.title}")
    print(f"   GitHub username: {args.username}")
    print(f"   Repository name: {args.repo_name}")
    
    print("\nNext steps:")
    print("1. Review the generated MkDocs configuration in mkdocs.yml")
    print("2. Check the processed markdown files in the docs/ directory")
    print("3. Commit and push the changes to GitHub")
    print("4. GitHub Actions will automatically deploy the site to GitHub Pages")
    
    if not args.no_serve:
        run_mkdocs_serve(project_dir, activate_cmd)

if __name__ == "__main__":
    main()