#!/usr/bin/env python3
"""
Generate HTML pages for interim builds directory structure.
Scans for build-numbered directories (builds/00001, builds/00002, etc.) 
and creates/updates index.html and individual build pages.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Base directory for builds
BASE_DIR = Path(__file__).parent
BUILDS_DIR = BASE_DIR / "builds"

# Template for individual date pages
BUILD_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Build #{build_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
        }}
        
        .back-link {{
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        h1 {{
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }}
        
        .build-display {{
            color: #666;
            font-size: 1.1rem;
        }}
        
        .info-section {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
        }}
        
        .info-section h2 {{
            color: #333;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }}
        
        .info-content {{
            color: #555;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        .files-section {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .files-section h2 {{
            color: #333;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }}
        
        .file-list {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .file-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            transition: background 0.3s;
        }}
        
        .file-item:hover {{
            background: #e9ecef;
        }}
        
        .file-name {{
            font-weight: 600;
            color: #333;
            flex: 1;
        }}
        
        .file-size {{
            color: #666;
            margin: 0 1rem;
        }}
        
        .file-download {{
            padding: 0.5rem 1rem;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.3s;
        }}
        
        .file-download:hover {{
            background: #5568d3;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 2rem;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="../../index.html" class="back-link">← Back to all builds</a>
            <h1>📦 Build #{build_id}</h1>
            <p class="build-display">Created: {created_date}</p>
        </div>
        
        <div class="info-section">
            <h2>📝 Build Information</h2>
            <div class="info-content">
<!-- INFO_START -->
{info}
<!-- INFO_END -->
            </div>
        </div>
        
        <div class="files-section">
            <h2>📁 Files ({file_count})</h2>
            <div class="file-list">
<!-- FILES_START -->
{files}
<!-- FILES_END -->
            </div>
        </div>
    </div>
    
    <script>
        // GitHub configuration for raw file downloads
        const GITHUB_OWNER = 'r7l-labs';
        const GITHUB_REPO = 'interim-builds';
        const GITHUB_BRANCH = 'main';
        const BUILD_ID = '{build_id}';
        
        // Update all download links to use raw GitHub URLs
        document.addEventListener('DOMContentLoaded', function() {{
            const downloadLinks = document.querySelectorAll('.file-download');
            downloadLinks.forEach(link => {{
                const filename = link.getAttribute('data-filename');
                if (filename) {{
                    const rawUrl = `https://raw.githubusercontent.com/${{GITHUB_OWNER}}/${{GITHUB_REPO}}/${{GITHUB_BRANCH}}/builds/${{BUILD_ID}}/${{filename}}`;
                    link.href = rawUrl;
                }}
            }});
        }});
    </script>
</body>
</html>
"""

def format_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def is_build_directory(name):
    """Check if directory name matches build ID pattern (00001, 00002, etc.)."""
    return bool(re.match(r'^\d{5}$', name))

def get_build_directories():
    """Get all directories that match build ID pattern."""
    if not BUILDS_DIR.exists():
        BUILDS_DIR.mkdir(exist_ok=True)
        return []
    
    dirs = []
    for item in BUILDS_DIR.iterdir():
        if item.is_dir() and is_build_directory(item.name):
            jar_files = list(item.glob('*.jar'))
            # Get creation time
            try:
                created = datetime.fromtimestamp(item.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            except:
                created = 'Unknown'
            
            dirs.append({
                'name': item.name,
                'build_id': item.name,
                'path': item,
                'file_count': len(jar_files),
                'created': created
            })
    # Sort by build ID (newest first)
    dirs.sort(key=lambda x: x['name'], reverse=True)
    return dirs

def get_next_build_id():
    """Get the next available build ID."""
    builds = get_build_directories()
    if not builds:
        return "00001"
    
    # Get the highest build number
    max_id = max(int(b['build_id']) for b in builds)
    return f"{max_id + 1:05d}"

def read_existing_info(html_file):
    """Read existing info section from HTML file if it exists."""
    if not html_file.exists():
        return "No information added yet. Edit this HTML file to add build notes, changelog, or other details."
    
    try:
        content = html_file.read_text(encoding='utf-8')
        match = re.search(r'<!-- INFO_START -->\n(.*?)\n<!-- INFO_END -->', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not read existing info from {html_file}: {e}")
    
    return "No information added yet. Edit this HTML file to add build notes, changelog, or other details."

def generate_build_page(build_dir):
    """Generate HTML page for a specific build directory."""
    build_id = build_dir['build_id']
    build_path = build_dir['path']
    html_file = build_path / 'index.html'
    
    # Skip if index.html already exists
    if html_file.exists():
        print(f"Skipped: {html_file} (already exists)")
        return
    
    # Get default info for new pages
    existing_info = "No information added yet. Edit this HTML file to add build notes, changelog, or other details."
    
    # Get JAR files
    jar_files = sorted(build_path.glob('*.jar'))
    
    # Generate file list HTML
    if jar_files:
        files_html = []
        for jar_file in jar_files:
            size = jar_file.stat().st_size
            files_html.append(f'''                <div class="file-item">
                    <span class="file-name">{jar_file.name}</span>
                    <span class="file-size">{format_size(size)}</span>
                    <a href="#" class="file-download" data-filename="{jar_file.name}" download="{jar_file.name}">Download</a>
                </div>''')
        files_content = '\n'.join(files_html)
    else:
        files_content = '''                <div class="empty-state">
                    <p>No JAR files found</p>
                </div>'''
    
    # Generate the page
    html_content = BUILD_PAGE_TEMPLATE.format(
        build_id=build_id,
        created_date=build_dir['created'],
        info=existing_info,
        file_count=len(jar_files),
        files=files_content
    )
    
    # Write the file
    html_file.write_text(html_content, encoding='utf-8')
    print(f"Generated: {html_file}")

def update_index_page(directories):
    """Update the main index.html with directory listings."""
    index_file = BASE_DIR / 'index.html'
    
    if not index_file.exists():
        print("Error: index.html not found!")
        return
    
    # Read existing index.html
    content = index_file.read_text(encoding='utf-8')
    
    # Generate directory listing HTML
    if directories:
        dir_html = []
        for dir_info in directories:
            file_s = 's' if dir_info['file_count'] != 1 else ''
            dir_html.append(f'''                <a href="builds/{dir_info['name']}/index.html" class="directory-item">
                    <div class="directory-name">Build #{dir_info['build_id']}</div>
                    <div class="directory-files">{dir_info['file_count']} file{file_s} • {dir_info['created']}</div>
                </a>''')
        dir_content = '\n'.join(dir_html)
    else:
        dir_content = '''                <div class="empty-state">
                    <p>No builds yet. Upload JAR files via FTP to builds/00001/ and run the generator script.</p>
                </div>'''
    
    # Replace the directory list section
    new_content = re.sub(
        r'<!-- DIRECTORIES_LIST_START -->.*?<!-- DIRECTORIES_LIST_END -->',
        f'<!-- DIRECTORIES_LIST_START -->\n{dir_content}\n                <!-- DIRECTORIES_LIST_END -->',
        content,
        flags=re.DOTALL
    )
    
    # Write updated index
    index_file.write_text(new_content, encoding='utf-8')
    print(f"Updated: {index_file}")

def main():
    """Main function to generate all HTML files."""
    print("Scanning for build directories...")
    
    # Ensure builds directory exists
    BUILDS_DIR.mkdir(exist_ok=True)
    
    directories = get_build_directories()
    
    dir_word = 'ies' if len(directories) != 1 else 'y'
    print(f"Found {len(directories)} build director{dir_word}")
    
    if directories:
        print(f"Next build ID will be: {get_next_build_id()}")
    
    # Generate individual build pages
    for dir_info in directories:
        generate_build_page(dir_info)
    
    # Update main index
    update_index_page(directories)
    
    print("\n✅ All HTML files generated successfully!")
    print(f"Open {BASE_DIR}/index.html in a browser to view.")
    print(f"\nTo add a new build:")
    print(f"  1. Create directory: builds/{get_next_build_id()}/")
    print(f"  2. Upload JAR files to that directory")
    print(f"  3. Run: python3 generate.py")

if __name__ == '__main__':
    main()
