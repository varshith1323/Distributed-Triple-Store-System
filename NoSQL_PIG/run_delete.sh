#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <subject> <predicate>"
    exit 1
fi

# Assign command-line arguments to variables
subject=$1
prdicate=$2

# Define the path to the Pig script
PIG_SCRIPT_PATH="//Users/varshithvattikuti/Desktop/NoSQL_PIG/delete.pig"

# Define the input and output paths
INPUT_FILE="/Users/varshithvattikuti/Desktop/NoSQL_PIG/triples.txt"
OUTPUT_DIR="/Users/varshithvattikuti/Desktop/NoSQL_PIG/output"
OUTPUT_FILE="$OUTPUT_DIR/deleted_triples.txt"

# Ensure the output directory exists and is empty
mkdir -p "$OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"/*
echo "subject: $subject"
echo "predicate: $predicate"

# Run the Pig script with parameters
pig -x local \
    -param delete_subject="$subject" \
    -param delete_predicate="$predicate" \
    -f "$PIG_SCRIPT_PATH"

# Check the exit status of the Pig script
if [ $? -eq 0 ]; then
    echo "Delete script executed successfully."
    # Ensure the output directory is not empty
    if [ "$(ls -A $OUTPUT_DIR)" ]; then
        cat $OUTPUT_DIR/part-* > "$OUTPUT_FILE"
        # Move the updated file to replace the original input file
        if [ -f "$OUTPUT_FILE" ]; then
            mv "$OUTPUT_FILE" "$INPUT_FILE"
            echo "The input file has been updated successfully."
            rm -rf "$OUTPUT_DIR"/*
        else
            echo "No output file was created. Please check the Pig script and output directory."
        fi
    else
        echo "No output file was created. Please check the Pig script and output directory."
    fi
else
    echo "Failed to execute the delete script."
    exit 1
fi

