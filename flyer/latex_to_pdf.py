#!/usr/bin/env python3
"""
LaTeX to PDF Converter
Converts .tex files to PDF using pdflatex
"""

import subprocess
import os
import sys
import argparse
from pathlib import Path
import shutil


def check_pdflatex():
    """Check if pdflatex is installed and available"""
    pdflatex_path = shutil.which('pdflatex')

    if pdflatex_path is None:
        # Check common MiKTeX installation paths on Windows
        if sys.platform == 'win32':
            import getpass
            username = getpass.getuser()
            potential_paths = [
                f"C:\\Users\\{username}\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe",
                "C:\\Program Files\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe",
                "C:\\Program Files (x86)\\MiKTeX\\miktex\\bin\\pdflatex.exe"
            ]

            for path in potential_paths:
                if Path(path).exists():
                    print(f"Found pdflatex at: {path}")
                    return path

        print("Error: pdflatex not found. Please install a LaTeX distribution:")
        print("  - Windows: Install MiKTeX or TeX Live")
        print("  - macOS: Install MacTeX")
        print("  - Linux: Install texlive (sudo apt-get install texlive-full)")
        return False

    return pdflatex_path


def compile_latex(tex_file, output_dir=None, runs=2, pdflatex_cmd=None):
    """
    Compile a LaTeX file to PDF

    Args:
        tex_file: Path to the .tex file
        output_dir: Output directory (default: same as input file)
        runs: Number of compilation runs (default: 2, for references/TOC)
        pdflatex_cmd: Path to pdflatex command (optional)

    Returns:
        True if successful, False otherwise
    """
    tex_path = Path(tex_file).resolve()

    if not tex_path.exists():
        print(f"Error: File '{tex_file}' not found")
        return False

    if tex_path.suffix != '.tex':
        print(f"Error: File '{tex_file}' is not a .tex file")
        return False

    # Use provided pdflatex command or default
    if pdflatex_cmd is None:
        pdflatex_cmd = 'pdflatex'

    # Set output directory
    if output_dir:
        out_dir = Path(output_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = tex_path.parent

    # Base name without extension
    base_name = tex_path.stem

    print(f"Compiling: {tex_path}")
    print(f"Output directory: {out_dir}")

    # Run pdflatex multiple times for references
    for run in range(runs):
        print(f"Compilation run {run + 1}/{runs}...")

        try:
            # Run pdflatex with output directory
            result = subprocess.run(
                [
                    pdflatex_cmd,
                    '-interaction=nonstopmode',  # Don't stop on errors
                    f'-output-directory={out_dir}',
                    str(tex_path)
                ],
                capture_output=True,
                text=True,
                cwd=tex_path.parent  # Run in the directory of the tex file
            )

            if result.returncode != 0:
                print(f"Warning: pdflatex returned non-zero exit code: {result.returncode}")
                print("Error output:")
                print(result.stderr)
                # Check if PDF was still created
                pdf_path = out_dir / f"{base_name}.pdf"
                if not pdf_path.exists():
                    print(f"Error: PDF file was not created")
                    return False
                else:
                    print(f"PDF was created despite errors: {pdf_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error running pdflatex: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    # Check if PDF was created
    pdf_path = out_dir / f"{base_name}.pdf"
    if pdf_path.exists():
        print(f"Success! PDF created: {pdf_path}")

        # Clean up auxiliary files
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot', '.bbl', '.blg']
        for ext in aux_extensions:
            aux_file = out_dir / f"{base_name}{ext}"
            if aux_file.exists():
                aux_file.unlink()
                print(f"Cleaned up: {aux_file.name}")

        return True
    else:
        print(f"Error: PDF file was not created at {pdf_path}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert LaTeX files to PDF',
        epilog='Example: python latex_to_pdf.py document.tex'
    )
    parser.add_argument(
        'tex_file',
        help='Path to the .tex file to compile'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory for the PDF (default: same as input file)'
    )
    parser.add_argument(
        '-r', '--runs',
        type=int,
        default=2,
        help='Number of compilation runs (default: 2)'
    )
    parser.add_argument(
        '--keep-aux',
        action='store_true',
        help='Keep auxiliary files (.aux, .log, etc.)'
    )

    args = parser.parse_args()

    # Check if pdflatex is available
    pdflatex_path = check_pdflatex()
    if not pdflatex_path:
        sys.exit(1)

    # Compile the LaTeX file
    success = compile_latex(args.tex_file, args.output_dir, args.runs, pdflatex_path)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print("LaTeX to PDF Converter")
        print("Usage: python latex_to_pdf.py <tex_file>")
        print("       python latex_to_pdf.py -h for help")
        sys.exit(1)

    main()