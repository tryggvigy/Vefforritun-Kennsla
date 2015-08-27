#!/usr/bin/python
# -*- encoding: utf-8 -*-

import argparse, os, smtplib
import email_composer
from ODSReader import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

gmail_user = "user"
gmail_pass = "pass"

def send_mail(to, subject, text, attach, mailServer):
	msg = MIMEMultipart()

	msg['From'] = gmail_user
	msg['To'] = to
	msg['Subject'] = subject

	msg.attach(MIMEText(text, 'plain', 'utf-8'))


	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition',
	       'attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part)

	mailServer.sendmail(gmail_user, to, msg.as_string())

def main():
	script_dir = '.'

	parser = argparse.ArgumentParser(description='This program sends emails to every student specified in an .ods file inside a specific project.')
	parser.add_argument('-b','--basedir', help='base directory of project.', required=True)
	parser.add_argument('-s','--subject', help='subject of emails.', required=True)
	parser._optionals.title = "flag arguments"
	args = vars(parser.parse_args())

	#directories
	base_dir = os.path.join(script_dir, args['basedir'])
	projects_dir = os.path.join(base_dir, "YFIRFARID")
	ODS_FILE = os.path.join(base_dir, "yfirferd.ods")


	doc = ODSReader(ODS_FILE)
	table = doc.getSheet("Sheet1")

	# Connect to gmail
	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmail_user, gmail_pass)

	# Send emails
	email_addresses = email_composer.get_email_addresses(table)
	for address in email_addresses:
		email_body = email_composer.compose_email(table, address)
		send_mail(address+"@hi.is", args['subject'], email_body, os.path.join(projects_dir, address, 'UMSOGN.txt'), mailServer)
		print email_body;
		print "[*] mail sent to " + address
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()

if __name__ == '__main__':
	main()
