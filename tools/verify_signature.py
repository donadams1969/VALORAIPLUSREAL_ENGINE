import argparse
import sys
import ed25519

# ANSI color codes for clear terminal feedback
class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def verify_signature(public_key_path, signature_path, data_path):
    """
    Verifies an Ed25519 signature of a file against a public key.

    This function provides a clear, step-by-step output to the terminal,
    making the verification process transparent to the user.

    Args:
        public_key_path (str): The path to the public key file.
        signature_path (str): The path to the signature file.
        data_path (str): The path to the original data file (e.g., the manifest).

    Returns:
        bool: True if verification is successful, False otherwise.
    """
    print(f"{colors.BOLD}VALORAIPLUS2E Artifact Verification{colors.ENDC}")
    print("=" * 40)
    print(f" ▸ Loading Public Key:  {public_key_path}")
    print(f" ▸ Loading Data File:   {data_path}")
    print(f" ▸ Loading Signature:   {signature_path}")
    print("-" * 40)

    try:
        # 1. Read the public key from the file
        with open(public_key_path, 'rb') as f:
            public_key_hex = f.read()
            verifying_key = ed25519.VerifyingKey(public_key_hex)
        print("   - Public key loaded successfully.")

        # 2. Read the signature from the file
        with open(signature_path, 'rb') as f:
            signature = f.read()
        print("   - Signature loaded successfully.")

        # 3. Read the data that was signed (the manifest)
        with open(data_path, 'rb') as f:
            data = f.read()
        print("   - Data file loaded successfully.")

        # 4. Perform the cryptographic verification
        print("\nAttempting cryptographic verification...")
        verifying_key.verify(signature, data)

        print(f"\n{colors.OKGREEN}{colors.BOLD}✅ VERIFICATION SUCCESSFUL{colors.ENDC}")
        print("   The signature is valid and the manifest has not been tampered with.")
        return True

    except ed25519.BadSignatureError:
        print(f"\n{colors.FAIL}{colors.BOLD}❌ VERIFICATION FAILED: INVALID SIGNATURE{colors.ENDC}")
        print("   The signature does not match the file and public key.")
        print("   Reason: The file may have been altered, or the wrong key/signature was used.")
        return False
    except FileNotFoundError as e:
        print(f"\n{colors.FAIL}{colors.BOLD}❌ ERROR: FILE NOT FOUND{colors.ENDC}")
        print(f"   The file '{e.filename}' could not be found.")
        return False
    except Exception as e:
        print(f"\n{colors.FAIL}{colors.BOLD}❌ An unexpected error occurred: {e}{colors.ENDC}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="A modular tool to verify the Ed25519 signature of a manifest file. Conforms to the VALORAIPLUS2E attestation discipline.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--key', required=True, help='Path to the public key file (e.g., keys/signing.pub).')
    parser.add_argument('--signature', required=True, help='Path to the signature file (e.g., artifacts/MANIFEST_SHA256.txt.sig).')
    parser.add_argument('--file', required=True, help='Path to the data file that was signed (e.g., artifacts/MANIFEST_SHA256.txt).')

    args = parser.parse_args()

    # Exit with a non-zero status code on failure, which is standard practice for CLI tools
    if not verify_signature(args.key, args.signature, args.file):
        sys.exit(1)

if __name__ == "__main__":
    main()
