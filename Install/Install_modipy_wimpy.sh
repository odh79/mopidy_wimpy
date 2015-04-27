#!/bin/bash
apt-get -y install git python-pip
pip install requests 
#pip install setuptools==14.3.1
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
cd /usr/src
git clone https://github.com/tamland/wimpy.git
cd wimpy
python setup.py install
cd ..
git config --global http.sslverify false
git clone https://github.com/odh79/mopidy_wimpy.git
git config --global http.sslverify true
cd mopidy_wimpy
python setup.py install
cp mopidy_wimpy/ext.conf /usr/local/lib/python2.7/dist-packages/Mopidy_Wimpy-0.2.0-py2.7.egg/mopidy_wimpy/ext.conf
cp /etc/mopidy/mopidy.conf /etc/mopidy/mopidy.conf.old
echo "# ----------" >> /etc/mopidy/mopidy.conf
echo "# | Wimpy  |" >> /etc/mopidy/mopidy.conf  
echo "# ----------" >> /etc/mopidy/mopidy.conf
echo "[wimpy]" >> /etc/mopidy/mopidy.conf
echo "enabled = true" >> /etc/mopidy/mopidy.conf
echo "username =" >> /etc/mopidy/mopidy.conf
echo "password =" >> /etc/mopidy/mopidy.conf

echo "\n\n\nEdit your username and password for wimp"
echo "Press enter to continue"
read hello
nano /etc/mopidy/mopidy.conf
echo "If there is a problem with playing tracks, try to edit"
echo "/usr/src/wimpy/wimpy/wimpy.py and change"
echo "class Config(object):"
echo "    api = WIMP_API"
echo "\n to "
echo "class Config(object):"
echo "    api = TIDAL_API"
echo "\n and then do\n cd /usr/src/wimpy\n python setup.py install"

/etc/init.d/mopidy restart


