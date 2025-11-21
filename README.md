# Interim Builds

A static HTML file browser for JAR builds organized by sequential build numbers.

## Overview

This system generates HTML pages that list JAR files uploaded to numbered build directories. It's designed to work with FTP uploads - you upload your JAR files to the next available build folder (00001, 00002, etc.), then run the generator script to create/update the HTML pages.

## Structure

```
interim-builds/
├── index.html              # Main page listing all builds
├── generate.py             # Script to generate/update HTML files
├── builds/                 # Container for all builds
│   ├── 00001/             # Build #00001
│   │   ├── index.html     # Auto-generated page for this build
│   │   ├── file1.jar      # Your JAR files
│   │   └── file2.jar
│   ├── 00002/             # Build #00002
│   │   ├── index.html
│   │   └── file.jar
│   └── 00003/             # Build #00003 (next build)
│       └── ...
```

## Usage

### 1. Upload Files via FTP

Create a directory with the next sequential build number (e.g., `builds/00001`, `builds/00002`) and upload your JAR files into it.

```bash
# Example structure:
builds/00001/
  ├── myapp-v1.0.jar
  └── myapp-v1.1.jar

builds/00002/
  └── myapp-v1.2.jar
```

### 2. Generate Build Pages

Run the generator script to create/update individual build HTML pages:

```bash
python3 generate.py
```

This will:
- Scan the `builds/` directory for numbered folders (00001, 00002, etc.)
- Generate/update an `index.html` in each build directory
- Show you the next available build number

**Note**: The main index.html automatically detects builds using JavaScript, so you don't need to regenerate it unless you want to update timestamps.

### 3. Add Build Information

After the HTML pages are generated, you can manually edit any build's `index.html` file to add build notes:

```html
<!-- INFO_START -->
Add your build information here:
- Version: 1.0.0
- Changes: Fixed critical bug in authentication
- Known issues: None
<!-- INFO_END -->
```

**Important:** Only edit the content between `<!-- INFO_START -->` and `<!-- INFO_END -->`. The generator script preserves this section when regenerating pages.

## Features

- **Sequential Build Numbers**: Builds are numbered automatically (00001, 00002, 00003, etc.)
- **Auto-Detection**: 
  - Index page uses JavaScript to automatically detect builds via GitHub API
  - Falls back to sequential detection if API is unavailable
  - No need to manually update the index page
- **GitHub Raw Downloads**: Download links point directly to raw GitHub URLs for reliable file access
- **File Listing**: Shows all JAR files in each build with file sizes
- **Editable Build Info**: Each build page has a section where you can manually add build notes, changelogs, etc.
- **Persistent Edits**: Your manual edits to the info section are preserved when regenerating pages
- **Clean UI**: Modern, responsive design that works on all devices
- **Timestamps**: Shows creation date for each build

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Example Workflow

1. **Check next build number:**
   ```bash
   python3 generate.py
   # Output shows: "Next build ID will be: 00003"
   ```

2. **Upload via FTP:**
   ```
   Upload myapp.jar to /builds/00003/
   ```

3. **Generate pages:**
   ```bash
   python3 generate.py
   ```

4. **Edit build info:**
   Open `/builds/00003/index.html` and edit the section between the INFO markers

5. **View in browser:**
   Open `index.html` in any web browser

## Tips

- Always use 5-digit build numbers: `00001`, `00002`, `00003`, etc.
- The main index.html uses JavaScript to auto-detect builds - it will work automatically once deployed to GitHub Pages
- Run `generate.py` only when you add new builds or want to update individual build pages
- The script is safe to run multiple times - it preserves your manual edits
- You can have multiple JAR files in each build directory
- Builds are displayed newest first on the main index page
- Download links use GitHub's raw content URLs for direct file access

## License

See LICENSE file for details.
