#!/usr/bin/env bash
set -euo pipefail

echo "🪝 Installing git hooks..."

mkdir -p .git/hooks
cp privacy_guard_bundle_v1/git-hooks/pre-commit .git/hooks/pre-commit
cp privacy_guard_bundle_v1/git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-commit .git/hooks/pre-push

echo "✅ Git hooks installed."
