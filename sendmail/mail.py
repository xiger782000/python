import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import socket
import fcntl
import struct

import subprocess
import sys

########## Global IP ##########
def getip():
  cwd='./'
  cmdline = 'curl ipv4.icanhazip.com'

  p = subprocess.Popen (cmdline, shell=True, cwd=cwd, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        close_fds=True)

  (stdouterr, stdin) = (p.stdout, p.stdin)


  if sys.version_info.major == 3:
    i=0
    while True:
      line = str (stdouterr.readline (), encoding='utf-8')
      if not line:
        break
      if i == 3:
        return line.strip()
      i=i+1
  else:
    i=0
    while True:
      line = stdouterr.readline ()
      if not line:
        break
      if i == 3:
        return line.strip()
      i=i+1

  ret = p.wait ()

######## Ethernet Local IP #######
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


######## SendMail #######
def sendMail():
    ######## Ethernet IP #########
    sub_ip=get_ip_address('lo')
    host_ip=get_ip_address('eth0')
    global_ip=getip()

    ######## Mail Setup ##########
    userid = 'send mail address'
    userpw = 'send mail password'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    from_mail = userid
    to_mail = 'to mail address'

    ######## Mail Content ########
    subject = '[raspberry pi]ip = ' + str(host_ip)
    message = 'host_ip=' + str(host_ip) + '\n' + 'global ip=' + str(global_ip) + '\n'

    ######## Mail Message Setting #############
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg.attach(MIMEText(message, 'plain'))

    ######## Mail ##########
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls();
    server.login(userid, userpw)
    server.sendmail(from_mail, to_mail, msg.as_string())
    server.close()

if __name__ == '__main__' :
    sendMail()