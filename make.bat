@echo off
python make_properties.py
pyinstaller ^
  --onefile ^
  --clean ^
  --noupx ^
  --win-private-assemblies ^
  --icon=.\fcalc.ico ^
  --noconfirm ^
  --noconsole ^
  --version-file=properties.rc ^
  fcalc.py
pause
