#!/bin/bash

rm test.py
cd core
mv settings.py basesettings.py
mv cloudsettings_dev.py settings.py
cd ../../
git add .
git commit -m "Done"
git push --set-upstream origin version_1.1


cd src/core/
mv settings.py cloudsettings_dev.py
mv basesettings.py settings.py
cd ..
clear