#!/bin/bash

# Description: This script cleans LaTeX files, processes bibliography files, and updates bibliography references in a .tex file.
# It is compatible with both macOS and Linux systems.

# Define directory and file names
dirname="xTower"
dirname_arxiv="${dirname}_arXiv"
main_tex_file="acl_latex"

# Step 1: Clean LaTeX files
# Using arxiv_latex_cleaner to clean LaTeX files, keeping bibliography and using a specific configuration
echo "Cleaning latex files"
arxiv_latex_cleaner ${dirname}/ --keep_bib --config cleaner_config.yaml 

# Step 2: Clean anthology.bib
# Running a Python script to remove unused bibliographies and output a cleaned .bib file
echo "Cleaning anthology.bib, transforming into anthology_small.bib"
python3 removed_unused_bibs.py \
    -b ${dirname_arxiv}/anthology.bib \
    -p ${dirname_arxiv}/${main_tex_file}.tex \
    -o ${dirname_arxiv}/anthology_small.bib

# Step 3. Remove the big anthology.bib
echo "Removing anthology.bib"
rm ${dirname_arxiv}/anthology.bib

# Step 4: Rename the main .tex file
# Renaming the main LaTeX file for consistency
echo "Renaming ${main_tex_file}.tex to main.tex"
mv ${dirname_arxiv}/${main_tex_file}.tex ${dirname_arxiv}/main.tex

# Step 5: Update bibliography reference in the .tex file
# Replacing "anthology" with "anthology_small" within the \bibliography command in the main .tex file
echo "Replacing anthology by anthology_small in ${dirname_arxiv}/main.tex"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' -e '/\\bibliography{[^}]*anthology[^}]*}/s/anthology/anthology_small/g' ${dirname_arxiv}/main.tex
else
    # Linux and other UNIX-like OS
    sed -i -e '/\\bibliography{[^}]*anthology[^}]*}/s/anthology/anthology_small/g' ${dirname_arxiv}/main.tex
fi

# Final step: Instructions for the user
# Remind the user to handle the output.bbl file appropriately
echo -e "MAKE SURE TO: \n 1. GET THE 'output.bbl' FILE; \n 2. RENAME IT TO 'main.bbl'; \n 3. PLACE IT INSIDE ${dirname_arxiv}/"

# End of script
