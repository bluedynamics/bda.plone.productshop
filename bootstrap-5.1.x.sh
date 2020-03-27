#!/bin/sh
rm -r ./lib ./include ./local ./bin
ln -fs plone-5.1.x.cfg buildout.cfg
python3 -mvenv .
./bin/pip -U pip
./bin/pip install -r requirements.cfg 
./bin/buildout

