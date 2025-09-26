# ===== Fixed templates/nodes/email_node.py =====
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Dict, Optional

def email_node(state: Dict) -> Dict:
    """
    Enhanced email sending node with robust error handling and multiple content sources.
    """
    try:
        # Get credentials
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
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

        # Get email content from various possible state keys
        content_sources = ["body", "summary", "translation", "text"]
        body = ""
        content_type = "unknown"
        
        for source in content_sources:
            if state.get(source) and str(state[source]).strip():
                body = str(state[source]).strip()
                content_type = source
                break
        
        if not body:
            print("⚠️ No email content found in state")
            new_state = state.copy()
            new_state["status"] = "Email skipped - no content"
            new_state["recipient"] = state.get("recipient", "unknown")
            return new_state

        recipient = state.get("recipient", sender_email)
        
        # Validate recipient email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, recipient):
            error_msg = f"Invalid recipient email format: {recipient}"
            print(f"❌ {error_msg}")
            new_state = state.copy()
            new_state["status"] = f"Email failed: {error_msg}"
            new_state["recipient"] = recipient
            new_state["error"] = error_msg
            return new_state

        # Create subject based on content type and state
        subject_parts = ["Automated Agent Report"]
        if content_type == "summary":
            subject_parts.append("- Content Summary")
        elif content_type == "translation":
            target_lang = state.get("target_language", "unknown")
            subject_parts.append(f"- Translation to {target_lang}")
        elif state.get("scraped_url"):
            subject_parts.append(f"- From {state['scraped_url']}")
        
        subject = " ".join(subject_parts)
        custom_subject = state.get("subject")
        if custom_subject:
            subject = str(custom_subject)

        # Create email with metadata
        email_body = body
        
        # Add metadata footer
        metadata_lines = []
        if state.get("scraped_url"):
            metadata_lines.append(f"Source URL: {state['scraped_url']}")
        if state.get("original_word_count"):
            metadata_lines.append(f"Original word count: {state['original_word_count']}")
        if state.get("summary_word_count"):
            metadata_lines.append(f"Summary word count: {state['summary_word_count']}")
        if state.get("target_language"):
            metadata_lines.append(f"Translation target: {state['target_language']}")
        
        if metadata_lines:
            email_body += "\n\n" + "-" * 40 + "\n"
            email_body += "Metadata:\n" + "\n".join(metadata_lines)

        # Create and send email
        print(f"📧 Attempting to send email to {recipient}...")
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        
        # Attach the body
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

        # Try to send with multiple SMTP configurations
        smtp_configs = [
            ('smtp.gmail.com', 587, True),  # Gmail TLS
            ('smtp.gmail.com', 465, False),  # Gmail SSL
        ]
        
        email_sent = False
        last_error = None
        
        for smtp_server, port, use_tls in smtp_configs:
            try:
                if use_tls:
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                else:
                    with smtplib.SMTP_SSL(smtp_server, port) as server:
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                
                email_sent = True
                break
                
            except Exception as e:
                last_error = e
                continue
        
        if email_sent:
            new_state = state.copy()
            new_state["status"] = "Email sent successfully"
            new_state["recipient"] = recipient
            new_state["subject"] = subject
            new_state["content_type"] = content_type
            new_state["email_length"] = len(email_body)
            print(f"✅ Email sent successfully to {recipient}!")
            return new_state
        else:
            error_msg = f"All SMTP attempts failed. Last error: {last_error}"
            raise Exception(error_msg)
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = "SMTP authentication failed. Check your email credentials and app password."
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        new_state["error"] = error_msg
        return new_state
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {str(e)[:100]}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        new_state["error"] = error_msg
        return new_state
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)[:100]}"
        print(f"❌ Email failed: {error_msg}")
        new_state = state.copy()
        new_state["status"] = f"Email failed: {error_msg}"
        new_state["recipient"] = state.get("recipient", "unknown")
        new_state["error"] = error_msg
        return new_state