import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email():

    message = Mail(
        from_email="sivamapandeya239@gmail.com",  # verified sender
        to_emails="shivampandey52444@gmail.com",   # send to yourself for testing
        subject="Test Email from HRM System",
        plain_text_content="This is a test email from your agentic HRM system 🚀"
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)

        print("Status Code:", response.status_code)
        print("Headers:", response.headers)

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    send_email()