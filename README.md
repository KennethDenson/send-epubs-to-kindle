# Send EPUBs to Kindle

This Python script automates the process of searching for `.epub` files in a specified directory and its subdirectories, then emailing them to a designated Kindle email address. The script ensures that each file is only sent once and introduces a delay between emails to avoid overwhelming the email server.

## Features

- **Recursive Search**: Searches through a specified directory and all its subdirectories for `.epub` files.
- **Email Sending**: Sends each `.epub` file as an email attachment.
- **Avoid Duplicate Sends**: Keeps track of sent files using a log file to prevent resending.
- **Rate Limiting**: Introduces a delay (1 minute) between sending each email to avoid server overload.

## Requirements

- Python 3.x

You'll download the [send-epubs-to-kindle.py](url) (or copy and paste into a new python file) on your linux machine. Edit the areas of the script that are marked. I recomend setting environment variables for the sending email address and it's password by doing the following:


```bash
export EMAIL_LOGIN='your_email@example.com'
export EMAIL_PASSWORD='your_password'
