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
  
def emailAlert():
  global min_T
  global smtpUser
  global smtpPass
  toAdd = 'earthling471@gmail.com'
  fromAdd = smtpUser
  subject = "Minimum Temperature in the Greenhouse overnight"
  header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
  body = 'The Minimum Temperature overnight was : ' + str(min_T) + '\n\n\n' + 'Message sent from Greenhouse pi'

  s = smtplib.SMTP('smtp.gmail.com', 587)    # gmail also uses port 465, try it if this one gives you trouble
  #s = smtplib.SMTP('smtp.office365.com', 587)    #outlook uses this smtp server and port number

  # This sets us up for encryption, before sending username and password over the internet
  s.ehlo()
  s.starttls()
  s.ehlo()
  s.login(smtpUser, smtpPass)  # logging into server to send the email
  s.sendmail(fromAdd, toAdd, header + '\n\n' + body)  # declares to who it is sent. needs 2 linefeeds

  print('Temperature message sent' + '\n' + '--------------->')

  s.quit           # when the email is sent, we close the server  
  return  

