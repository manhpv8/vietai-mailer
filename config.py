import os
from src.utils.env import load_and_set_env_vars

ENV  = 'dev'
load_and_set_env_vars(ENV)

subject  = os.getenv("SUBJECT")
email_sender  = os.getenv("EMAIL_SENDER")
password_sender  = os.getenv("PASSWORD_SENDER")

host= os.getenv("HOST")
port =  os.getenv("PORT")