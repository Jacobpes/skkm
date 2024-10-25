import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


URL = "https://skkm.fi/?page=main"
MEMORY_LIST_FILE = "memory_list.txt"

load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
DEBUG = False
REQUEST_INTERVAL = 60

# Print out the environment variables to debug
if DEBUG:
    print(f"SMTP_SERVER: {SMTP_SERVER}")
    print(f"SMTP_PORT: {SMTP_PORT}")
print(f"SENDER_EMAIL: {SENDER_EMAIL}")
print(f"RECEIVER_EMAIL: {RECEIVER_EMAIL}")
print("--------------------------------")
print("Agent is running...")
print("")
item_id_memory = []
# read item_id_memory from file of found. item_id_memory.txt separated by commas
if os.path.exists('item_id_memory.txt'):
    with open('item_id_memory.txt', 'r') as file:
        item_id_memory = file.read().split(',')
        file.close()
else:
    item_id_memory = []
    # create item_id_memory.txt
    with open('item_id_memory.txt', 'w') as file:
        file.write('')
    file.close()

def send_email(subject, body, is_html=False):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    # Attach the body with appropriate MIME type
    if is_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    try:
        # Use SMTP_SSL if port is 465, otherwise use SMTP and starttls
        if SMTP_PORT == '465':
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        else:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.ehlo()
                server.starttls()  # Secure the connection
                server.ehlo()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        import traceback
        traceback.print_exc()
        return False

# define a function that writes to a file
def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# define a function that reads a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# read the auction names from the file and store them in a list
MEMORY_LIST = read_file(MEMORY_LIST_FILE).splitlines()

def get_auction_names(URL):
    response = requests.get(URL) # send a get request to the URL
    soup = BeautifulSoup(response.text, 'html.parser') # parse the HTML content
    auction_links = soup.select('ul.ui-menu a') # find all auction links
    auction_names = [link.get_text(strip=True) for link in auction_links] # extract the text from each link and store it in a list
    return auction_names

def check_for_new_auctions(auction_names):
    for auction_name in auction_names:
        if auction_name not in MEMORY_LIST:
            print(f"New auction found: {auction_name}")
            # add the auction name to MEMORY_LIST
            MEMORY_LIST.append(auction_name)
            write_to_file(MEMORY_LIST_FILE, '\n'.join(MEMORY_LIST))
            send_email(f"New auction found: {auction_name}", f"New auction found: {auction_name}")

# main function
def main():
    while True:
        auction_names = get_auction_names(URL)
        print(f"Found {len(auction_names)} auction names")
        print(auction_names)
        check_for_new_auctions(auction_names)
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    main()