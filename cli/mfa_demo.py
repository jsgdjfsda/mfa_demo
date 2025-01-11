import sys
import pyotp
import os
import qrcode

SECRET_FILE = "secret.key"


def register_device():
    """
    Generate a TOTP key, print the info for the user,
    and save the secret to a local file.
    """
    # Generate a random secret for TOTP
    secret = pyotp.random_base32()
    
    # Create the TOTP object
    totp = pyotp.TOTP(secret)
    
    # Here, you can provide an identifier for the user, e.g. email or username
    # Adjust the issuer_name for your application / class project
    provisioning_uri = totp.provisioning_uri(name="test_user@example.com", issuer_name="MyMFADemoApp")
    
    # Print instructions for the user
    print("=== Registering a new device ===")
    print(f"Your new TOTP secret is: {secret}")
    print("Add this secret to Google Authenticator (or scan a QR code with the provisioning URI below):")
    print(provisioning_uri)
    print("Now scanning or manually adding this key in Google Authenticator will let you generate codes.")
    
    # Save the secret to a file (not secure for real use)
    with open(SECRET_FILE, "w") as f:
        f.write(secret)
    
    print(f"\nSecret saved to {SECRET_FILE}. You can now run this script again and select 'Verify Code' to test it.\n")
    img = qrcode.make(provisioning_uri)
    img.save("mfa_qr_code.png")
    print("QR code generated and saved to 'mfa_qr_code.png'. Scan this in Google Authenticator.")

def verify_code():
    """
    Read the secret from the file, prompt for a code, and verify it.
    """
    if not os.path.exists(SECRET_FILE):
        print(f"Error: Secret file '{SECRET_FILE}' not found. Please register a device first.")
        return
    
    # Read the secret from file
    with open(SECRET_FILE, "r") as f:
        secret = f.read().strip()
    
    totp = pyotp.TOTP(secret)
    
    print("=== Verify code ===")
    user_code = input("Enter the 6-digit code from Google Authenticator: ").strip()
    
    # Verify the code
    if totp.verify(user_code):
        print("Access granted!")
    else:
        print("Access denied!")


def main():
    """
    Simple CLI to register a device or verify code.
    Usage:
        python mfa_demo.py register
        python mfa_demo.py verify
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python mfa_demo.py register   # to register a new device")
        print("  python mfa_demo.py verify     # to verify a code")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'register':
        register_device()
    elif command == 'verify':
        verify_code()
    else:
        print(f"Unknown command: {command}")
        print("Use 'register' or 'verify'.")


if __name__ == "__main__":
    main()

