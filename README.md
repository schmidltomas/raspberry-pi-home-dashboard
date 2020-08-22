# raspberry-pi-home-dashboard
Simple customized home dashboard for Raspberry Pi.

Work in progress...

(Planned) features:
* Clock ✓
* Personalised greeting ✓
* Indoor temperature, air pressure and humidity (use sensor)
* Weather forecast (use some web service) ✓
* RSS news feed ✓
* Current time to work (use some routing API) ✓
* Automatic display switch off (use motion sensor)

# Attributions
Wallpapers are from interfacelift.com, which is sadly no longer running.

Weather data and weather icons by [The Norwegian Meteorological Institute](https://www.met.no/en), under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0/) and [Creative Commons 4.0 BY International](https://creativecommons.org/licenses/by/4.0/) licences.

OpenSans font by Steve Matteson at [Google Fonts](https://fonts.google.com/), licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).  

# Dependencies
* Kivy (https://kivy.org/#home)
* Python Client for Google Maps Services (https://github.com/googlemaps/google-maps-services-python)
    * requires Google Cloud API key
* feedparser (https://pypi.org/project/feedparser/)
* python-dateutil (https://pypi.org/project/python-dateutil/)

# Install Kivy on Ubuntu
1. `sudo apt-get install libsdl2-image-dev`
2. `sudo add-apt-repository ppa:kivy-team/kivy`
3. `sudo apt-get install python3-kivy`

# Install Kivy on Raspbian
1. `sudo apt update`
2. `sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev`
3. `python3 -m pip install --upgrade --user pip setuptools`
4. `python3 -m pip install --upgrade --user Cython==0.29.10 pillow`
5. `python3 -m pip install --user kivy`

# Troubleshooting
* If you get `RssServiceException` with `SSL: DH_KEY_TOO_SMALL` message on Raspbian, comment this line in `/etc/ssl/openssl.cnf`:
```CipherString = DEFAULT@SECLEVEL=2```
* To find out supported locales on Ubuntu/Raspbian, use `locale -a`

