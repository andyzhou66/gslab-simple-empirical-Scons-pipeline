"""
Build the paper PDF from LaTeX source using pdflatex.

This script is invoked from the SConscript action, which runs from the
project ROOT. The script changes to the step directory so that relative
\\input{} paths in the .tex file resolve correctly.

Multi-pass compilation (2 passes) is performed so that cross-references,
table of contents, and \\input{}ed content are fully resolved.

All output (stdout/stderr) is captured by the SConscript's shell redirection
into the step log: 4.build-paper-and-slides/temp/Sconscript_build_paper_and_slides.log
"""
import os
import subprocess
import sys


def main():
    # Paths relative to project ROOT (SCons action working directory)
    step_dir = '4.build-paper-and-slides'
    tex_source = 'code/paper.tex'       # step-relative
    output_dir = 'output'                # step-relative
    jobname = 'paper'                    # base name for .pdf, .aux, .log

    # Resolve absolute paths
    cwd = os.getcwd()
    step_dir_abs = os.path.join(cwd, step_dir)
    output_dir_abs = os.path.join(step_dir_abs, output_dir)

    # Ensure output directory exists
    os.makedirs(output_dir_abs, exist_ok=True)

    # pdflatex on Windows does not accept backslash paths.
    # Convert to forward slashes (safe on Linux too — no-op).
    output_dir_fwd = output_dir_abs.replace('\\', '/')

    print(f'Building paper from: {os.path.join(step_dir, tex_source)}')
    print(f'Output directory:    {os.path.join(step_dir, output_dir)}')
    print(f'Working directory:   {step_dir}')

    # Two-pass compilation:
    #   Pass 1: generates .aux file (cross-reference data) and .toc
    #   Pass 2: reads .aux from pass 1, resolves \\ref{}, \\tableofcontents
    for pass_num in (1, 2):
        print(f'\n=== pdflatex pass {pass_num} ===')

        result = subprocess.run(
            [
                'pdflatex',
                '-interaction', 'nonstopmode',
                '-output-directory', output_dir_fwd,
                '-jobname', jobname,
                tex_source,              # step-relative from step_dir cwd
            ],
            cwd=step_dir_abs,            # run from step dir so \\input resolves
            capture_output=True,
            text=True,
        )

        # Print pdflatex stdout to the log for diagnostics
        if result.stdout:
            print(result.stdout)

        if result.returncode != 0:
            print(f'ERROR: pdflatex pass {pass_num} failed '
                  f'with return code {result.returncode}')
            if result.stderr:
                print('STDERR:', result.stderr)
            sys.exit(result.returncode)

    output_pdf = os.path.join(step_dir, output_dir, f'{jobname}.pdf')
    print(f'\nPaper built successfully: {output_pdf}')


if __name__ == '__main__':
    main()
