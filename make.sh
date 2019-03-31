#/bin/sh

pyinstaller \
  --onefile \
  --clean \
  --noupx \
  --icon .\fcalc.ico \
  --noconfirm \
  --noconsole \
  fcalc.py
