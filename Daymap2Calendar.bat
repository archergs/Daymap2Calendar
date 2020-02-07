@echo off
:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
:: Execute stuff...
echo Python is installed. Installing dependencies...
pip install -r requirements.txt
C:\Python3.8.1\python.exe script/daymap2calendar.py

:errorNoPython
echo Python not found. Python 3.8.1 will now be installed. This may take a moment...
curl https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe --output python3.exe
python3.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_test=0 TargetDir=C:\Python3.8.1
echo Python is now installed. Thanks for waiting!
pip install -r requirements.txt
C:\Python3.8.1\python.exe script/daymap2calendar.py