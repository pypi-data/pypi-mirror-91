# Merge pdf
Merge by name, all pdfs in the current folder, or specific list of files, into a single pdf file

# Install 
```bash
$ pip install merge-pdf
```

## How to use
``` python
# Import module
from merge_pdf import merge

# Path of the output pdf file
output_file = "c:\\output\\merged_files.pdf"

# Folder of the output file
output_file_folder = "c:\\output"

# Folder within have pdf files
folder_files_pdf = "c:\\pdf_files"

# List of specific pdf files
files_list = [
    "c:\\pdf_files\\01.pdf",
    "c:\\pdf_files\\02.pdf",
    "c:\\pdf_files\\03.pdf"
]

# Merge the files inside of specific folder and save in output file
merge.Merge (output_file).merge_folder (folder_files_pdf)

# Use a folder to generate the output file with the default name in this folder
merge.Merge (output_file_folder).merge_folder (folder_files_pdf)

# Merge specific list of files
merge.Merge (output_file, replace= True).merge_file_list (files_list)

# Merge files and allow replace existing file output
merge.Merge (output_file, replace=True).merge_folder (folder_files_pdf)

# Merge files and print the status of the program
merge.Merge (output_file, debug=True).merge_folder (folder_files_pdf)

```