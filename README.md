# Night Vision Goggles
Open source night vision goggles that use old Gear VR headsets as a base. 

## Parts Required / Assembling
- <a href="https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/" target="_blank">1x Raspberry Pi 3 A+</a>
- <a href="https://www.waveshare.com/rpi-ir-cut-camera.htm" target="_blank">1x Rpi IR-CUT Camera</a>
- <a href="https://www.waveshare.com/img/devkit/accBoard/Infrared-LED-Board-B/Infrared-LED-Board-B-5.jpg" target="_blank">6x Waveshare IR Led Board</a>
- Samsung Gear VR Headset (You can use any cardboard style headset, but you'll need to modify the 3d files accordingly)
- Powerbank (it should have 2 usb outputs, one should be at least 2A to power the RPI)
- Usb cables, a button switch for function control and RPI shutdown
There are no full instructions yet, but I have added some photos in the /pictures folder to help you assemble the goggles. I also build on my YouTube channel, it is not an instruction video but it might help: https://www.youtube.com/watch?v=c6y9qKiKzgg

## Installation
Copy the nightvision.py to your /pi folder and Run:
``` bash
$ python3 nightvision.py
```
To get it to start when the goggles are booted, follow this guide to add the nightvision.py to LXDE autostart: https://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/

Note: The script is using MMAL to create multiple images of the camera feed, which is the library for the raspicam. Therefore the script is only tested on Raspberry OS Buster and not Bullseye. 

