# Form Backup Program

A simple Python script to back up form data from a CSV export. It supports handling European characters and outputs detailed reports in both CSV and text formats.

## Features
- Backs up forms listed in a CSV export file from the MoveON platform.
- Handles directories with spaces and special characters.
- Provides a detailed report on backed-up and skipped forms.
- Outputs a statistical summary of the backup process.

## Requirements
- Python 3.x
- Required Python libraries:
  - `pandas`
  - `tk`
  - `requests`
  - `tqdm`

## Installation
1. Ensure you have Python 3 installed on your system. If not, download and install it from the [official Python website](https://www.python.org/).
2. Install the required dependencies by running the following command in your terminal/command prompt:
   ```sh
   pip install pandas requests tqdm
   ```

## How to Run the Program
1. Download the script file and save it on your computer.
2. Open your terminal (or command prompt).
3. Navigate to the directory where the script file is saved using the `cd` command.
4. Run the script by typing:
   ```sh
   python backupper.py
   ```

## Using the Program
1. **Select CSV Export File**:
   - A file dialog will appear prompting you to select your CSV export file.
2. **Enter MoveON Back Office URL**:
   - You will be prompted to enter your MoveON back office URL. Copy and paste your URL into the input dialog.
3. **Select Backup Directory**:
   - A folder dialog will appear prompting you to select a directory to save the backups. Navigate to and select your desired backup location (e.g., Downloads folder).

### Output
- **form_backup_report.csv**:
  - A semicolon-separated CSV file listing all forms with columns: `Form name` and `Backed up` (with values `Yes` or `No`).
- **stats_report.txt**:
  - A text file containing the process summary, including the number of backed-up forms, skipped forms, total forms, and the start and end times of the process.

## Example
If everything runs smoothly, you will see a progress bar indicating the status of the backup process. Once completed, you will find the `form_backup_report.csv` and `stats_report.txt` files in the selected backup directory.

## Troubleshooting
- **CSV File Not Opening**:
  - Ensure the CSV file is correctly formatted and encoded in UTF-16.
- **Network Errors**:
  - Check your internet connection if files fail to download.
- **Permission Issues**:
  - Ensure you have the necessary permissions to read the CSV file and write to the backup directory.

Happy Backing Up!
