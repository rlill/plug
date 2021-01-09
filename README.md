# plug
Raspberry Pi GPIO control with webservice

## Description
Minimal webservice that can be installed on a Raspberry Pi.
It allows the user to control certain output pins of the GPIO by clicking the corresponding button.
Permissions can be set so that only logged in users may switch an individual port on or off,
or the port can be 'public'.

Additionally every output pin can be toggled on and off also with a pushbutton connected to another
GPIO pin which is configured as the corresponding input.

## Run in development mode
To be allowed to use port 80 the program must be started as root
```
sudo python3 plug.py
```

## Run in production mode
Install gunicorn:
```
pip install gunicorn
```

To be allowed to use port 80 the program must be started as root
```
sudo gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload
```

run it in the background:
```
sudo nohup gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload  &
```

## Configuration
is in config.yaml
```
ports:
 - name: Light
   permission:
    - ALL
   gpio_actor: 10
   gpio_button: 2
 - name: Toaster
   permission:
    - charly
    - michelle
   gpio_actor: 11
   gpio_button: 3

users:
 - name: charly
   password: '81dc9bdb52d04dc20036dbd8313ed055'
```
Each port is one button (see screenshot below) and has a ```name```, a output pin ```gpio_actor```, optionally an input pin ```gpio_button```and a list of permitted users or ```ALL``` for buttons without access restriction.

Each user has a ```name```and a ```passowrd``` stored as hex-encoded MD5 hash.
You can encrypt it e. g. in Bash with
```
$ echo -n '1234' | md5sum
```

### Further reading
To create an device you may want to set up your Raspberry Pi with a read-only file-system to avoid damage if unplugged without shutdown.
* https://www.raspberry-pi-geek.de/ausgaben/rpg/2018/08/raspbian-im-read-only-modus/2/
* https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353

### Screenshot
![](https://github.com/rlill/plug/blob/main/static/screemshot.png?raw=true)
