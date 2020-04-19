#!/usr/bin/python3

# Using a Raspberry pi to collect temps and put into db. Then send an email
# for the lowest temp overnight


import sqlite3
import smtplib  # email server support
import os       # allows access to system variables
# import imghdr   # allows email of pictures
from datetime import datetime
# from time import sleep
from email.message import EmailMessage

smtpUser = os.environ.get('smtpUser') # using envirnoment variable for critical data
smtpPass = os.environ.get('smtpPass')

conn = sqlite3.connect('/home/pi/greenhouse2020.db')
c = conn.cursor()

min_T=0
max_T=100

def get_min():
  global min_T
  c.execute('SELECT dt, MIN(temperature) FROM greenhouse ORDER BY dt ASC LIMIT 72;') # last 12hours
  min_T = c.fetchall()
  



