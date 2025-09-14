import os

def main():
    print("Select an option:")
    print("1. Run Admin Dashboard")
    print("2. Run Validation Portal")
    print("3. Generate Certificates")
    print("4. Send Certificates (Email)")
    choice = input("Enter choice: ")
    if choice == "1":
        os.system("python src/dashboard/app.py")
    elif choice == "2":
        os.system("python src/validation_portal/app.py")
    elif choice == "3":
        os.system("python src/cert_gen/generate_certs.py")
    elif choice == "4":
        os.system("python src/email_dist/main.py")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()