@echo off
pyinstaller ^
  --onefile ^
  --clean ^
  --noupx ^
  --win-private-assemblies ^
  --icon .\fcalc.ico ^
  --noconfirm ^
  --noconsole ^
  fcalc.py
pause
