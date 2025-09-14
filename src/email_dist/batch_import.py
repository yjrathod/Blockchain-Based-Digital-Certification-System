import csv
import os
from certificate_distributor import CertificateDistributor

def import_participants_from_csv(csv_path, certificate_path, certificate_type="Certificate"):
    """Import participants from CSV and add certificates to queue"""
    
    # Initialize distributor
    distributor = CertificateDistributor()
    
    # Verify certificate file exists
    if not os.path.exists(certificate_path):
        print(f"❌ Certificate file not found: {certificate_path}")
        return False
    
    # Verify CSV file exists
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    print(f"📋 Importing participants from: {csv_path}")
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
            
            reader = csv.DictReader(csvfile) if has_header else csv.reader(csvfile)
            
            for row_num, row in enumerate(reader, 1):
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
                    
                    # Add certificate to queue
                    cert_id = distributor.add_certificate_to_queue(
                        name=name.strip(),
                        email=email.strip(),
                        certificate_type=certificate_type,
                        pdf_path=certificate_path,
                        organization=organization.strip() if organization else None
                    )
                    
                    print(f"✅ Added: {name} ({email}) - Certificate ID: {cert_id}")
                    imported_count += 1
                    
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
    
    return imported_count > 0

if __name__ == "__main__":
    # Example usage
    csv_file = input("Enter CSV file path: ").strip()
    cert_file = input("Enter certificate file path: ").strip()
    cert_type = input("Enter certificate type (default: 'Certificate'): ").strip() or "Certificate"
    
    success = import_participants_from_csv(csv_file, cert_file, cert_type)
    
    if success:
        print("\n🎉 Import completed!")
        choice = input("Do you want to send all certificates now? (y/n): ").strip().lower()
        if choice == 'y':
            distributor = CertificateDistributor()
            distributor.send_all_pending()
    else:
        print("\n❌ Import failed!")