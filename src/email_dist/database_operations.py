import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path='certificates.db'):
        self.db_path = db_path
    
    def add_participant(self, name: str, email: str, organization: Optional[str] = None, phone: Optional[str] = None) -> Optional[int]:
        """Add a participant to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO participants (name, email, organization, phone)
            VALUES (?, ?, ?, ?)
            ''', (name, email, organization, phone))
            participant_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Added participant: {name} ({email})")
            return participant_id
        except sqlite3.IntegrityError:
            # Email already exists, get existing participant
            cursor.execute('SELECT id FROM participants WHERE email = ?', (email,))
            participant_id = cursor.fetchone()[0]
            print(f"ℹ️  Participant already exists: {email}")
            return participant_id
        finally:
            conn.close()
    
    def add_certificate_record(self, participant_id: int, certificate_type: str, 
                             pdf_path: str, subject: str = None, body: str = None) -> int:
        """Add a certificate record to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO certificates (participant_id, certificate_type, pdf_path, email_subject, email_body)
        VALUES (?, ?, ?, ?, ?)
        ''', (participant_id, certificate_type, pdf_path, subject, body))
        
        certificate_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Added certificate record ID: {certificate_id}")
        return certificate_id
    
    def get_pending_certificates(self) -> List[Dict]:
        """Get all pending certificates to be sent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT c.id, p.name, p.email, p.organization, c.certificate_type, 
               c.pdf_path, c.email_subject, c.email_body
        FROM certificates c
        JOIN participants p ON c.participant_id = p.id
        WHERE c.email_status = 'pending'
        ORDER BY c.created_at
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'certificate_id': row[0],
            'name': row[1],
            'email': row[2],
            'organization': row[3],
            'certificate_type': row[4],
            'pdf_path': row[5],
            'email_subject': row[6],
            'email_body': row[7]
        } for row in results]
    
    def update_certificate_status(self, certificate_id: int, status: str, error_message: str = None):
        """Update certificate sending status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status == 'sent':
            cursor.execute('''
            UPDATE certificates 
            SET email_status = ?, sent_at = ?, error_message = NULL
            WHERE id = ?
            ''', (status, datetime.now(), certificate_id))
        else:
            cursor.execute('''
            UPDATE certificates 
            SET email_status = ?, error_message = ?
            WHERE id = ?
            ''', (status, error_message, certificate_id))
        
        conn.commit()
        conn.close()
    
    def get_certificate_history(self, limit: int = 50) -> List[tuple]:
        """Get certificate sending history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT p.name, p.email, c.certificate_type, c.email_status, 
               c.sent_at, c.error_message
        FROM certificates c
        JOIN participants p ON c.participant_id = p.id
        ORDER BY c.created_at DESC
        LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total participants
        cursor.execute('SELECT COUNT(*) FROM participants')
        total_participants = cursor.fetchone()[0]
        
        # Total certificates
        cursor.execute('SELECT COUNT(*) FROM certificates')
        total_certificates = cursor.fetchone()[0]
        
        # Sent certificates
        cursor.execute('SELECT COUNT(*) FROM certificates WHERE email_status = "sent"')
        sent_certificates = cursor.fetchone()[0]
        
        # Pending certificates
        cursor.execute('SELECT COUNT(*) FROM certificates WHERE email_status = "pending"')
        pending_certificates = cursor.fetchone()[0]
        
        # Failed certificates
        cursor.execute('SELECT COUNT(*) FROM certificates WHERE email_status LIKE "failed%"')
        failed_certificates = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_participants': total_participants,
            'total_certificates': total_certificates,
            'sent_certificates': sent_certificates,
            'pending_certificates': pending_certificates,
            'failed_certificates': failed_certificates
        }