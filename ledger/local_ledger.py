def commit_action(actor, kind, details):
    print(f"Committing action: {actor}, {kind}, {details}")

if __name__ == "__main__":
    commit_action("system", "test", "Initializing ledger.")
