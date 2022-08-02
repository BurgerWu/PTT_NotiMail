#import modules and packages
from email.message import EmailMessage
import ssl
import os
from datetime import datetime
import smtplib

def send_mail(receiever_address, last_check_time, keyword, board_name, mail_content_list):  
    """
    This function sends email using smtplib library with content generated from input content list and template text.
    Input: 
    - receiever_address: Receiver's email address
    - last_check_time: Last time running keyword searching
    - keyword: Keyword of interest
    - mail_content_list: List containing titles with keyword inside
    
    Output: There is no output of this function
    """
    #Initiate titel_content_list text
    title_content_list = ""

    #Iterate through content list to generate list object in html format
    for item in mail_content_list:
        title_content_list += '<li><a href={}>{}</a></li>'.format("ptt.cc" + item['href'], item['title'])
    
    #Generate title content insertion to mail body
    title_content = """<ol>{}</ol>""".format(title_content_list)

    #Open mail template and insert title content to mail body
    with open("mail_template.txt",'r+') as f:
        mail_content = f.read().format(keyword, board_name, last_check_time, title_content)

    #Define email sender and corresponding password
    email_sender = 'aritek1x5@gmail.com'
    email_password = os.getenv('Python_email_credentials')

    #Set the subject and information about the mail
    subject = 'PTT Notification Mail for {} in {} - {}'.format(keyword, board_name, datetime.strftime(datetime.now(),"%Y-%m-%d"))
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiever_address
    em['Subject'] = subject

    #Set content of the email and specify it as html format
    em.set_content(mail_content, 'html')

    #Add SSL for security
    context = ssl.create_default_context()

    #Log in to smpt server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiever_address, em.as_string())