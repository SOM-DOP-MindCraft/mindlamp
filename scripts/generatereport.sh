#!/bin/bash

# Paths to directories
MAIN_DIR="/workspaces/mindlamp"
REPORT_DIR=
NOTEBOOK_DIR="notebooks"
OUTPUT_DIR=$MAIN_DIR/


$OUTPUT_DIR/$OUTPUT_FILE

# Path to the output HTML file
OUTPUT_FILE="TMLDNreport.html"

# Path to the notebook file
NOTEBOOK="/workspaces/mindlamp/notebooks/TMLDNreport.ipynb"


# Ensure the reports directory exists
mkdir -p $OUTPUT_DIR

# Step 1: Convert the notebook to HTML
echo "Generating HTML file from notebook..."
jupyter nbconvert --to html --TemplateExporter.exclude_input=True $NOTEBOOK --output-dir=$OUTPUT_DIR --output=$OUTPUT_FILE

# Step 2: Check if the HTML file was created
if [ -f "$OUTPUT_DIR/$OUTPUT_FILE" ]; then
    echo "HTML file generated successfully!"
else
    echo "Error generating HTML file. Exiting."
    exit 1
fi

# Step 3: Add the HTML file to Git
echo "Adding the HTML file to Git..."
git add $OUTPUT_DIR/$OUTPUT_FILE

# Step 4: Commit the change
echo "Committing the HTML file..."
git commit -m "Update HTML report"

# Step 5: Push the changes to GitHub
echo "Pushing the changes to GitHub..."
git push origin main  # or use the appropriate branch name if not 'main'

# Step 6: Confirm that everything worked
if [ $? -eq 0 ]; then
    echo "HTML file successfully pushed to GitHub!"
    cd $OUTPUT_DIR/
    python3 -m http.server 8000
else
    echo "Error pushing the changes. Exiting."
    exit 1
fi
