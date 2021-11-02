import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import sys
sys.path.append("/Library/Python/3.7/site-packages")
from ringdb import ringdb

# Global Config
username = "info@ericvuu.com"
password = "" # This is yandex password
imap_srv = "imap.yandex.com"
NUM_MAIL = 100
# RingDB Config
REFEED_TIME = 10*60*60
EMAIL_PREFIX = "EMAIL_"
EMAIL_LIMIT = 100
email_db_inst = None


def feed_mail(num_mail = NUM_MAIL):
	# Connect
	imap = imaplib.IMAP4_SSL(imap_srv)
	# Authenticate
	imap.login(username, password)
	# Get inbox
	status, messages = imap.select("INBOX")
	# Get total email
	messages = int(messages[0])
	# Get num_mail recent mail
	for i in range(messages, messages-num_mail, -1):
		# Fetch mail
		res, msg = imap.fetch(str(i), "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				# Parse a bytes email into a message object
				msg = email.message_from_bytes(response[1])
				# Decode the email subject
				subject = decode_header(msg["Subject"])[0][0]
				if isinstance(subject, bytes):
					# If it's a bytes, decode to str
					subject = subject.decode()
				# Get the sensder
				from_ = msg.get("From")

				# Only find mail from PGSHARP
				if subject.find("Confirm Your Registration") != -1 and from_.find("noreply@pgsharp.com") != -1:
					if msg.is_multipart():
						for part in msg.walk():
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							try:
								body = part.get_payload(decode=True).decode()
							except:
								pass

							if content_type == "text/plain" and "attachment" not in content_disposition:
								line = body.split("\n")
								save_fmt = {"usrname" : "", "content" : line, "verify" : ""}
								for l in line:
									if l.startswith("Dear "):
										save_fmt["usrname"] = l.split(" ")[1]
									elif l.startswith("http://url3088.pgsharp.com"):
										save_fmt["verify"] = l
									else:
										pass
								save_mail(save_fmt)
							else:
								pass


def save_mail(data):
	global email_db_inst
	if not email_db_inst:
		email_db_inst = ringdb(EMAIL_LIMIT, EMAIL_PREFIX)
	email_db_inst.smart_save("usrname", data["usrname"], data)


def find_by_username(usr_name):
	global email_db_inst
	if not email_db_inst:
		email_db_inst = ringdb(EMAIL_LIMIT, EMAIL_PREFIX)
		return []
	else:
		data = email_db_inst.find_by(usr_name, "usrname")
		return data

if __name__ == '__main__':
	feed_mail(3)
	print(find_by_username("ukhflemdxi"))








