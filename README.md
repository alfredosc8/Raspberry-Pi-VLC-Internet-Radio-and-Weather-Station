RPI Weather radio, based on https://github.com/rotti/Rottis-RPi-Tron-Radio-Clone-
Project run by Franco and Luca
---------------------------------------------------------------------------------
Differently from all available RbPi radio I found so far, this one uses VLC, which, 
even though it uses more resources, it is a much more powerful player compared to mpc/mpd.

For me, I have a 7% CPU usage, after hours of radio streaming, which I find acceptable.

I used a 3.5" touch screen from Kuman, so, if you go with different dimensions, fix the 
screen variables in Radio_Weather.py

To make it run, you'll need:
1. Install VLC (apt....)
2. Install pyowm (https://github.com/csparpa/pyowm)
3. Make VLC autostart (https://www.raspberrypi.org/forums/viewtopic.php?t=17051&p=170858)
4. I add a copy om my /etc/rc.local file, since I do some stuff in there too. My Radio is 
   setup to use blueetooh streaming, so I do auto pairing in here too. You can use it as reference
5. Check Radio_Weather.py, to set your own city and openweathermap.org key
6. Put your openweathermap.ork key in the key file provided
7. Put your radio logos/icons in the radio_icons folder (use png files, best 100px by 100px)
7. Modify the radio_list.txt file with your radio station and your radio icons file name

Some of the icons are not used (Like favorites...) I will be working to make them do other 
stuff (open a nas folder, or read mp3 from a USB)

Have fun

