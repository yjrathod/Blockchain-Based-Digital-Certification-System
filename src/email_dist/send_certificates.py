#!/usr/bin/env python3
"""
Send All Pending Certificates
This script sends all pending certificates in the database.
"""

from certificate_distributor import CertificateDistributor

def main():
    print("📧 Certificate Distribution System")
    print("=" * 50)
    
    # Initialize distributor
    distributor = CertificateDistributor()
    
    # Show current status
    print("\n📊 Current Status:")
    distributor.show_statistics()
    
    # Ask for confirmation
    print("\n" + "=" * 50)
    choice = input("🚀 Send all pending certificates? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        print("\n📬 Starting certificate distribution...")
        results = distributor.send_all_pending()
        
        print(f"\n🎉 Distribution completed!")
        print(f"   ✅ Successfully sent: {results['sent']}")
        print(f"   ❌ Failed: {results['failed']}")
        print(f"   📊 Total processed: {results['total']}")
        
        # Show updated statistics
        print(f"\n📊 Final Statistics:")
        distributor.show_statistics()
        
    else:
        print("❌ Certificate distribution cancelled.")

if __name__ == "__main__":
    main()