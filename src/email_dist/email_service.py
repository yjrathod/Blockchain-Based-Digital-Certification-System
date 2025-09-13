import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class EmailService:
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.readonly'
    ]
    
    def __init__(self):
        self.service = self.authenticate_gmail()
        print("✅ Gmail service authenticated successfully!")
    
    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Check if token.json exists (saved credentials)
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            print("📄 Found existing token.json")
        
        # If there are no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
            else:
                print("🔐 Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ Authorization completed!")
            
            # Save credentials for next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                print("💾 Token saved to token.json")
        
        return build('gmail', 'v1', credentials=creds)
    
    def create_message_with_attachment(self, to_email: str, subject: str, body: str, attachment_path: str):
        """Create email message with file attachment"""
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject
        
        # Add email body
        message.attach(MIMEText(body, 'plain'))
        
        # Add file attachment
        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            message.attach(part)
        else:
            raise FileNotFoundError(f"Attachment file not found: {attachment_path}")
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    def send_email(self, to_email: str, subject: str, body: str, attachment_path: str) -> tuple:
        """Send email with attachment"""
        try:
            print(f"📧 Sending email to: {to_email}")
            
            # Create message
            message = self.create_message_with_attachment(to_email, subject, body, attachment_path)
            
            # Send message
            sent_message = self.service.users().messages().send(
                userId="me", body=message
            ).execute()
            
            print(f"✅ Email sent successfully! Message ID: {sent_message['id']}")
            return True, sent_message['id']
            
        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
            
        except HttpError as e:
            error_msg = f"Gmail API error: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def test_connection(self):
        """Test Gmail API connection"""
        try:
            # Try to get user profile to test connection
            profile = self.service.users().getProfile(userId="me").execute()
            email = profile.get('emailAddress')
            print(f"✅ Gmail API connection successful!")
            print(f"📧 Connected account: {email}")
            return True, email
        except HttpError as e:
            if 'insufficient' in str(e).lower() or '403' in str(e):
                print(f"❌ Gmail API connection failed: Insufficient permissions")
                print(f"💡 This usually means you need to re-authenticate with proper scopes.")
                print(f"🔧 Please delete token.json and try again.")
            else:
                print(f"❌ Gmail API HTTP error: {str(e)}")
            return False, str(e)
        except Exception as e:
            print(f"❌ Gmail API connection failed: {str(e)}")
            return False, str(e)
