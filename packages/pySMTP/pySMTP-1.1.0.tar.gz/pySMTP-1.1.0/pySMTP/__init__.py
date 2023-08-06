import smtplib


def send_email(sender_email, sender_password, receiver_email, email_subject, email_body):
    email_contents = 'Subject: {}\n\n{}'.format(email_subject, email_body)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, email_contents)


def help():
    print("""pySMTP is an easy-to-use python library to send emails within seconds
    
Usage:
import pySMTP
pySMTP.send_email(sender_email, sender_password, receiver_email, email_subject, email_body)
    
Example:
import pySMTP
pySMTP.send_email('my.email@email.com', 'my_password', 'my.friends.email@email.com', 'Test', 'I sent this email with python!')
    
IMPORTANT:
Gmail users must turn on 'Less secure app access' in order to avoid smtplib errors. 
You can turn it on like so:

- go to 'Manage your google account'
- then click on the 'security' tab
- scroll down until you find 'Less secure app access' and click on the 'Turn on access' button
- you should be asked to "Allow less secure apps" again. turn it on.

NOTE: turning this feature is generally not a good idea as it isn't safe (see why online)
I suggest you continue reading the 'SAFER ALTERNATIVE' below.

SAFER ALTERNATIVE:
You can use an app password. See how to make one below:

- go to 'Manage your google account'
- then click on the 'security' tab
- find 'Signing into Google'
- click on 'App passwords'
- type out your password
- change 'Select app' to 'Mail'
- change 'Select device' to the device you are currently using

If you've followed these steps correctly, you should be good to go!
""")
