#!/bin/bash

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -b|--base64)
            BASE64_DECODED_STRING="$2"
            shift 2
            ;;
        -s|--suffix)
            SUFFIX="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check if the Base64 string is provided
if [ -z "$BASE64_DECODED_STRING" ]; then
    echo "Base64 Decoded string not provided."
    exit 1
fi

# Check if the suffix is provided; if not, use a default value
if [ -z "$SUFFIX" ]; then
    SUFFIX=".txt"
fi

# Create a temporary file with the specified suffix
TEMP_FILE=$(mktemp --suffix="$SUFFIX")

# Decode the Base64 string and store it in the temporary file
echo "$BASE64_DECODED_STRING" > "$TEMP_FILE"

# Open the temporary file in Vim
vim "$TEMP_FILE"

# Optionally, remove the temporary file after Vim is closed
rm "$TEMP_FILE"
