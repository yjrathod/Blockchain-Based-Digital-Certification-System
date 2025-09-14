from database_operations import DatabaseManager

db = DatabaseManager()
pending = db.get_pending_certificates()

print(f"📋 Pending certificates: {len(pending)}")
for i, cert in enumerate(pending):
    print(f"{i+1}. {cert['name']} - {cert['email']}")

stats = db.get_statistics()
print(f"\n📊 Statistics:")
print(f"Total participants: {stats['total_participants']}")
print(f"Total certificates: {stats['total_certificates']}")
print(f"Pending: {stats['pending_certificates']}")