#!/usr/bin/env python3
"""
Serve Mkdocs site locally using UV and Python 3.10+.

Usage: 
cd algorithmic_pareto/scripts
python serve.py --repo-dir .. --username pbprasad99 --repo-name algorithmic_pareto

Notes:
- On Windows, ensure Python 3.10+ and UV are installed and available in your PATH.
- If you install Python or UV during your session, restart your terminal or update your PATH.
- This script is cross-platform and will work on macOS, Linux, and Windows as long as prerequisites are met.
"""
import os
import subprocess
import sys
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

def find_python_and_uv():
    """Find python3.12, python3.11, python3.10, python3, or python (>=3.10) and uv executables. Error if no suitable python or uv is found."""
    import shutil
    # Try python3.12, python3.11, python3.10, python3, python in order
    for py in ["python3.12", "python3.11", "python3.10", "python3", "python"]:
        py_exec = shutil.which(py)
        if py_exec:
            # Check version
            try:
                version_str = subprocess.run([py_exec, "--version"], check=True, text=True, capture_output=True).stdout.strip()
                version_num = tuple(map(int, version_str.split()[1].split(".")[:2]))
                if version_num >= (3, 10):
                    break
            except Exception:
                continue
    else:
        print("Error: Python 3.10 or greater is required but was not found in your PATH. Please install Python 3.10+ and try again.")
        sys.exit(1)
    uv_exec = shutil.which("uv")
    if not uv_exec:
        print("Error: uv is required but was not found in your PATH. Please install it from https://github.com/astral-sh/uv.")
        sys.exit(1)
    return py_exec, uv_exec

def check_prerequisites():
    """Check if required tools are installed."""
    python_exec, uv_exec = find_python_and_uv()
    # Check Python version
    try:
        version_str = run_command(f"{python_exec} --version", "Python 3.10+ is not installed")
        version_num = tuple(map(int, version_str.strip().split()[1].split(".")[:2]))
        if version_num < (3, 10):
            print("Error: Python 3.10 or higher is required.")
            sys.exit(1)
        print(f"✓ {python_exec} is installed: {version_str}")
    except Exception as e:
        print(f"Error: Could not determine Python 3.10+ version: {e}")
        sys.exit(1)
    # Check for git
    try:
        run_command("git --version", "git is not installed")
        print("✓ git is installed")
    except:
        print("Error: git is not installed")
        sys.exit(1)
    # Check for uv
    try:
        run_command(f"{uv_exec} --version", "uv is not installed")
        print("✓ uv is installed")
    except:
        print("Error: uv is not installed. Please install it from https://github.com/astral-sh/uv.")
        sys.exit(1)
    return python_exec, uv_exec

def setup_uv_env(project_dir, python_exec, uv_exec):
    """Create a UV venv with Python 3.10+ only."""
    print(f"\n🔧 Setting up UV environment ({python_exec} only)...")
    venv_dir = os.path.join(project_dir, ".uv_venv")
    if os.path.exists(venv_dir):
        print("UV environment already exists. Skipping creation.")
    else:
        run_command(f"{uv_exec} venv {venv_dir} --python={python_exec}", f"Failed to create UV venv with {python_exec}")
    # Return the path to the Python executable in the venv
    py_version = os.path.basename(python_exec)
    if sys.platform == "win32":
        python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
        mkdocs_bin = os.path.join(venv_dir, "Scripts", "mkdocs")
        venv_bin = os.path.join(venv_dir, "Scripts")
    else:
        # Try to find the correct python binary in the venv
        python_bin = os.path.join(venv_dir, "bin", py_version)
        if not os.path.exists(python_bin):
            python_bin = os.path.join(venv_dir, "bin", "python3")
        mkdocs_bin = os.path.join(venv_dir, "bin", "mkdocs")
        venv_bin = os.path.join(venv_dir, "bin")
    return python_bin, mkdocs_bin, venv_dir, venv_bin

def install_dependencies(venv_dir, venv_bin, uv_exec):
    print("\n📦 Installing MkDocs and plugins with UV...")
    req_path = os.path.abspath(os.path.join(venv_dir, "..", "requirements.txt"))
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = venv_dir
    env["PATH"] = venv_bin + os.pathsep + env.get("PATH", "")
    try:
        result = subprocess.run(
            [uv_exec, "pip", "install", "-r", req_path],
            check=True,
            text=True,
            capture_output=True,
            env=env
        )
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies with UV: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def run_mkdocs_serve(project_dir, mkdocs_bin, venv_bin):
    """Run MkDocs serve to preview the site using the UV environment."""
    print("\n🌐 Starting MkDocs server for preview...")
    print("   (Press Ctrl+C to stop the server when done)")
    os.chdir(project_dir)
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = os.path.dirname(venv_bin)
    env["PATH"] = venv_bin + os.pathsep + env.get("PATH", "")
    subprocess.run([mkdocs_bin, "serve"], env=env)

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
    python_exec, uv_exec = check_prerequisites()
    
    # Setup UV environment
    python_bin, mkdocs_bin, venv_dir, venv_bin = setup_uv_env(project_dir, python_exec, uv_exec)
    
    # Install dependencies (use uv)
    install_dependencies(venv_dir, venv_bin, uv_exec)
    
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
        run_mkdocs_serve(project_dir, mkdocs_bin, venv_bin)

if __name__ == "__main__":
    main()