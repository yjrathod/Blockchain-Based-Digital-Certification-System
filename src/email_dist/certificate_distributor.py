from email_service import EmailService
from database_operations import DatabaseManager
import os
from datetime import datetime

class CertificateDistributor:
    def __init__(self):
        self.email_service = EmailService()
        self.db_manager = DatabaseManager()
        print("🚀 Certificate Distributor initialized!")
    
    def add_certificate_to_queue(self, name: str, email: str, certificate_type: str, 
                                pdf_path: str, organization: str = None, phone: str = None,
                                custom_subject: str = None, custom_body: str = None) -> int:
        """Add a certificate to the sending queue"""
        
        # Verify PDF exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Add participant
        participant_id = self.db_manager.add_participant(name, email, organization, phone)
        
        # Create email content
        subject = custom_subject or f"Your {certificate_type} Certificate"
        body = custom_body or f"""Dear {name},

Congratulations! 🎉

We are pleased to present you with your {certificate_type} certificate attached to this email.

Thank you for your participation and dedication.

Best regards,
Certificate Team
"""
        
        # Add certificate record
        certificate_id = self.db_manager.add_certificate_record(
            participant_id, certificate_type, pdf_path, subject, body
        )
        
        print(f"📋 Certificate added to queue: {name} - {certificate_type}")
        return certificate_id
    
    def send_single_certificate(self, certificate_id: int) -> bool:
        """Send a specific certificate by ID"""
        # Get certificate details
        pending_certs = self.db_manager.get_pending_certificates()
        cert = next((c for c in pending_certs if c['certificate_id'] == certificate_id), None)
        
        if not cert:
            print(f"❌ Certificate ID {certificate_id} not found or already sent")
            return False
        
        return self._send_certificate(cert)
    
    def send_all_pending(self) -> dict:
        """Send all pending certificates"""
        pending_certificates = self.db_manager.get_pending_certificates()
        
        if not pending_certificates:
            print("ℹ️  No pending certificates to send")
            return {'total': 0, 'sent': 0, 'failed': 0}
        
        print(f"📬 Found {len(pending_certificates)} pending certificates")
        
        results = {'total': len(pending_certificates), 'sent': 0, 'failed': 0}
        
        for cert in pending_certificates:
            print(f"\n📧 Processing: {cert['name']} ({cert['email']})")
            
            if self._send_certificate(cert):
                results['sent'] += 1
            else:
                results['failed'] += 1
        
        print(f"\n📊 Summary: {results['sent']} sent, {results['failed']} failed out of {results['total']} total")
        return results
    
    def _send_certificate(self, cert: dict) -> bool:
        """Internal method to send a certificate"""
        try:
            # Send email
            success, result = self.email_service.send_email(
                cert['email'],
                cert['email_subject'] or f"Your {cert['certificate_type']} Certificate",
                cert['email_body'] or f"Dear {cert['name']},\n\nPlease find your certificate attached.\n\nBest regards,\nCertificate Team",
                cert['pdf_path']
            )
            
            # Update status
            if success:
                self.db_manager.update_certificate_status(cert['certificate_id'], 'sent')
                print(f"✅ Sent to {cert['email']}")
                return True
            else:
                self.db_manager.update_certificate_status(cert['certificate_id'], 'failed', result)
                print(f"❌ Failed to send to {cert['email']}: {result}")
                return False
                
        except Exception as e:
            error_msg = f"Exception during send: {str(e)}"
            self.db_manager.update_certificate_status(cert['certificate_id'], 'failed', error_msg)
            print(f"❌ Exception for {cert['email']}: {error_msg}")
            return False
    
    def show_statistics(self):
        """Display database statistics"""
        stats = self.db_manager.get_statistics()
        print("\n📊 Certificate Statistics:")
        print(f"   Total Participants: {stats['total_participants']}")
        print(f"   Total Certificates: {stats['total_certificates']}")
        print(f"   ✅ Sent: {stats['sent_certificates']}")
        print(f"   ⏳ Pending: {stats['pending_certificates']}")
        print(f"   ❌ Failed: {stats['failed_certificates']}")
    
    def show_recent_history(self, limit: int = 10):
        """Display recent certificate history"""
        history = self.db_manager.get_certificate_history(limit)
        
        print(f"\n📋 Recent {limit} Certificates:")
        print("-" * 80)
        print(f"{'Name':<20} {'Email':<25} {'Type':<15} {'Status':<10} {'Sent At'}")
        print("-" * 80)
        
        for record in history:
            name, email, cert_type, status, sent_at, error = record
            sent_time = sent_at if sent_at else 'Not sent'
            print(f"{name:<20} {email:<25} {cert_type:<15} {status:<10} {sent_time}")