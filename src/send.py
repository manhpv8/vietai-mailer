
import smtplib
from src.utils.html import read_html_template
from src.utils.logger import get_logger
from src.utils.score_table import generate_content_ranking_html

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

import config


logger = get_logger()

def send_email(to_email: str, content_html: str):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = config.email_sender
    msg['From'] = config.email_sender
    msg['To'] = to_email

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(content_html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(config.email_sender, config.password_sender)
        smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_server.close()
        logger.warn(f"Send to email {to_email} Successfuly!!!")
    
    except Exception as ex:
        logger.exception(f"Send to email {to_email} Failed!!!")
        logger.exception(f"Something went wrong: {ex}")
        return False, str(ex)
    return True, ""
        

def send_multiple_emails(template_location_path: str, data_df: pd.DataFrame):
    results = []
    tabel_ranking_template_html = read_html_template(location_path=template_location_path)
    for row in data_df.itertuples():
        curr_email = row.email
        content_html = generate_content_ranking_html(
            data_df = data_df,
            curr_email = curr_email,
            template_html = tabel_ranking_template_html
        )

        if content_html == None:
            results.append(f"{curr_email} Failed, Reason: content_html == None")        
        
        else:
            # send email
            status, message = send_email(to_email = curr_email, content_html= content_html)
            if status == False:
                results.append(f"{curr_email} Failed, Reason: {message}")
            else:
                results.append(f"{curr_email} Successed!!!")
    return results



        