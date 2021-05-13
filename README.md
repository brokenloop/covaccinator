# Covaccinator

A scraper to find available Covid 19 vaccination appointments in Montreal.

## Getting Started


### Installing dependencies

You'll need Python 3.9+.

```
pip install -r requirements.txt
python main.py
```

### Running the project

Create a `secret.py` file, containing an authtoken from https://clients3.clicsante.ca/, as well as credentials for an email account capable of sending email. You can find instructions on how to get these credentials [here](https://towardsdatascience.com/e-mails-notification-bot-with-python-4efa227278fb).

You can get your auth token from clicsante using developer tools in Google Chrome.

#### Sample secret.py

```
# Email Account
email_sender_account = "samplesender@gmail.com"
email_sender_username = "samplesender"
email_sender_password = "some_password"
email_smtp_server = "smtp.gmail.com"
email_smtp_port = 587

# Email Content
email_recepients = ["samplerecipient@gmail.com"]

authtoken = "cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh"

```

