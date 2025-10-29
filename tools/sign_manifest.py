def sign_manifest(keys, manifest, out):
    print(f"Signing manifest '{manifest}' with keys from '{keys}' to '{out}'")

if __name__ == "__main__":
    sign_manifest("keys", "artifacts/MANIFEST_SHA256.txt", "artifacts")
