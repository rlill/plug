# plug
Raspberry Pi GPIO control with webservice

Minimal webservice that can be installed on a Raspberry Pi.
It allows the user to control certain output pins of the GPIO by clicking the corresponding button.
Permissions can be set so that only logged in users may switch an individual port on or off,
or the port can be 'public'.

## Run in development mode
To be allowed to use port 80 the program must be started as root
> sudo python3 plug.py

## Run in production mode
Install gunicorn:
> pip install gunicorn

To be allowed to use port 80 the program must be started as root
> sudo gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload  

run it in the background:
> sudo nohup gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload  &

### Further reading
To create an device you may want to set up your Raspberry Pi with a read-only file-system to avoid damage if unplugged without shutdown.
* https://www.raspberry-pi-geek.de/ausgaben/rpg/2018/08/raspbian-im-read-only-modus/2/
* https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353

### Screenshot
![Screenshot](static/screenshot.png)
