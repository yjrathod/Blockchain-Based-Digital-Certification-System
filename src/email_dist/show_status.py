from database_operations import DatabaseManager
import os

print("🎓 Certificate Distribution System Status")
print("=" * 50)

# Check database status
db_manager = DatabaseManager()
stats = db_manager.get_statistics()

print(f"📊 Current Statistics:")
print(f"   Total Participants: {stats['total_participants']}")
print(f"   Total Certificates: {stats['total_certificates']}")
print(f"   ✅ Sent: {stats['sent_certificates']}")
print(f"   ⏳ Pending: {stats['pending_certificates']}")
print(f"   ❌ Failed: {stats['failed_certificates']}")

print("\n📋 Pending Certificates:")
pending = db_manager.get_pending_certificates()
for i, cert in enumerate(pending, 1):
    print(f"   {i}. {cert['name']} ({cert['email']}) - {cert['certificate_type']}")
    print(f"      📄 File: {os.path.basename(cert['pdf_path'])}")

print("\n" + "=" * 50)
print("🚀 Ready to send certificates!")
print("   To send all certificates, run: python main.py")
print("   Then choose option 2: 'Send all pending certificates'")
print("\n📧 Note: Gmail OAuth authentication will be required on first run.")