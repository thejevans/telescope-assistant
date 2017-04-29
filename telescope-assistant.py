# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:12:35 2017

@author: Jordan
"""

import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import time
import serial
from astropy.coordinates.name_resolve import NameResolveError
from datetime import datetime

ts = time.time()
lat = 41.3 #assuming south is negative
lon = -76.9378 #west is negative
height = 21 
#utcoffset = -4*u.hour #EDT #get EDT from lat, lon
utcoffset = (datetime.fromtimestamp(ts)-datetime.utcfromtimestamp(ts)).total_seconds()*u.s

def find_star(star_name,lat,lon,height,utcoffset):
    star = SkyCoord.from_name(star_name)
    observatory = EarthLocation(lat*u.deg, lon*u.deg,height=height*u.m)
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    t = Time(str(t)) - utcoffset
    star_altaz = star.transform_to(AltAz(obstime=t,location=observatory))
    alt = star_altaz.alt.deg
    az = star_altaz.az.deg
    return alt,az



#Start the serial port to communicate with arduino
data = serial.Serial('com10',9600, timeout=0)

 
#now we made an infinite while loop so the serial connection is maintained and we can keep communicating with arduino
while (1==1):
    star_name = str(raw_input("Enter object designation: ")) #Prompt the user for the angle
    try: 
        alt,az = find_star(star_name,lat,lon,height,utcoffset)
    except NameResolveError:
        print "Name not found. Try another."
        continue
    
    if alt > 0:
        az += 90
        if az > 360:
            az -= 360
            if alt > 180:
               az -= 180
               alt = 180-alt
        print alt,az
        alt = str(alt)+"t,"
        az = str(az)+"p,"
        data.write(alt+az) #code and send the angle to the Arduino through serial port160
    else:
        print "Object is below the horizon! Try another."
