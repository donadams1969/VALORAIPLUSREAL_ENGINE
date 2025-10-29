import argparse

def main():
    parser = argparse.ArgumentParser(description="Commit an irreversible action.")
    parser.add_argument("--actor", required=True, help="The actor performing the action.")
    parser.add_argument("--kind", required=True, help="The kind of action.")
    parser.add_argument("--details", required=True, help="Details of the action.")
    args = parser.parse_args()

    print(f"Committing action: actor={args.actor}, kind={args.kind}, details={args.details}")

if __name__ == "__main__":
    main()
