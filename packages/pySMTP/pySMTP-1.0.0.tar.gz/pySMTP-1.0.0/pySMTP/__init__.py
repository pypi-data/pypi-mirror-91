import smtplib


def send_email(sender_email, sender_password, receiver_email, email_body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, email_body)


def help():
    print("""pySMTP is an easy-to-use python library to send emails within seconds
    
Usage:
import pySMTP
pySMTP.send_email(sender_email, sender_password, receiver_email, email_body)
    
Example:
import pySMTP
pySMTP.send_email('my.email@email.com', 'my_password', 'my.friends.email@email.com', 'I sent this email with python!')
    
IMPORTANT:
Gmail users must turn on 'Less secure app access' in order to avoid smtplib errors. 
You can turn it on like so:

- go to 'Manage your google account'
- then click on the 'security' tab
- scroll down until you find 'Less secure app access' and click on the 'Turn on access' button
- you should be asked to "Allow less secure apps" again. turn it on.
    
If you've followed these steps correctly, you should be good to go!
(NOTE: turning this feature is generally not a good idea (see why online), I suggest turning it off when you're done, or using a burner gmail account if you have to)""")
