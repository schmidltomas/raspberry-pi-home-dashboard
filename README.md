# raspberry-pi-home-dashboard
Simple customized home dashboard for Raspberry Pi.

Work in progress...

(Planned) features:
* Clock ✓
* Personalised greeting ✓
* Indoor temperature, air pressure and humidity (use sensor)
* Weather forecast (use some web service) ✓
* RSS news feed ✓
* Current time to work (use some routing API)
* Automatic display switch off (use motion sensor)

# Attributions
Wallpapers are from interfacelift.com, which is sadly no longer running.

Weather data and weather icons by [The Norwegian Meteorological Institute](https://www.met.no/en), under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0/) and [Creative Commons 4.0 BY International](https://creativecommons.org/licenses/by/4.0/) licences.

OpenSans font by Steve Matteson at [Google Fonts](https://fonts.google.com/), licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).  

# Dependencies
* Kivy (https://kivy.org/#home)
* feedparser (https://pythonhosted.org/feedparser/)

# Install Kivy on Ubuntu
1. sudo apt-get install libsdl2-image-dev
2. sudo add-apt-repository ppa:kivy-team/kivy
3. sudo apt-get install python3-kivy
