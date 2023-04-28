import os
import re
import openpyxl
from PyPDF2 import PdfReader
import logging
from google_api_functs import create_drive_service
from google_api_functs import get_google_drive_link

# Suppress PyPDF2 unimportant messages about some files
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

# Path to the directory containing the resume PDFs
RESUME_DIR = 'Resumes'

# Create a new Excel workbook
wb = openpyxl.Workbook()
sheet = wb.active

# Add headers to the Excel sheet
sheet['A1'] = 'Name'
sheet['B1'] = 'Degree'
sheet['C1'] = 'filename'
opened = 0
unopened_files = 0

# Function to insert optional spaces in a string for regex
def insert_optional_spaces(s):
    return r'\s*'.join(s)

# Create Google Drive service
drive_service = create_drive_service("credentials.json")

my_folder_id = "1GkjNYfue_baOfUWXTkkp2Q5dMk8jz8-fuKBneVOTPiGPtFOFi5hlPgzWVJV83E_RDEHN_5zq"

# List of degrees to be searched in the resumes
degree_list = [
    "computer science",
    "aerospace engineering",
    "civil engineering",
    "civil and environmental",
    "computer engineering",
    "agricultural and biological engineering",
    "bioengineering",
    "chemical engineering",
    "electrical engineering",
    "engineering mechanics",
    "industrial engineering",
    "mechanical engineering",
    "material science and engineering",
    "material science engineering",
    "materials science and engineering",
    "neural engineering",
    "nuclear, plasma, and radiological engineering",
    "physics",
    "systems engineering",
    "systems engineering (?:and|&) design",
    "engineering undeclared",
    "chemical and biomolecular engineering"
]

# Create a regex pattern to match the degrees in the text
degree_patterns = '|'.join([insert_optional_spaces(d) for d in degree_list])
degree_regex = rf'(?i){degree_patterns}'

# Loop through each PDF in the directory
for filename in os.listdir(RESUME_DIR):
    if filename.endswith('.pdf'):
        filepath = os.path.join(RESUME_DIR, filename)
        
        # Read the PDF and extract text
        with open(filepath, 'rb') as f:
            pdf = PdfReader(f)
            first_page = pdf.pages[0]
            text = first_page.extract_text()

        # Extract name from filename
        name_without_ext = os.path.splitext(filename)[0]
        name_match = re.search(r'([A-Za-z][a-z-]*\s+[A-Za-z][a-z-]*)((?=\.pdf)|$)', name_without_ext, re.IGNORECASE)

        # Extract degree using regular expressions
        degree_match = re.search(degree_regex, re.sub(r'\s+', ' ', text))

        # Write name and degree to Excel sheet
        if name_match and degree_match:
                name = name_match.group(0).title()  # Convert to title case
                degree = degree_match.group(0)
                google_drive_link = get_google_drive_link(drive_service, name, folder_id = my_folder_id)
                if google_drive_link:
                    row = (name, degree, google_drive_link)
                    sheet.append(row)
                    opened += 1
                else:
                    print(f'Google Drive link not found for {filename}')
        else:
            unopened_files += 1
            if not name_match:
                print(f'name_mismatch to {filename}')
            if not degree_match:
                print(f'degree_mismatch to {filename}')

# Save the Excel file
print("opened files: " + str(opened))
print("unopened files: " + str(unopened_files))
wb.save('resume_data.xlsx')
