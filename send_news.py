from functions import load_users, fetch_news, send_email
import datetime

def main():
    print(f"📅 Script started at {datetime.datetime.now()}")

    users = load_users()
    if not users:
        print("⚠️ No users found in users.json.")
        return

    for email, info in users.items():
        try:
            print(f"📬 Sending news to: {email}")
            news = fetch_news(info['categories'])
            send_email(email, news)
            print(f"✅ Successfully sent news to {email}")
        except Exception as e:
            print(f"❌ Failed to send email to {email}: {e}")

    print("🎉 All emails processed.")

if __name__ == '__main__':
    main()
