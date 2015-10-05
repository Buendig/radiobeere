#!/usr/bin/env python
# -*- coding: utf8 -*-

import MySQLdb
from glob import glob
import os
import login
import time
from mutagen.mp3 import MP3
import datetime


def audio_laenge(datei):
    audio = MP3(datei)
    sekunden = int(audio.info.length)
    laenge = str(datetime.timedelta(seconds = sekunden))
    return laenge


def main():

    connection = MySQLdb.connect(login.DB_HOST, login.DB_USER, login.DB_PASSWORD, login.DB_DATABASE)

    for pfad in glob('/var/www/Aufnahmen/aufnahme_fertig_*.mp3'):
        verzeichnis = os.path.dirname(pfad)
        teil = pfad.split('_')
        alias = teil[2]
        jahr = teil[3]
        monat = teil[4]
        tag = teil[5]
        stunde = teil[6]
        minute = teil[7]
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sender WHERE alias=%s",(alias,))
        for row in cursor:
            sender = "%s" % row
        datum = jahr+"."+monat+"."+tag 
        uhrzeit = stunde+":"+minute
        zeitstempel = time.mktime((int(jahr), int(monat), int(tag), int(stunde), int(minute), 0, 0, 0, -1))
        datei = alias+'_'+jahr+'-'+monat+'-'+tag+'_'+stunde+'-'+minute+'.mp3'
        laenge = audio_laenge(pfad)

        os.system('id3v2 -t'+'"'+sender+', '+tag+'.'+monat+'.'+jahr+', '+stunde+':'+minute+' Uhr'+'"'+' '+pfad)
        os.rename(pfad,verzeichnis+'/'+alias+'_'+jahr+'-'+monat+'-'+tag+'_'+stunde+'-'+minute+'.mp3')

        cursor.execute("INSERT INTO aufnahmen(datum, uhrzeit, sender, datei, zeitstempel, laenge) VALUES (%s,%s,%s,%s,%s,%s)",(datum, uhrzeit, sender, datei, zeitstempel, laenge,))
        connection.commit()

    connection.close()

if __name__ == '__main__':
    main()