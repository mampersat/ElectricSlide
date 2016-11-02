#Raspberry PI code

## Protocol
Card Reader speaks [Wiegand](https://en.wikipedia.org/wiki/Wiegand_interface):
> The Wiegand interface uses three wires, one of which is a common ground and two of which are data transmission wires usually called DATA0 and DATA1, alternately labeled "D0" and "D1" or "Data Low" and "Data High". When no data is being sent, both DATA0 and DATA1 are pulled up to the "high" voltage level — usually +5 VDC. When a 0 is sent the DATA0 wire is pulled to a low voltage while the DATA1 wire stays at a high voltage. When a 1 is sent the DATA1 wire is pulled to a low voltage while DATA0 stays at a high voltage.

## Hardware
[Pin out](http://www.manualguru.com/omnitek/omniprox-reader-op40/users-manual) for RFID reader. Unimportant pins crossed out. (Note: op40 puts out 5v and a Raspberry Pi's GPIO pins are only rated for 3v)

|Color|Wire|
|-----|----|
|Red|DC+Input|
|Black|Ground|
|White|Data 1|
|Green|Data 0|
|~~Brown~~|~~LED Control~~|
|~~Purple~~|~~Tamper~~|

Because the Raspberry Pi's GPIO pins are only 3.3v tolerant, you'll need to use a [voltage divider](https://learn.sparkfun.com/tutorials/voltage-dividers) to step down the 5v input to ~3.3v.

In testing, I used a 1.8k resistor for R1 and a 3.3k resistor for R2 which should give us a V<sub>out</sub> = 3.24V which is [close enough](https://www.scribd.com/doc/101830961/GPIO-Pads-Control2).

The following is an example of how I connected it all up:
![schematic](https://github.com/mampersat/ElectricSlide/raw/master/pi/schematic.png "Schematic")

## Library
RaspberryPI library [pigpio](http://abyz.co.uk/rpi/pigpio/examples.html#Python_wiegand_py) can read wiegand. You'll need to install a [daemon](http://abyz.co.uk/rpi/pigpio/download.html) to get the python code to work.

The apt-get install is the easiest method:

```bash
$ sudo apt-get update
$ sudo apt-get install pigpio python-pigpio python3-pigpio

$ sudo service pigpiod start
```

