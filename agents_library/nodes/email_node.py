# templates/nodes/email_node.py
import smtplib
from email.message import EmailMessage
import os
from typing import Dict

def email_node(state: Dict) -> Dict:
    """
    Sends an email using SMTP.
    Requires sender credentials to be set in environment variables.
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            raise ValueError("SENDER_EMAIL and SENDER_PASSWORD environment variables not set.")

        body = state.get("body") or state.get("summary") or state.get("translation") or state.get("text", "")
        recipient = state.get("recipient", sender_email)

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = "Automated Agent Report"
        msg['From'] = sender_email
        msg['To'] = recipient

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        new_state = state.copy()
        new_state["status"] = "Email sent successfully."
        new_state["recipient"] = recipient
        print(f"📧 Sent a real email to {recipient}!")
        return new_state
    except Exception as e:
        print(f"❌ ERROR: Email failed to send. Check credentials and permissions. Details: {e}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {e}"
        new_state["recipient"] = state.get("recipient", "unknown")
        return new_state