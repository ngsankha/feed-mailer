#!/usr/bin/env python3

import pickle
import yaml
import feedparser
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

STATE_FILE  = 'feed_email.state'
CONFIG_FILE = 'config.yaml'

config = yaml.load(open(CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
state = {}
body = ''

if os.path.isfile(STATE_FILE):
	with open(STATE_FILE, 'rb') as f:
		state = pickle.load(f)

for feed in config['feeds']:
	parsed_feed = feedparser.parse(feed)
	text_feed = ''
	dates = []
	for item in parsed_feed.entries:
		usable_date = None
		if 'published_parsed' in item:
			usable_date = item.published_parsed
		else:
			usable_date = item.updated_parsed
		if feed in state:
			if state[feed] < usable_date:
				text_feed += ("%s\n%s\n\n" % (item.title, item.link))
				dates.append(usable_date)
		else:
			text_feed += ("%s\n%s\n\n" % (item.title, item.link))
			dates.append(usable_date)

	if len(dates) != 0:
		state[feed] = max(dates)
	if text_feed != "":
		body += (parsed_feed.feed.title + "\n")
		body += "==========================\n"
		body += text_feed

body = body.strip()
if body != '':
	msg = MIMEMultipart()
	msg['From'] = 'Feeds Update'
	msg['To'] = config['to']
	msg['Subject'] = 'New posts today'
	msg.attach(MIMEText(body))
	mail_server = smtplib.SMTP("smtp.gmail.com", 587)
	mail_server.ehlo()
	mail_server.starttls()
	mail_server.ehlo()
	mail_server.login(config['auth']['username'], config['auth']['password'])
	mail_server.sendmail(config['auth']['username'], config['to'], msg.as_string())
	mail_server.close()

	with open(STATE_FILE, 'wb') as f:
		pickle.dump(state, f)
