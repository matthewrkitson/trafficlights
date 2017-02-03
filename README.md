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
    SSID="<your network SSID>"
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
 * Under "Advanced Options"
    * Change the hostname (I chose "trafficlights")
    * Turn off the serial port (with my GPIO pinout it resulted in the LEDs flickering as the system started, which in turn seemed to cause power problems that stopped the system booting properly (but I'd also got a broken earth connection that I only discovered later, so that might have been the cause of those problems))
* Install the software we need
  * `sudo apt-get update`
  * `sudo apt-get install python3-flask`
  * `sudo apt-get install python3-rpi.gpio`
  * `sudo apt-get install git`
