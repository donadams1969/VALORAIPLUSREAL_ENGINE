# scripts/quarterly-drill.sh
trufflehog git file://$(pwd) --json > full-scan.json
node scripts/analyze-drill.js # Simulate incidents, test response
