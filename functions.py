import os
import json
import requests
from email.mime.text import MIMEText
import smtplib

# Constants
USERS_FILE = 'users.json'
API_KEY = 'a85520c611194e80a7e989fad1db00b3'  # Replace with your actual NewsAPI key
FROM_EMAIL = 'chandrikanarne45@gmail.com'
EMAIL_PASSWORD = 'qdgahyugxnpowxzl'  # Replace with your Gmail App Password

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_news(categories):
    news_by_category = {}
    for category in categories:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={API_KEY}'
        try:
            response = requests.get(url, verify=False)  # Disable SSL verification
            data = response.json()
            if data['status'] == 'ok':
                headlines = [article['title'] for article in data['articles'][:5]]
                news_by_category[category] = headlines
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch news for {category}: {e}")
    return news_by_category


def send_email(to_email, news_by_category):
    content = ""
    if not news_by_category:
        content = "<p>No news available at this time. Please check back later.</p>"
    else:
        for category, headlines in news_by_category.items():
            content += f"<h3>{category.title()} News</h3><ul>"
            if headlines:
                for headline in headlines:
                    content += f"<li>{headline}</li>"
            else:
                content += "<li>No news available right now.</li>"
            content += "</ul><br>"

    msg = MIMEText(content, 'html')
    msg['Subject'] = 'Your Personalized News Digest'
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(FROM_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
