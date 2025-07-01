from functions import load_users, fetch_news, send_email

def main():
    users = load_users()
    for email, info in users.items():
        news = fetch_news(info['categories'])
        send_email(email, news)
    print("✅ News sent to all users!")

if __name__ == '__main__':
    main()
