import os
import subprocess
import time
import shutil

ganache_process = None

def start_blockchain():
    global ganache_process
    if ganache_process is None or ganache_process.poll() is not None:
        # Detect whether 'ganache' or 'ganache-cli' is installed
        ganache_cmd = shutil.which("ganache") or shutil.which("ganache-cli")

        if not ganache_cmd:
            print("❌ Ganache is not installed or not in PATH.")
            print("👉 Install it with: npm install -g ganache")
            return

        ganache_process = subprocess.Popen(
            [ganache_cmd, "--deterministic"],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        print("⏳ Starting blockchain (Ganache)...")
        time.sleep(3)  # wait for it to be ready
        print("✅ Blockchain started")

def stop_blockchain():
    global ganache_process
    if ganache_process:
        ganache_process.terminate()
        ganache_process = None
        print("🛑 Blockchain stopped")

def main():
    while True:
        print("\nSelect an option:")
        print("1. Run Admin Dashboard")
        print("2. Run Validation Portal")
        print("3. Generate Certificates")
        print("4. Send Certificates (Email)")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            start_blockchain()
            os.system("python src/dashboard/app.py")
        elif choice == "2":
            start_blockchain()
            os.system("python src/validation_portal/app.py")
        elif choice == "3":
            start_blockchain()
            os.system("python src/cert_gen/generate_certs.py")
        elif choice == "4":
            start_blockchain()
            os.system("python src/email_dist/main.py")
        elif choice == "5":
            stop_blockchain()
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
