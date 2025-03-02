@echo off
REM Activate the virtual environment
call C:\Users\abbe1\Python Automation\.venv\Scripts\Activate.bat >nul 2>&1

REM Run the Python script with two arguments
python "C:\Users\abbe1\Python Automation\src\reservip.py" %1 %2


