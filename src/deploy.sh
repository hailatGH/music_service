#!/bin/bash

rm test.py
cd core
mv settings.py basesettings.py
mv cloudsettings.py settings.py
cd ../../
git add .
<<<<<<< HEAD
git commit -m "done"
git push --set-upstream origin version_1.1
=======
git commit -m "Done"
git push
>>>>>>> main

cd src/core/
mv settings.py cloudsettings.py
mv basesettings.py settings.py
cd ..
clear