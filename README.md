# plug
Raspberry Pi GPIO control with webservice



sudo python3 plug.py 


pip install gunicorn

sudo gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload  

sudo nohup gunicorn -w 4 -b 0.0.0.0:80 plug:app --preload  &


https://www.raspberry-pi-geek.de/ausgaben/rpg/2018/08/raspbian-im-read-only-modus/2/

https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353



