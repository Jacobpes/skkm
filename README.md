## Automated agent for giving notifications for ending auctions at skkm.fi

### How to use

1. Clone the repository
2. Install the dependencies by running `pip install -r requirements.txt`
3. Create a .env file and add the following variables:
- SENDER_EMAIL= your@email.com
- SENDER_PASSWORD= Your_email_password1234
- RECEIVER_EMAIL= recipient@email.com
- SMTP_SERVER= smtp.gmail.com
- SMTP_PORT=587
3. Run the script by running `python main.py`