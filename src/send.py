
import smtplib
from src.utils.html import read_html_template
from src.utils.logger import get_logger
from src.utils.score_table import generate_content_ranking_html

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os


logger = get_logger()

def send_email(subject, to_email: str, html_content: str):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject 
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = to_email

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html_content, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login( os.getenv("EMAIL_SENDER"),  os.getenv("PASSWORD_SENDER"))
        smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_server.close()
        logger.warn(f"Send to email {to_email} Successfuly!!!")
    
    except Exception as ex:
        logger.exception(f"Send to email {to_email} Failed!!!")
        logger.exception(f"Something went wrong: {ex}")
        return False, str(ex)
    return True, ""
        

def send_multiple_emails( subject, data_df: pd.DataFrame):
    results = []
    for row in data_df.itertuples():
        curr_email = row.email
    
        html_content = row.html_content
        status, message = send_email(subject, to_email = curr_email, html_content= html_content)
        if status == False:
            results.append(f"{curr_email} Failed, Reason: {message}")
        else:
            results.append(f"{curr_email} Successed!!!")
    return results



        