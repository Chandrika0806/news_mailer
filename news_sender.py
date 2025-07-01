from functions import load_users, fetch_news, send_email
import datetime

def main():
    print(f"\n--- News Mailer started at {datetime.datetime.now()} ---")

    users = load_users()
    if not users:
        print("⚠️ No users found in users.json.")
        return

    for email, info in users.items():
        try:
            print(f"Sending news to: {email}")
            news = fetch_news(info['categories'])
            send_email(email, news)
            print(f"✅ Successfully sent to: {email}")
        except Exception as e:
            print(f"❌ Error sending to {email}: {e}")

    print("--- News sending completed ---")

if __name__ == '__main__':
    main()
