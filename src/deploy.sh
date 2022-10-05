#!/bin/bash

echo "Enter a commit for the push: "
read COMMIT

cd core
mv settings.py basesettings.py
mv cloudsettings.py settings.py

cd ../../
git add .
git commit -m "$COMMIT"
git push --set-upstream origin main

cd src/core/
mv settings.py cloudsettings.py
mv basesettings.py settings.py
cd ..
clear