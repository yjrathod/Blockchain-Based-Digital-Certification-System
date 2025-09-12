from database_setup import create_database
from certificate_distributor import CertificateDistributor
import os

def main():
    print("🎓 Certificate Distribution System")
    print("=" * 50)
    
    # Initialize database
    if not os.path.exists('certificates.db'):
        print("Setting up database...")
        create_database()
    
    # Initialize distributor
    distributor = CertificateDistributor()
    
    # Test Gmail connection
    success, result = distributor.email_service.test_connection()
    if not success:
        print("❌ Gmail connection failed. Please check your credentials.")
        return
    
    while True:
        print("\n" + "=" * 50)
        print("📋 Choose an option:")
        print("1. Add certificate to queue")
        print("2. Send all pending certificates")
        print("3. View statistics")
        print("4. View recent history")
        print("5. Test email connection")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            add_certificate_interactive(distributor)
        elif choice == '2':
            distributor.send_all_pending()
        elif choice == '3':
            distributor.show_statistics()
        elif choice == '4':
            distributor.show_recent_history()
        elif choice == '5':
            distributor.email_service.test_connection()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def add_certificate_interactive(distributor):
    """Interactive function to add certificates"""
    print("\n📝 Add New Certificate")
    print("-" * 30)
    
    name = input("Recipient Name: ").strip()
    email = input("Recipient Email: ").strip()
    certificate_type = input("Certificate Type (e.g., 'Completion Certificate'): ").strip()
    
    # Show available PDF files
    if os.path.exists('certificates'):
        pdf_files = [f for f in os.listdir('certificates') if f.lower().endswith('.pdf')]
        if pdf_files:
            print("\n📄 Available PDF files:")
            for i, file in enumerate(pdf_files, 1):
                print(f"   {i}. {file}")
            
            try:
                file_choice = int(input("Select PDF file number: ")) - 1
                if 0 <= file_choice < len(pdf_files):
                    pdf_path = os.path.join('certificates', pdf_files[file_choice])
                else:
                    pdf_path = input("Or enter full PDF path: ").strip()
            except ValueError:
                pdf_path = input("Enter PDF file path: ").strip()
        else:
            print("📁 No PDF files found in 'certificates' folder")
            pdf_path = input("Enter full PDF file path: ").strip()
    else:
        pdf_path = input("Enter PDF file path: ").strip()
    
    organization = input("Organization (optional): ").strip() or None
    
    try:
        cert_id = distributor.add_certificate_to_queue(
            name, email, certificate_type, pdf_path, organization
        )
        print(f"✅ Certificate added with ID: {cert_id}")
        
        send_now = input("Send immediately? (y/n): ").strip().lower()
        if send_now == 'y':
            distributor.send_single_certificate(cert_id)
            
    except Exception as e:
        print(f"❌ Error adding certificate: {str(e)}")

if __name__ == "__main__":
    main()