#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <subject> <predicate> <object>"
    exit 1
fi

# Assign command-line arguments to variables
SUBJECT="$1"
PREDICATE="$2"
OBJECT="$3"

# Define the path to the Pig script
PIG_SCRIPT_PATH="/Users/varshithvattikuti/Desktop/NoSQL_PIG/update.pig"

# Define the input and output paths
INPUT_FILE="/Users/varshithvattikuti/Desktop/NoSQL_PIG/triples.txt"
OUTPUT_DIR="/Users/varshithvattikuti/Desktop/NoSQL_PIG/output"
OUTPUT_FILE="$OUTPUT_DIR/updated_triples.txt"

# Ensure the output directory exists and is empty
mkdir -p "$OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"/*

# Run the Pig script with parameters
pig -x local \
    -param new_subject="$SUBJECT" \
    -param new_predicate="$PREDICATE" \
    -param new_object="$OBJECT" \
    -f "$PIG_SCRIPT_PATH"

# Check the exit status of the Pig script
if [ $? -eq 0 ]; then
    echo "Update script executed successfully."
    # Concatenate part files into the final output file
    cat $OUTPUT_DIR/part-* > $OUTPUT_FILE
    if [ -f "$OUTPUT_FILE" ]; then
        # Move the updated file to replace the original input file
        mv "$OUTPUT_FILE" "$INPUT_FILE"
        echo "The input file has been updated successfully."
        # Cleanup output directory
        rm -rf "$OUTPUT_DIR"/*
    else
        echo "No output file was created. Please check the Pig script and output directory."
    fi
else
    echo "Failed to execute the update script."
    exit 1
fi
