# Project Title


## Introduction

A brief introduction to the project and its purpose.

## Table of Contents



## Installation

1. Clone this repository to your local machine.
git clone https://github.com/Phammanh26/vietai-mailer
2. Configuring environment variables in conf/dev/.env
  - Navigate to the conf/dev directory in your project.
  - Create a new file named .env.
  - Open the .env file in a text editor.
  - Define the required environment variables in the .env file. In your case, the following environment variables should be defined:

  SUBJECT - A string containing the subject of the email you want to send.
  ### EMAIL_SENDER - The email address of the sender.
  ### PASSWORD_SENDER - The password of the email account of the sender.
  ### HOST - The IP address of the host where the application is running.
  ### PORT - The port number that the application is running on.
  
  #### Here's an example of how you can define these variables in the .env file:
    SUBJECT='VIETAI | BÁO CÁO XẾP HẠNG HÀNG TUẦN'
    EMAIL_SENDER='example@example.com'
    PASSWORD_SENDER='password123'
    HOST='0.0.0.0'
    PORT=8000
    Save the .env file. The environment variables will be automatically loaded when you start your application using Docker Compose.








3. Build docker
docker compose up

4. Access url: http://0.0.0.0:8000
