from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import requests
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'users.json'

# 🔑 Replace this with your actual NewsAPI key
API_KEY = 'a85520c611194e80a7e989fad1db00b3'

# 📧 Replace with your email and app password
FROM_EMAIL = 'chandrikanarne45@gmail.com'
EMAIL_PASSWORD = 'qdgahyugxnpowxzl'  # Replace this before running


# 📂 Load and save users
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


# 🏠 Homepage
@app.route('/')
def index():
    return render_template('index.html')


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        categories = request.form.getlist('categories')
        users = load_users()
        if email in users:
            return "User already exists!"
        users[email] = {'password': password, 'categories': categories}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')


# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and users[email]['password'] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')


# 👤 Dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    users = load_users()
    user = users[session['email']]
    return render_template('dashboard.html', email=session['email'], categories=user['categories'])


# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


# 📰 Fetch news using NewsAPI
def fetch_news(categories):
    news_by_category = {}
    for category in categories:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'ok':
            headlines = [article['title'] for article in data['articles'][:5]]
            news_by_category[category] = headlines
    return news_by_category


# 📧 Send news email
def send_email(to_email, news_by_category):
    content = ""
    for category, headlines in news_by_category.items():
        content += f"<h3>{category.title()} News</h3><ul>"
        for headline in headlines:
            content += f"<li>{headline}</li>"
        content += "</ul><br>"

    msg = MIMEText(content, 'html')
    msg['Subject'] = 'Your Personalized News Digest 📰'
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(FROM_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)


# 🚀 Route to send news to all users
@app.route('/send-news')
def send_news():
    users = load_users()
    for email, info in users.items():
        news = fetch_news(info['categories'])
        send_email(email, news)
    return "News sent to all users!"

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    start_server()

