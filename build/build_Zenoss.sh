#!/bin/bash
cd ../src
python2 --version
python2 setup.py bdist_egg
cd dist
zip -r "xFusion zenoss Plugin v2.0.18.zip" *