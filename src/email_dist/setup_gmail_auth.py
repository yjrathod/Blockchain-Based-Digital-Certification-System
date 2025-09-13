#!/usr/bin/env python3
"""
Gmail Authentication Setup Script
This script helps set up Gmail API authentication properly.
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes needed
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def setup_authentication():
    """Set up Gmail API authentication step by step"""
    print("🔐 Gmail API Authentication Setup")
    print("=" * 50)
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("📋 To fix this:")
        print("   1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("   2. Create or select a project")
        print("   3. Enable Gmail API")
        print("   4. Create OAuth 2.0 credentials (Desktop application)")
        print("   5. Download and save as 'credentials.json' in this directory")
        return False
    
    print("✅ Found credentials.json")
    
    # Remove existing token if it exists
    if os.path.exists('token.json'):
        print("🗑️  Removing existing token.json for fresh authentication...")
        os.remove('token.json')
    
    creds = None
    
    try:
        print("🔐 Starting OAuth flow...")
        print("📱 Your browser will open automatically")
        print("🔗 If it doesn't, please copy and paste the URL that appears below")
        
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        
        # Try different methods to handle the OAuth flow
        try:
            # First try with run_local_server
            creds = flow.run_local_server(
                port=0,
                prompt='consent',
                open_browser=True
            )
        except Exception as e:
            print(f"⚠️  Local server method failed: {e}")
            print("🔄 Trying manual method...")
            
            # Fallback to manual method
            creds = flow.run_console()
        
        print("✅ Authentication successful!")
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("💾 Credentials saved to token.json")
        
        # Test the connection
        print("\n🧪 Testing Gmail API connection...")
        service = build('gmail', 'v1', credentials=creds)
        
        try:
            # Test basic API access
            profile = service.users().getProfile(userId="me").execute()
            email = profile.get('emailAddress')
            print(f"✅ Gmail API connection successful!")
            print(f"📧 Connected account: {email}")
            
            # Test message listing (readonly permission)
            messages = service.users().messages().list(userId="me", maxResults=1).execute()
            print("✅ Gmail read permissions working")
            
            print("\n🎉 Setup completed successfully!")
            print("🚀 You can now run: python main.py")
            
            return True
            
        except HttpError as e:
            print(f"❌ API test failed: {e}")
            if 'insufficient' in str(e).lower():
                print("💡 The authentication may need more permissions.")
                print("🔄 Try running this script again.")
            return False
            
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure your credentials.json is valid")
        print("   2. Check that Gmail API is enabled in Google Cloud Console")
        print("   3. Ensure your OAuth consent screen is configured")
        print("   4. Try running this script with administrator privileges")
        return False

def main():
    """Main function"""
    print("Starting Gmail authentication setup...\n")
    
    if setup_authentication():
        print("\n✅ Authentication setup complete!")
        print("📧 Ready to send certificates!")
    else:
        print("\n❌ Authentication setup failed!")
        print("📞 Please check the troubleshooting tips above.")
        sys.exit(1)

if __name__ == "__main__":
    main()