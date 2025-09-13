import csv
import os
from database_operations import DatabaseManager

def test_import_participants_from_csv(csv_path, certificate_path, certificate_type="Certificate"):
    """Test import participants from CSV without sending emails"""
    
    # Initialize database manager only (no email service)
    db_manager = DatabaseManager()
    
    # Verify certificate file exists
    if not os.path.exists(certificate_path):
        print(f"❌ Certificate file not found: {certificate_path}")
        return False
    
    # Verify CSV file exists
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    print(f"🧪 TEST MODE: Importing participants from: {csv_path}")
    print(f"📄 Certificate file: {certificate_path}")
    print(f"🎓 Certificate type: {certificate_type}")
    print("=" * 50)
    
    imported_count = 0
    failed_count = 0
    
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Try to detect if the CSV has headers
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(sample)
            
            if has_header:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
            else:
                reader = csv.reader(csvfile)
                rows = list(reader)
            
            for row_num, row in enumerate(rows, 1):
                try:
                    if has_header:
                        # Handle different possible column names
                        name = row.get('Name') or row.get('name') or row.get('NAME')
                        email = row.get('Email') or row.get('email') or row.get('EMAIL')
                        organization = row.get('Organization') or row.get('organization') or row.get('ORGANIZATION') or None
                    else:
                        # Assume first column is name, second is email
                        if len(row) >= 2:
                            name = row[0].strip()
                            email = row[1].strip()
                            organization = row[2].strip() if len(row) > 2 else None
                        else:
                            print(f"❌ Row {row_num}: Insufficient columns")
                            failed_count += 1
                            continue
                    
                    if not name or not email:
                        print(f"❌ Row {row_num}: Missing name or email")
                        failed_count += 1
                        continue
                    
                    # Add participant
                    participant_id = db_manager.add_participant(
                        name=name.strip(),
                        email=email.strip(),
                        organization=organization.strip() if organization else None
                    )
                    
                    if participant_id:
                        # Create email content
                        subject = f"Your {certificate_type} Certificate"
                        body = f"""Dear {name},

Congratulations! 🎉

We are pleased to present you with your {certificate_type} certificate attached to this email.

Thank you for your participation and dedication.

Best regards,
Certificate Team"""
                        
                        # Add certificate record
                        cert_id = db_manager.add_certificate_record(
                            participant_id, certificate_type, certificate_path, subject, body
                        )
                        
                        print(f"✅ Added: {name} ({email}) - Certificate ID: {cert_id}")
                        imported_count += 1
                    else:
                        print(f"❌ Row {row_num}: Failed to add participant {name}")
                        failed_count += 1
                    
                except Exception as e:
                    print(f"❌ Row {row_num}: Error processing {row} - {str(e)}")
                    failed_count += 1
                    continue
    
    except Exception as e:
        print(f"❌ Error reading CSV file: {str(e)}")
        return False
    
    print("=" * 50)
    print(f"📊 Import Summary:")
    print(f"   ✅ Successfully imported: {imported_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📧 Total certificates in queue: {imported_count}")
    
    # Show database statistics
    stats = db_manager.get_statistics()
    print(f"\n📊 Database Statistics:")
    print(f"   Total Participants: {stats['total_participants']}")
    print(f"   Total Certificates: {stats['total_certificates']}")
    print(f"   ✅ Sent: {stats['sent_certificates']}")
    print(f"   ⏳ Pending: {stats['pending_certificates']}")
    print(f"   ❌ Failed: {stats['failed_certificates']}")
    
    return imported_count > 0

if __name__ == "__main__":
    # Test with your provided files
    csv_file = r"K:\Programmer Kishan\Hackathon\participants.csv"
    cert_file = r"K:\Programmer Kishan\Hackathon\Test.pptx"
    cert_type = "Hackathon Completion Certificate"
    
    success = test_import_participants_from_csv(csv_file, cert_file, cert_type)
    
    if success:
        print("\n🎉 Test import completed successfully!")
        print("📧 To send emails, you need to:")
        print("   1. Complete Gmail OAuth authentication")
        print("   2. Run: python main.py")
        print("   3. Choose option 2: 'Send all pending certificates'")
    else:
        print("\n❌ Test import failed!")