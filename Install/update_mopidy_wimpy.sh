#!/bin/bash
cd /usr/src/mopidy_wimpy
git config --global http.sslverify false
git pull
git config --global http.sslverify true
python setup.py install
cp mopidy_wimpy/ext.conf /usr/local/lib/python2.7/dist-packages/Mopidy_Wimpy-0.2.0-py2.7.egg/mopidy_wimpy/
/etc/init.d/mopidy restart
