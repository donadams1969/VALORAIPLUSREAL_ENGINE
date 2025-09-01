import argparse
import sys
import ed25519

# ANSI color codes for terminal output
class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def verify_signature(public_key_path, signature_path, data_path):
    """
    Verifies an Ed25519 signature of a file.

    Args:
        public_key_path (str): The path to the public key file.
        signature_path (str): The path to the signature file.
        data_path (str): The path to the original data file (e.g., the manifest).

    Returns:
        bool: True if verification is successful, False otherwise.
    """
    print(f"{colors.BOLD}Running verification...{colors.ENDC}")
    print(f"  - Public Key: {public_key_path}")
    print(f"  - Data File:  {data_path}")
    print(f"  - Signature:  {signature_path}")
    print("-" * 30)

    try:
        # Read the public key, signature, and data from their respective files
        with open(public_key_path, 'rb') as f:
            public_key_hex = f.read()
            verifying_key = ed25519.VerifyingKey(public_key_hex)

        with open(signature_path, 'rb') as f:
            signature = f.read()

        with open(data_path, 'rb') as f:
            data = f.read()

        # Perform the verification
        verifying_key.verify(signature, data)

        print(f"{colors.OKGREEN}✅ VERIFICATION SUCCESSFUL:{colors.ENDC} The signature is valid and the file has not been tampered with.")
        return True

    except ed25519.BadSignatureError:
        print(f"{colors.FAIL}❌ VERIFICATION FAILED:{colors.ENDC} The signature is invalid. The file may have been tampered with or the wrong key was used.")
        return False
    except FileNotFoundError as e:
        print(f"{colors.FAIL}❌ ERROR:{colors.ENDC} File not found: {e.filename}")
        return False
    except Exception as e:
        print(f"{colors.FAIL}❌ An unexpected error occurred: {e}{colors.ENDC}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Verify an Ed25519 signature for a given file. This is a modular tool for third-party verification.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--key', required=True, help='Path to the public key file (e.g., keys/signing.pub).')
    parser.add_argument('--signature', required=True, help='Path to the signature file (e.g., artifacts/MANIFEST_SHA256.txt.sig).')
    parser.add_argument('--file', required=True, help='Path to the file that was signed (e.g., artifacts/MANIFEST_SHA256.txt).')

    args = parser.parse_args()

    if not verify_signature(args.key, args.signature, args.file):
        sys.exit(1) # Exit with a non-zero code to indicate failure, useful for scripting

if __name__ == "__main__":
    main()
