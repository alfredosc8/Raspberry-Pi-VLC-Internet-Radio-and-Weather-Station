#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPi-Tron-Radio Clone ... added some more features (weather, confirmation, ...)
BIG THANKS TO:
Raspberry Pi Web-Radio with 2.8' TFT Touchscreen and Tron-styled graphical interface
GitHub: http://github.com/5volt-junkie/RPi-Tron-Radio
Blog: http://5volt-junkie.net
MIT License: see license.txt
--------------------------------------------------
March 30th 2017 Based on the above, Franco and I developed this little radio with weather forecast. 
Loads of the hard work was done on the original Tron Radio, that made verything easier!
"""

#you need to install pyowm on your RbPi. Here's the link and some instructions: https://github.com/csparpa/pyowm
import datetime
import os
import subprocess
import sys
import time
import requests
import pygame
import pyowm
from pygame.locals import *
from libvlc import VLC

pygame.init()


# User settings
PLAYLIST = 'radio_list.txt' #you can create your own playlist, just follow the design of this file
LOCATION = 'Durlach,DE' #on openweatermap.org you can  find all avaiable cities and city id (requested on the next line)
CITY_ID = '2934469'

# Openweather key - register for free at openweathermap.org - YOU NEED YOUR OWN KEY
KEY = '94b5263ca1ed425199214db97b47b4fa'

# Constants definitions
# Screen size 
WIDTH = 480
HEIGHT = 320
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 32)

# Skins - many more skins are available, I decided to go with a single color one, I am not that fashionable
SKIN1 = pygame.image.load('skins/skin_tron_m1.png')
SKIN2 = pygame.image.load('skins/skin_tron_m3.png')
SKIN3 = pygame.image.load('skins/skin_tron_m2.png')
SKINS = (SKIN1, SKIN2, SKIN3)

# Fonts - if you wish to have different fonts, just place them in the fonts folder, and use the below scheme to set up yours
FONT1 = pygame.font.Font(None, 25)
FONT2 = pygame.font.Font(None, 28)
FONT3 = pygame.font.Font('fonts/BAUHS93.TTF', 43)
FONT4 = pygame.font.Font('fonts/ARIALN.TTF', 25)
FONT5 = pygame.font.Font('fonts/ARIALN.TTF', 20)
FONT_COLOR = (50, 255, 255)

"""Colors references""" #not use for my radio, but who knows what you want to do
#             R    G    B
# white   = (255, 255, 255)
# red     = (255,   0,   0)
# green   = (  0, 255,   0)
# blue    = (  0,   0, 255)
# black   = (  0,   0,   0)
# cyan    = ( 50, 255, 255)
# magenta = (255,   0, 255)
# yellow  = (255, 255,   0)
# orange  = (255, 127,   0)

# Other declarations needed for the touchscreen
os.environ['SDL_FBDEV'] = '/dev/fb1'
os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
os.environ['SDL_MOUSEDRV'] = 'TSLIB'
#this is needed to display the weatehr forecast
WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

# Disable mouse cursor - I couldn't find a way to disable it, so I made it invisible :)
pygame.mouse.set_cursor(
    (8, 8),
    (0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0))

#all sort of definitions
def poweroff():
    """Power off system"""
    poweroff_label = FONT1.render('Shutting down', 1, (FONT_COLOR))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(poweroff_label, (10, 100))
    pygame.display.flip()
    time.sleep(5)
    subprocess.call('vlc.stop()', shell=True)
    subprocess.call('poweroff', shell=True)


def reboot():
    """Reboot system"""
    reboot_label = FONT1.render('Rebooting...', 1, (FONT_COLOR))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(reboot_label, (10, 100))
    pygame.display.flip()
    time.sleep(5)
    subprocess.call('vlc.stop()', shell=True)
    subprocess.call('reboot', shell=True)


def quit_radio():
    """Close radio"""
    subprocess.call('vlc.stop()', shell=True)
    pygame.quit()
    sys.exit()


def get_weather():
    """Get current weather"""
    global w
    obs = owm.weather_at_place(LOCATION)
    w = obs.get_weather()


def get_forecast():
    """Get weather forecast"""
    global f
    fc = owm.daily_forecast(LOCATION)
    f = fc.get_forecast()


def weekday(d):
    """Return name of the day"""
    if d > 6:
        d -= 7
    return WEEKDAYS[d]


def on_touch(x, y):
    """Get touchscreen events coordinates"""
    if  18 <= x <= 115 and 161 <= y <= 231:
        button(1)
    if  133 <= x <= 228 and 161 <= y <= 231:
        button(2)
    if  251 <= x <= 344 and 161 <= y <= 231:
        button(3)
    if  365 <= x <= 459 and 161 <= y <= 231:
        button(4)
    if  18 <= x <= 115 and 240 <= y <= 311:
        button(5)
    if  133 <= x <= 228 and 240 <= y <= 311:
        button(6)
    if  251 <= x <= 344 and 240 <= y <= 311:
        button(7)
    if  365 <= x <= 459 and 240 <= y <= 311:
        button(8)


def button(number):
    """Buttons event handlers"""
    global menu, status
    if number == 1:
        if menu == 1:
            vlc.play()

    if number == 2:
        if menu == 1:
            vlc.pause()

    if number == 3:
        if menu == 1:
            vlc.volup()
        if menu == 3:
            pygame.quit()
            sys.exit()

    if number == 4:
        if menu == 1:
            vlc.volume(0)
        if menu == 2:
            update_screen()
        if menu == 3:
            vlc.stop()
            pygame.quit()
            sys.exit()

    if number == 5:
        if menu == 1:
            vlc.prev()
        if menu == 3:
            poweroff()

    if number == 6:
        if menu == 1:
            vlc.next()
        if menu == 3:
            reboot()

    if number == 7:
        if menu == 1:
            vlc.voldown()

    if number == 8:
        menu += 1
        if menu > len(SKINS):
            menu = 1
        create_all_labels()
        update_screen()


def create_radio_label():
    """Generate main title"""
    global radio_label
    radio_label = FONT3.render('INTERNET RADIO', 1, (FONT_COLOR))


def create_station_label():
    """Generate station name label amd radio logo item""" #all logos are 100px width. You can adapt your logos
    global station_label, radio_logo
    station = vlc.get_title()
    if station != '':
        for line in playlist:
            line = line.split(';')
            if line[0] in station:
                if line[1]:
                    station = line[1]
                if line[2] and len(line[2]) > 4:
                    radio_icon = line[2]
                    radio_logo = pygame.image.load('radio_icons/' + radio_icon)
                else:
                    radio_logo = False
        if radio_logo and len(station) > 16:
            station = station[:13] + '...'
        elif len(station) > 24:
            station = station[:21] + '...'
        station_label = FONT4.render('Station: ' + station, 1, (FONT_COLOR))


def create_volume_label():
    """Generate current audio volume label"""
    global volume_label
    volume_label = FONT4.render('Volume: ' + vlc.get_volume(), 1, (FONT_COLOR))


def create_time_label():
    """Generate current date/time label"""
    global time_label
    current_time = datetime.datetime.now().strftime('%H:%M  %d.%m.%Y')
    time_label = FONT4.render(current_time, 1, (FONT_COLOR))


def create_temperature_label():
    """Generate current temperature label"""
    global temperature_label
    get_weather()
    temperature = w.get_temperature(unit='celsius')
    temp = round(temperature['temp'], 1)
    temperature_label = FONT4.render(str(temp) + u'ºC', 1, (FONT_COLOR))


def create_weather_icon():
    """Generate current weather icon item"""
    global weather_icon
    get_weather()
    icons = w.get_weather_icon_name()
    weather_icon = pygame.image.load('weather_icons/' + icons + '.png')


def create_location_label():
    """Generate location label"""
    global location_label
    city = LOCATION.split(',')
    location_label = FONT4.render('Weather in ' + city[0], 1, (FONT_COLOR))


def create_forecast_label():
    """Generate forecast title label"""
    global forecast_label
    forecast_label = FONT4.render('3 days Forecast', 1, (FONT_COLOR))


def create_days_labels():
    """Generate days name labels"""
    global day1_label, day2_label, day3_label
    day1 = weekday(datetime.datetime.today().weekday() + 1)
    day2 = weekday(datetime.datetime.today().weekday() + 2)
    day3 = weekday(datetime.datetime.today().weekday() + 3)
    day1_label = FONT4.render(day1, 1, (FONT_COLOR))
    day2_label = FONT4.render(day2, 1, (FONT_COLOR))
    day3_label = FONT4.render(day3, 1, (FONT_COLOR))


def create_forecast_icons():
    """Generate forecast icons items"""
    global forecast_icon1, forecast_icon2, forecast_icon3
    get_forecast()
    icons = [weather.get_weather_icon_name() for weather in f]
    path = ('weather_icons/')
    forecast_icon1 = pygame.image.load(path + str(icons[1]) + '.png')
    forecast_icon2 = pygame.image.load(path + str(icons[2]) + '.png')
    forecast_icon3 = pygame.image.load(path + str(icons[3]) + '.png')


def create_forecast_temperatures():
    """"Generate forecast temperatures labels"""
    global temp1_label, temp2_label, temp3_label
    request = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast/daily?id='
        + CITY_ID
        + '&units=metric&appid='
        + KEY)
    temps = request.json()
    temp1 = round(temps['list'][1]['temp']['day'], 1)
    temp2 = round(temps['list'][2]['temp']['day'], 1)
    temp3 = round(temps['list'][3]['temp']['day'], 1)
    temp1_label = FONT4.render(str(temp1), 1, (FONT_COLOR))
    temp2_label = FONT4.render(str(temp2), 1, (FONT_COLOR))
    temp3_label = FONT4.render(str(temp3), 1, (FONT_COLOR))


def create_weather_label():
    """Generate current weather label"""
    global weather_label
    get_weather()
    status = w.get_detailed_status()
    weather_label = FONT4.render(status, 1, (FONT_COLOR))


def create_wind_label():
    """Generate current wind speed label"""
    global wind_label
    get_weather()
    wind = w.get_wind()
    wind = round(wind['speed'], 1)
    wind_label = FONT4.render('Wind = ' + str(wind) + 'm/s', 1, (FONT_COLOR))


def create_pressure_label():
    """Generate current pressure label"""
    global pressure_label
    get_weather()
    pressure = w.get_pressure()
    pressure = pressure['press']
    pressure_label = FONT4.render('Pressure = ' + str(pressure) + 'hpa', 1, (FONT_COLOR))


def create_ip_label():
    """Generate current IP label"""
    global ip_label
    ip = subprocess.check_output('hostname -I', shell=True).strip()
    ip_label = FONT5.render('IP: ' + ip[:15], 1, (FONT_COLOR))


def create_cputemp_label():
    """Generate current CPU temperature label"""
    global cputemp_label
    cpu_temp = subprocess.check_output('/opt/vc/bin/vcgencmd measure_temp', shell=True).strip()
    cputemp_label = FONT5.render('CPU' + cpu_temp, 1, (FONT_COLOR))


def create_ram_label():
    """Generate used RAM label"""
    global ram_label
    ram = subprocess.check_output('/usr/bin/free -h | /bin/grep Mem', shell=True).split()
    ram = ram[0], '/'.join(ram[2:4])
    ram = str(ram)
    chars_to_remove = ['\'', '(', ')', ',']
    ram = ram.translate(None, ''.join(chars_to_remove))
    ram_label = FONT5.render(ram, 1, (FONT_COLOR))


def create_procs_label():
    """Generate running processes label"""
    global procs_label
    procs = subprocess.check_output('/bin/ps -e | /usr/bin/wc -l', shell=True).split()
    procs_label = FONT5.render('Procs: ' + procs[0], 1, (FONT_COLOR))


def create_cpuusage_label():
    """Generate current CPU usage label"""
    global cpuusage_label
    cpu = subprocess.check_output('/usr/bin/vmstat', shell=True).split()
    cpu = str(100 - int(cpu[37]))
    cpuusage_label = FONT5.render('CPU usage: ' + cpu + '%', 1, (FONT_COLOR))


def create_diskfree_label():
    """Generate free disk space label"""
    global diskfree_label
    df = subprocess.check_output('/bin/df -h .', shell=True).split()
    diskfree_label = FONT5.render('Disk: ' + df[11], 1, (FONT_COLOR))


def create_all_labels():
    """Generate all graphical items"""
    if menu == 1:
        create_radio_label()
        create_station_label()
        create_volume_label()
        create_time_label()
        create_temperature_label()
        create_weather_icon()
    elif menu == 2:
        create_location_label()
        create_forecast_label()
        create_days_labels()
        create_forecast_icons()
        create_forecast_temperatures()
        create_weather_label()
        create_temperature_label()
        create_wind_label()
        create_pressure_label()
    elif menu == 3:
        create_ip_label()
        create_cputemp_label()
        create_ram_label()
        create_time_label()
        create_procs_label()
        create_cpuusage_label()
        create_diskfree_label()

#here is where all labels, icons and logos are placed depending on which menu you are looking at
def update_screen():
    """Draw all screen items"""
    SCREEN.blit(SKINS[menu - 1], (0, 0))
    if menu == 1:
        SCREEN.blit(radio_label, (80, 10))
        SCREEN.blit(station_label, (35, 60))
        SCREEN.blit(volume_label, (35, 90))
        SCREEN.blit(time_label, (35, 120))
        SCREEN.blit(temperature_label, (380, 58))
        SCREEN.blit(weather_icon, (370, 70))
        if radio_logo:
            SCREEN.blit(radio_logo, (270, 60))
    elif menu == 2:
        SCREEN.blit(location_label, (35, 180))
        SCREEN.blit(forecast_label, (35, 18))
        SCREEN.blit(day1_label, (60, 50))
        SCREEN.blit(day2_label, (220, 50))
        SCREEN.blit(day3_label, (380, 50))
        SCREEN.blit(forecast_icon1, (38, 61))
        SCREEN.blit(forecast_icon2, (198, 61))
        SCREEN.blit(forecast_icon3, (358, 61))
        SCREEN.blit(temp1_label, (60, 120))
        SCREEN.blit(temp2_label, (220, 120))
        SCREEN.blit(temp3_label, (380, 120))
        SCREEN.blit(weather_label, (120, 215))
        SCREEN.blit(temperature_label, (35, 215))
        SCREEN.blit(wind_label, (35, 240))
        SCREEN.blit(pressure_label, (35, 265))
    elif menu == 3:
        SCREEN.blit(ip_label, (32, 15))
        SCREEN.blit(cputemp_label, (32, 40))
        SCREEN.blit(ram_label, (32, 65))
        SCREEN.blit(time_label, (32, 110))
        SCREEN.blit(procs_label, (200, 15))
        SCREEN.blit(cpuusage_label, (200, 40))
        SCREEN.blit(diskfree_label, (200, 65))

    pygame.display.flip()


# Initialize objects
pygame.time.set_timer(USEREVENT +1, 1000)
vlc = VLC()

playlist = open(PLAYLIST, 'r')
playlist = playlist.readlines()
for line in playlist:
    line = line.split(';')
    vlc.enqueue(line[0])
vlc.play()

owm = pyowm.OWM(KEY)

# Draw menu and start event monitor
seconds = 0
menu = 1
station_label = FONT4.render('Station: no data', 1, (FONT_COLOR))
radio_logo = False
create_all_labels()
update_screen()
running = True

while running:
    for event in pygame.event.get():
        if event.type == USEREVENT +1:
            seconds += 1
            if menu == 1:
                create_station_label()
                create_volume_label()
                create_time_label()
                if seconds == 1800:
                    seconds = 0
                    create_temperature_label()
                    create_weather_icon()
            elif menu == 2:
                if seconds == 600:
                    seconds = 0
                    create_all_labels()
            elif menu == 3:
                if seconds == 5:
                    seconds = 0
                    create_all_labels()
            update_screen()

        if event.type == pygame.QUIT:
            print('Quit radio')
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                print('Quit radio')
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            seconds = 0
            on_touch(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            update_screen()

    time.sleep(0.1)
