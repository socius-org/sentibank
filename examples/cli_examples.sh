#!/bin/bash
# CLI Examples for Sentibank
# Make sure sentibank is installed: pip install sentibank

echo "🏦 Sentibank CLI Examples"
echo "========================"

# 1. List available dictionaries
echo -e "\n1. Listing available dictionaries:"
sentibank list

echo -e "\n2. Listing dictionaries and origins:"
sentibank list --origins

# 3. Analyze sentiment of text
echo -e "\n3. Analyzing sentiment:"
sentibank analyze VADER_v2014 "I love this product! It's amazing!"

echo -e "\n4. Analyzing negative sentiment:"
sentibank analyze VADER_v2014 "This is terrible and disappointing."

# 5. Analyze with JSON output
echo -e "\n5. JSON output format:"
sentibank analyze VADER_v2014 "Great product, highly recommended!" --json

# 6. Analyze text from file
echo -e "\n6. Creating sample text file:"
echo "This is an amazing product with excellent quality. I highly recommend it to everyone!" > sample_text.txt

echo "Analyzing text from file:"
sentibank analyze VADER_v2014 --file sample_text.txt

# 7. Show dictionary information
echo -e "\n7. Dictionary information:"
sentibank info VADER_v2014

# 8. Export dictionary
echo -e "\n8. Exporting dictionary to JSON:"
sentibank export VADER_v2014 --format json --output vader_exported.json
echo "Exported dictionary to vader_exported.json"

echo -e "\n9. Export to CSV format:"
sentibank export AFINN_v2015 --format csv --output afinn_exported.csv
echo "Exported dictionary to afinn_exported.csv"

# Clean up
echo -e "\n🧹 Cleaning up example files:"
rm -f sample_text.txt vader_exported.json afinn_exported.csv

echo -e "\n✅ CLI examples completed!"
echo "For more information, run: sentibank --help"