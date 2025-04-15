import os
import argparse
import re

"""
Usage :
python generate_docs_index.py . --readme README.md
"""
def generate_markdown_index(root_dir, github_base_url=None):
    """
    Generate a markdown index of folders as a string.
    
    Args:
        root_dir (str): Root directory to start traversing
        github_base_url (str, optional): Base URL for GitHub links.
    
    Returns:
        str: The generated markdown index as a string
    """
    result = ["# index\n"]
    
    base_len = len(root_dir.rstrip(os.sep))
    
    # Sort directories to ensure consistent output
    dir_list = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')  # Skip git directories
        
        # Skip root directory itself
        if root == root_dir:
            continue
            
        rel_path = root[base_len:].lstrip(os.sep)
        depth = rel_path.count(os.sep)
        dir_list.append((depth, rel_path, root))
    
    # Sort by path to ensure parent directories come before children
    dir_list.sort(key=lambda x: x[1])
    
    for depth, rel_path, root in dir_list:
        indent = '  ' * depth
        folder_name = os.path.basename(root)
        
        # Create link
        if github_base_url:
            # For GitHub, create a proper link to the folder
            link_path = rel_path.replace(os.sep, '/')
            link = f"{github_base_url}/{link_path}"
        else:
            # For local, just link to the folder
            link = rel_path.replace('\\','/')
        
        # Add entry to index
        result.append(f"{indent}- [{folder_name}]({link})")
    
    return "\n".join(result)

def update_readme_with_markers(readme_file, index_content, begin_marker, end_marker):
    """
    Update README file with index content between begin and end markers.
    Creates markers if they don't exist yet.
    
    Args:
        readme_file (str): Path to the README.md file
        index_content (str): Index content to insert
        begin_marker (str): Begin marker for index section
        end_marker (str): End marker for index section
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the entire file content
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for both markers in the content
        begin_index = content.find(begin_marker)
        end_index = content.find(end_marker)
        
        if begin_index != -1 and end_index != -1 and begin_index < end_index:
            # Both markers exist and are in the correct order
            # Replace content between markers (keeping the markers)
            before = content[:begin_index + len(begin_marker)]
            after = content[end_index:]
            new_content = f"{before}\n\n{index_content}\n\n{after}"
        elif begin_index != -1:
            # Only begin marker exists
            before = content[:begin_index + len(begin_marker)]
            new_content = f"{before}\n\n{index_content}\n\n{end_marker}"
        elif end_index != -1:
            # Only end marker exists (unusual case)
            after = content[end_index:]
            new_content = f"{begin_marker}\n\n{index_content}\n\n{after}"
        else:
            # No markers exist, append to the end
            new_content = f"{content}\n\n{begin_marker}\n\n{index_content}\n\n{end_marker}"
        
        # Write the updated content back to the file
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error updating README: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate markdown index for documentation folders.')
    parser.add_argument('root_dir', help='Root documentation directory')
    parser.add_argument('--output-file', help='Output markdown file (if not specified, prints to stdout)')
    parser.add_argument('--github-url', help='Base GitHub URL (e.g., https://github.com/username/repo/tree/main/docs)')
    parser.add_argument('--readme', help='README.md file to update with the index')
    parser.add_argument('--begin-marker', 
                        default='<!-- BEGIN_DOCS_INDEX -->',
                        help='Begin marker in README.md (default: <!-- BEGIN_DOCS_INDEX -->)')
    parser.add_argument('--end-marker', 
                        default='<!-- END_DOCS_INDEX -->',
                        help='End marker in README.md (default: <!-- END_DOCS_INDEX -->)')
    parser.add_argument('--no-title', action='store_true',
                        help='Omit the title from the documentation index')
    
    args = parser.parse_args()
    
    # Generate the index content
    if args.no_title:
        index_content = generate_markdown_index(args.root_dir, args.github_url).replace("# Index\n\n", "")
    else:
        index_content = generate_markdown_index(args.root_dir, args.github_url)
    
    if args.readme:
        # Update README.md with markers
        success = update_readme_with_markers(
            args.readme, 
            index_content, 
            args.begin_marker, 
            args.end_marker
        )
        if success:
            print(f"Successfully updated {args.readme} with the documentation index")
        else:
            print(f"Failed to update {args.readme}")
    elif args.output_file:
        # Write to a separate file
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"Index generated at {args.output_file}")
    else:
        # Print to stdout
        print(index_content)

if __name__ == "__main__":
    main()