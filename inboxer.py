import base64
import email
import imaplib
import os
import smtplib

from email.mime.text import MIMEText


username   = os.getenv("USERNAME")
password   = os.getenv("PASSWORD")
hostname   = os.getenv("HOSTNAME")
directory  = os.getenv("DIRECTORY")
target     = os.getenv("TARGET")
from_email = os.getenv("FROM_EMAIL")
base_url   = os.getenv("BASE_URL")


def run():
    print("Connecting...")
    M = imaplib.IMAP4_SSL(hostname)
    M.login(username, password)
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        mid = int(num)
        if mid > 0:
          print('# Message %s' % (mid))
          (result, file_name) = ana2(data[0][1])
          if result:
              M.copy(num, target)
              M.store(num, '+FLAGS', '\\Deleted')
              if file_name:
                  x = draft_reply(file_name, data[0][1])
                  with smtplib.SMTP(hostname) as sx:
                      print(sx.noop())
                      print(sx.login(username, password))
                      print(sx.send_message(x))
    M.close()
    M.logout()


def draft_reply(file_name, msg):
    msg = msg.decode("utf-8")
    em = email.message_from_string(msg)

    subj = em.get("Subject")
    rt = em.get("Reply-To")
    to = em.get("From")
    if rt:
        to = rt
    new_msg = MIMEText(base_url + file_name)
    new_msg["To"] = to
    new_msg["From"] = from_email
    new_msg["Subject"] = "Re: " + subj
    return new_msg


def ana2(msg):
    msg = msg.decode("utf-8")
    em = email.message_from_string(msg)

    if em.is_multipart():
        for px in em.get_payload(decode=False):
            fn = px.get_filename()
            if not fn:
                continue
            pl = px.get_payload()
            c = base64.b64decode(pl)
            subj = em.get("Subject")
            if subj[0:3].lower() == 'to:':
                fn = subj[3:]
            fn = fn.strip()
            out_file = directory + "/" + fn
            with open(out_file, 'wb+') as fh:
                print("> {}\t{}".format(fn, out_file))
                fh.write(c)
            print("------------------")
            return (True, fn)
    else:
        print("> mail not multipart: {}".format(em.get("Subject")))
        print(em.get_payload().strip())
        print("------------------")
        return (True, None)

run()
