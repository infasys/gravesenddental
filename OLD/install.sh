#!/bin/bash
python3 -m PyInstaller --onefile --windowed tahidtest.py --add-data ./tahidtest.ui:.
cp tahidtest.ui /var/specs/dist/.
cp bells.png /var/specs/dist/.
cp ./dist/tahidtest /var/specs/dist/.