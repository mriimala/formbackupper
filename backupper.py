import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog
import requests
from datetime import datetime
import hashlib
import io
from tqdm import tqdm

# Helper function to get the user's Downloads folder
def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Initialize Tkinter for file dialogs
root = tk.Tk()
root.withdraw()  # Hide the root window

# Set the initial directory to the user's Downloads folder
initial_dir = get_downloads_folder()

# Ask the user to select a CSV file containing list of MoveON forms
form_view_export_csv = filedialog.askopenfilename(
    title="Select your Forms default view's export.csv",
    initialdir=initial_dir,
    filetypes=(("CSV files", "*.csv"),)
)

# Read the CSV file with custom handling for line terminators and correct encoding
try:
    with open(form_view_export_csv, 'r', encoding='utf-16') as file:
        content = file.read().replace('\n', '\r\n')
    csv_table = pd.read_csv(io.StringIO(content), sep='\t', encoding='utf-16')
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Ask the user for the MoveON back office URL
back_office_url = simpledialog.askstring(
    title="MoveON backoffice URL",
    prompt="Copy your MoveON back office URL here:"
)

# Ask the user to choose a directory for saving the backup
selected_folder = filedialog.askdirectory(
    title="Select your backup directory",
    initialdir=initial_dir
)

# Note the start time of the process
start_time = datetime.now()

# Initialize counters for tracking backed-up, skipped, and total forms
form_count = 0
skipped_count = 0
total_count = 0

# Initialize a list to collect report data
report_data = []

# Use tqdm to create a progress bar
for index, form_row in tqdm(csv_table.iterrows(), total=len(csv_table), desc="Processing forms"):
    total_count += 1
    form_name = "".join(c for c in form_row.iloc[0] if c not in r'\/:*?"<>|').strip()  # Sanitize the form name
    form_url = form_row.iloc[1]
    is_active = form_row.iloc[2]

    if is_active == "No":
        # Add to report data as skipped
        report_data.append({"Form name": form_name, "Backed up": "No"})
        skipped_count += 1
    elif is_active == "Yes":
        form_folder_path = os.path.join(selected_folder, form_name)
        
        # Attempt to create a directory for the form, handle any errors
        try:
            os.makedirs(form_folder_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {form_folder_path}: {e}")
            continue  # Skip this form and move on to the next

        # Extract the Form ID from the URL
        form_id = form_url.split('form/')[1].split('/eng')[0]

        # Define URLs for each file type and their respective save paths
        file_urls = {
            "form_xml": os.path.join(form_folder_path, f"{form_name}_definition.xml"),
            "form_translation": os.path.join(form_folder_path, f"{form_name}_translation.xml"),
            "form_css": os.path.join(form_folder_path, f"{form_name}_form.css"),
            "form_pdf_css": os.path.join(form_folder_path, f"{form_name}_pdf.css"),
            "form_import_xslt": os.path.join(form_folder_path, f"{form_name}_import.xslt"),
        }

        moveon_file_path = f"{back_office_url}download/viewfile/form_id/{form_id}/control/"

        # Download each file if it doesn't already exist and isn't identical
        for file_key, file_path in file_urls.items():
            url = f"{moveon_file_path}{file_key}"
            try:
                if os.path.exists(file_path):
                    existing_file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                    response = requests.get(url, allow_redirects=True)
                    new_file_hash = hashlib.md5(response.content).hexdigest()
                    if existing_file_hash == new_file_hash:
                        continue
                else:
                    response = requests.get(url, allow_redirects=True)
                    with open(os.path.normpath(file_path), 'wb') as file:
                        file.write(response.content)
            except Exception as e:
                print(f"Error downloading file {url}: {e}")
                continue  # Skip this file and move on to the next

        # Add to report data as backed up
        report_data.append({"Form name": form_name, "Backed up": "Yes"})
        
        form_count += 1

# Note the end time of the process
end_time = datetime.now()

# Calculate the duration of the backup process
time_difference = int((end_time - start_time).total_seconds())

# Save the combined report as a semicolon-separated CSV file with UTF-8 encoding
report_df = pd.DataFrame(report_data)
report_df.to_csv(os.path.join(selected_folder, "form_backup_report.csv"), index=False, sep=';', encoding='utf-8-sig')

# Create the stats report content
stats_report_content = f"""Process started: {start_time.replace(microsecond=0)}
Process completed: {end_time.replace(microsecond=0)}
Process duration: {time_difference} seconds

Backed up {form_count} forms
Skipped {skipped_count} inactive forms
Total forms {total_count}
"""

# Save the stats report to a text file with UTF-8 encoding
with open(os.path.join(selected_folder, "stats_report.txt"), 'w', encoding='utf-8') as stats_report_file:
    stats_report_file.write(stats_report_content)
