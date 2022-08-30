from email.message import EmailMessage
import ssl
import smtplib

EMAIL_ADRESS = "@gmail.com"
EMAIL_PASSWORD = ""
EMAIL_RECEIVER = "@gmail.com"

subject = "FTX Action performed"
body = """
A trade has been successfully acomplished in your account
"""

em = EmailMessage()
em['From']=EMAIL_ADRESS
em['To']=EMAIL_RECEIVER
em['subject']= subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
    smtp.sendmail(EMAIL_ADRESS,EMAIL_RECEIVER,em.as_string())