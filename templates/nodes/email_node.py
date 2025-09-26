# templates/nodes/email_node.py
import smtplib
from email.message import EmailMessage
import os
from typing import Dict

def email_node(state: Dict) -> Dict:
    """
    Sends an email using SMTP with robust error handling.
    Requires sender credentials to be set in environment variables.
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            # More helpful error message with graceful fallback
            error_msg = (
                "Email credentials not configured. Please set:\n"
                "SENDER_EMAIL=your@email.com\n"
                "SENDER_PASSWORD=your_app_password\n"
                "in your .env file or environment variables"
            )
            print(f"⚠️ {error_msg}")
            new_state = state.copy()
            new_state["status"] = "Email skipped - no credentials configured"
            new_state["recipient"] = state.get("recipient", "unknown")
            return new_state

        # Get email content from state
        body = (state.get("body") or 
                state.get("summary") or 
                state.get("translation") or 
                state.get("text", ""))
        
        if not body.strip():
            print("⚠️ No email content found in state")
            new_state = state.copy()
            new_state["status"] = "Email skipped - no content"
            new_state["recipient"] = state.get("recipient", "unknown")
            return new_state

        recipient = state.get("recipient", sender_email)

        # Create email message
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = state.get("subject", "Automated Agent Report")
        msg['From'] = sender_email
        msg['To'] = recipient

        # Send email
        print(f"📧 Attempting to send email to {recipient}...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        new_state = state.copy()
        new_state["status"] = "Email sent successfully"
        new_state["recipient"] = recipient
        print(f"✅ Email sent successfully to {recipient}!")
        return new_state
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "SMTP authentication failed. Check your email credentials and app password."
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        return new_state
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {e}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        return new_state
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"❌ Email failed: {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        return new_state