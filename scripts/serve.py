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
    print("\n📦 Installing MkDocs and plugins...")
    run_command(f"{activate_cmd} && pip install -r ../requirements.txt",
                 "Failed to install dependencies")

# def install_dependencies(activate_cmd):
#     """Install MkDocs and required plugins."""
#     print("\n📦 Installing MkDocs and plugins...")
    
#     # List of packages to install
#     packages = [
#         "mkdocs",
#         "mkdocs-material",
#         "mkdocs-awesome-pages-plugin",
#         "mkdocs-git-revision-date-localized-plugin",
#         "mkdocs-minify-plugin",
#         "pymdown-extensions",
#         "pillow",
#         "cairosvg"
#     ]
    
#     # Install packages
#     packages_str = " ".join(packages)
#     run_command(f"{activate_cmd} && pip install {packages_str}",
#                "Failed to install dependencies")
    
#     print("✓ All dependencies installed successfully")



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