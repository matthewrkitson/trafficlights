# traffic-lights
Raspberry Pi project to control LED traffic lights

# Overview

* Raspberry Pi Zero 
 * With WiFi dongle
 * Connected to red and green LEDs through GPIO
 * Running lighttpd offering Web API to control LEDs 

# Raspberry Pi setup
* Download latest image and write to SD card
```
  sudo su
  apt-get install funzip
  
  # Insert SD card
  dmesg 
  # Look at output to work out what device the SD card was recognised as
  
  # Download the latest raspbian image and unzip direct to the sd card 
  # (replace /dev/sdc with the appropriate device)
  wget -O - https://downloads.raspberrypi.org/raspbian_latest | funzip > /dev/sdc
```
* Add an empty file called `ssh` to the boot partition
* Add a file called `wpa_supplicant.conf` to the boot partition, and fill with your WiFi settings
```
network={
    ssid="<your network SSID>"
    psk="<your network password>"
    key_mgmt=WPA-PSK
}
```
* Turn the Raspberry Pi on
* By default, it will appear on the network as "raspberrypi"
* Log in using the standard Raspbian username and password
* Run raspi-config
 * Resize the filesystem
 * Change the default password
 * Change the hostname (I chose "trafficlights")
 * Under "Interfacing Options"
    * Turn off the serial port (with my GPIO pinout it resulted in the LEDs flickering as the system started, which in turn seemed to cause power problems that stopped the system booting properly (but I'd also got a broken earth connection that I only discovered later, so that might have been the cause of those problems))
  * (Optional) Turn on VNC for a remote connection
    * Under "Interfacing options", turn on VNC
    * Inder "Advanced options" choose a reasonable screen resolution (important if you have no monitor plugged in to your pi)
    * Now you can use VNC Viewer to connect to the Pi to control it. 
* Install the software we need
  * `sudo apt-get update`
  * `sudo apt-get install python3-flask`
  * `sudo apt-get install python3-rpi.gpio`
  * `sudo apt-get install lighttpd`
  * `sudo apt-get install git`
  * Install flup - I think I did `sudo pip3 install flup-py3`, but you may need to Google this...
* Allow the lighttpd web server to control GPIO and turn the Pi off
  * `sudo usermod -a -G gpio www-data`
  * Use `sudo visudo` to add the line `www-data ALL=NOPASSWD: /sbin/poweroff` to /etc/sudoers
* Clone this repository into the `pi` user's home area
  * `git clone https://github.com/matthewrkitson/trafficlights.git`
* Update the lighttpd configuration to enable fast-cgi and point to the traffic lights web app
  * `sudo service lighttpd start`
  * Browse to http://trafficlights/ and check that the welcome page is there. If it's not, you need to fix lighttpd. 
  * `sudo lighty-enable-mod fast-cgi`
  * Edit `/etc/lighttpd/lighttpd.conf` adding the following lines
```
fastcgi.server = ("/trafficlights" =>
   ((
      "socket" => "/tmp/trafficlights-fcgi.sock",
      "bin-path" => "/home/pi/trafficlights/website/host-trafficlights.fcgi",
      "check-local" => "disable",
      "max-procs" => 1
   ))
)
```
  * `sudo service lighttpd restart` (or `sudo service lighttpd force-reload`, but this didn't always seem to work for me)
  * Browse to http://trafficlights/trafficlights/ to see the trafficlights control page. 
