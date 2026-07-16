@echo off
REM Activate the virtual environment and run SCons builds

cd /d "%~dp0"

REM Activate the venv
call ..\Scripts\activate.bat

REM Show activated status
echo.
echo Virtual Environment Activated!
echo.
echo You can now run:
echo   - python run.py                      (build all modified files)
echo   - python run.py build/path/to/dir   (build specific directory)
echo   - python run.py build/path/to/file  (build specific file)
echo.
echo Navigate to 'analysis' or 'paper_slides' subdirectory first:
echo   cd analysis
echo   python run.py
echo.

cmd /k
