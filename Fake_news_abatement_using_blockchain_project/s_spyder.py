# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:38:41 2020

@author: curse
"""

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

MY_ADDRESS = 'cursednarutouzumaki@gmail.com'
PASSWORD = 'Maverick@467'
transactions = 'neptune is blue maybe'

# set up the SMTP server
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

names, emails = get_contacts('hot_words.txt') # read contacts
message_template = read_template('message_template.txt')
res = dict(zip(names, emails))

line = transactions.split()
for word in names:
    lower = word.lower()
    lower = lower.rstrip()
    count = 0
    for each in line:
        line2 = each.lower()
        line2 = line2.strip("!@#$%^&*()_-+=")
        if lower == line2:
            count+=1
    if count != 0:

        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=word.title())

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=res["word"]
        msg['Subject']="This is TEST"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

# Terminate the SMTP session and close the connection
s.quit()




