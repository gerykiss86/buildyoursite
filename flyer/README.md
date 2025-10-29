# LaTeX to PDF Flyer Generator

A professional LaTeX-based flyer generation system with Python automation script and beautiful two-sided flyer templates for Y2K Global OÜ.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Templates](#templates)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 Overview

This project provides:
- **Python script** (`latex_to_pdf.py`) for automated LaTeX to PDF conversion
- **Professional flyer template** with modern design, gradients, and typography
- **Two-sided A4 format** optimized for professional printing
- **Automatic cleanup** of auxiliary LaTeX files
- **Cross-platform support** (Windows, macOS, Linux)

## 🛠️ Prerequisites

### Required Software

1. **Python 3.x** - For running the conversion script
2. **LaTeX Distribution** - For compiling .tex files to PDF
3. **Git** (optional) - For version control

### Python Dependencies

No external Python packages required! Uses only standard library modules:
- `subprocess` - For running pdflatex
- `pathlib` - For file path handling
- `argparse` - For command-line arguments
- `shutil` - For checking system commands

## 📦 Installation

### Windows

#### Option 1: Using WinGet (Recommended)
```powershell
# Install MiKTeX (LaTeX distribution)
winget install --id MiKTeX.MiKTeX -e

# Add MiKTeX to PATH (replace USERNAME with your Windows username)
setx PATH "%PATH%;C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64"

# Restart terminal/command prompt after PATH update
```

#### Option 2: Manual Installation
1. Download MiKTeX from [https://miktex.org/download](https://miktex.org/download)
2. Run the installer and follow the setup wizard
3. Choose "Install for current user" (recommended)
4. MiKTeX will automatically manage package installation

### macOS

```bash
# Using Homebrew
brew install --cask mactex

# Or download MacTeX from https://tug.org/mactex/
# File size: ~4GB (full distribution)
```

### Linux

#### Ubuntu/Debian
```bash
# Full installation (recommended)
sudo apt-get update
sudo apt-get install texlive-full

# Minimal installation
sudo apt-get install texlive-base texlive-latex-recommended texlive-latex-extra
```

#### Fedora/RHEL
```bash
sudo dnf install texlive-scheme-full
```

#### Arch Linux
```bash
sudo pacman -S texlive-most
```

## 📁 Project Structure

```
flyer/
├── README.md                 # This documentation file
├── latex_to_pdf.py          # Python conversion script
├── flyer_template.tex       # Main flyer template
├── simple_test.tex          # Simple test document
├── y2k-logo-schwarz 512.png # Company logo
├── flyer_template.pdf       # Generated PDF output
└── simple_test.pdf          # Test PDF output
```

## 🚀 Usage

### Basic Usage

```bash
# Convert a LaTeX file to PDF
python latex_to_pdf.py flyer_template.tex

# Specify output directory
python latex_to_pdf.py flyer_template.tex -o ./output

# Keep auxiliary files (for debugging)
python latex_to_pdf.py flyer_template.tex --keep-aux

# Run multiple compilation passes (for complex documents)
python latex_to_pdf.py flyer_template.tex -r 3
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `tex_file` | Path to .tex file to compile | Required |
| `-o, --output-dir` | Output directory for PDF | Same as input |
| `-r, --runs` | Number of compilation runs | 2 |
| `--keep-aux` | Keep auxiliary files (.aux, .log, etc.) | False |

### Examples

```bash
# Simple conversion
python latex_to_pdf.py simple_test.tex

# Complex document with bibliography
python latex_to_pdf.py thesis.tex -r 3

# Debug mode (keep logs)
python latex_to_pdf.py document.tex --keep-aux

# Custom output location
python latex_to_pdf.py flyer.tex -o ~/Documents/PDFs/
```

## 📄 Templates

### Flyer Template Features

The `flyer_template.tex` includes:

**Design Elements:**
- Gradient backgrounds (blue to purple)
- Geometric patterns and ornaments
- Shadow effects and blur
- Professional color scheme
- FontAwesome 5 icons

**Layout:**
- Two-sided A4 format
- Full-bleed design (0mm margins)
- Responsive content boxes
- Multi-column layouts
- Call-to-action sections

**Typography:**
- Helvetica and Avant Garde fonts
- Multiple font sizes and weights
- German language support
- Proper hyphenation

### Required LaTeX Packages

The template uses these packages (automatically installed by MiKTeX):

```latex
\usepackage[margin=0mm]{geometry}    % Page layout
\usepackage{tikz}                     % Graphics and backgrounds
\usepackage{tcolorbox}                % Colored boxes
\usepackage{fontawesome5}             % Icons
\usepackage{pgfornament}              % Decorative elements
\usepackage{helvet}                   % Helvetica font
\usepackage{avant}                    % Avant Garde font
```

## 🎨 Customization

### Modify Company Information

Edit these commands in `flyer_template.tex`:

```latex
\newcommand{\CompanyMain}{Y2K Global OÜ}
\newcommand{\CompanyPartner}{KISS IT Solutions e.U.}
\newcommand{\Street}{Sebastian-Kneipp-Gasse 9/18}
\newcommand{\City}{1020 Wien}
\newcommand{\Mail}{office@y2k.global}
\newcommand{\Phone}{+43 1 442 20 143}
\newcommand{\Web}{www.y2k.global}
\newcommand{\LogoFile}{y2k-logo-schwarz 512.png}
```

### Change Colors

Modify the color definitions:

```latex
\definecolor{y2kblack}{RGB}{20,20,20}
\definecolor{y2kaccent}{RGB}{255,193,7}
\definecolor{y2kblue}{RGB}{41,128,185}
\definecolor{gradientstart}{RGB}{52,152,219}
\definecolor{gradientend}{RGB}{155,89,182}
```

### Adjust Pricing

Update pricing variables:

```latex
\newcommand{\Monthly}{49{,}90\,€}
\newcommand{\Yearly}{499\,€}
\newcommand{\Validity}{4 Wochen}
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "pdflatex not found" Error

**Solution:** Ensure LaTeX is installed and in PATH:

```bash
# Windows
where pdflatex

# macOS/Linux
which pdflatex
```

If not found, add to PATH or reinstall LaTeX distribution.

#### 2. Missing Packages Error

**MiKTeX (Windows):** Will auto-install packages on first run.

**Other Systems:** Install missing packages manually:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-fonts-extra texlive-latex-extra

# macOS (with MacTeX installed)
sudo tlmgr install packagename
```

#### 3. Font Not Found

Install required fonts:
```bash
# Install FontAwesome5 package
tlmgr install fontawesome5
```

#### 4. Logo File Not Found

Ensure logo file exists in the same directory as .tex file, or update path:
```latex
\newcommand{\LogoFile}{path/to/your/logo.png}
```

#### 5. PDF Created with Errors

Check the log file for details:
```bash
python latex_to_pdf.py flyer_template.tex --keep-aux
# Then examine flyer_template.log
```

### MiKTeX Specific Issues

#### Package Installation Prompts
MiKTeX may prompt for package installation on first run. To avoid this:

1. Open MiKTeX Console
2. Go to Settings
3. Set "Install missing packages" to "Always"

#### Update MiKTeX
```powershell
# Update MiKTeX packages
miktex update
```

## 🔍 Script Features

### Automatic Path Detection

The script automatically detects pdflatex location on Windows:
- User installation: `C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\`
- System installation: `C:\Program Files\MiKTeX\`
- Program Files (x86): `C:\Program Files (x86)\MiKTeX\`

### Error Handling

- Validates input file existence
- Checks file extension (.tex)
- Handles compilation errors gracefully
- Reports missing dependencies

### Cleanup

Automatically removes auxiliary files:
- `.aux` - Auxiliary information
- `.log` - Compilation log
- `.out` - Hyperref output
- `.toc` - Table of contents
- `.lof` - List of figures
- `.lot` - List of tables
- `.bbl` - Bibliography
- `.blg` - Bibliography log

## 📊 Performance

- **Compilation time:** 2-5 seconds for simple documents
- **Memory usage:** ~100MB for typical flyer
- **Output quality:** Professional print-ready PDF
- **File size:** ~200KB for two-page flyer with graphics

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## 📜 License

This project is proprietary to Y2K Global OÜ. All rights reserved.

## 📞 Support

For technical support or questions:
- Email: office@y2k.global
- Phone: +43 1 442 20 143
- Web: www.y2k.global

---

*Created with ❤️ by Y2K Global OÜ in cooperation with KISS IT Solutions e.U.*