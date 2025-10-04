# Inventory Manager
A simple Python application for managing inventory using Google Sheets.  
The application provides a graphical interface built with Tkinter to add, update, and remove item quantities directly from a Google Sheet.

## Features
- View current inventory from a Google Sheet
- Add new items or update quantities of existing items
- Remove quantities of items
- Simple and user-friendly GUI (Tkinter)

## Technologies Used
- Python 3
- Tkinter
- gspread
- Google Sheets API

## Requirements
- Python 3.10 or higher
- Google Cloud project with Google Sheets and Google Drive APIs enabled
- A Google service account and credentials file (`credentials.json`)

## Installation
1. Clone the repository:
git clone https://github.com/neliobarbosa/inventory-manager.git
cd inventory-manager

Install dependencies:

pip install -r requirements.txt
Place your credentials.json file in the same folder as the program.

Run the program:

python inventory_manager.py
Google Sheets API setup (step-by-step)
Follow these steps to create a Google Cloud service account, enable the APIs, generate the credentials.json file and give it access to your Google Sheet.

1. Create a project in Google Cloud Console
Open https://console.cloud.google.com/

Click Select a project → New Project.

Give it a name (for example inventory-manager) and click Create.

2. Enable APIs
With the project selected, go to APIs & Services → Library.

Search for Google Sheets API and click Enable.

Also search for Google Drive API and click Enable.

gspread uses the Drive API for some operations, so enable both.

3. Create a service account and download the JSON key
Go to APIs & Services → Credentials.

Click Create credentials → Service account.

Fill a name (e.g. inventory-bot) and click Create → Done.

In the Service accounts list (or via IAM & Admin → Service accounts), find your service account.

Click the three dots (⋮) at the right and choose Manage keys (or open the service account, then the Keys tab).

Click Add Key → Create new key → choose JSON → Create.

A file will be downloaded (something like project-xxxxx-xxxx.json).

Rename it to credentials.json (optional) and move it into your project folder (but do not commit it to GitHub).

4. Share the Google Sheet with the service account
Create a Google Sheet (or open an existing one) in Google Sheets.

Click Share (top-right).

Open the downloaded credentials.json in a text editor and copy the value of "client_email", for example:

json
"client_email": "inventory-bot@project-123456.iam.gserviceaccount.com"
Paste that email into the Share dialog and give Editor permission. Click Send (or Save).

5. Sheet structure and name
The program expects the sheet headers in the first row to be exactly:

mathematica
Item | Quantity
Put each product on a separate row below the header, e.g.:

nginx
Shampoo | 10
Soap    | 5
The program opens the sheet by name "PlanilhaLar" by default. You can:

Rename your Google Sheet to PlanilhaLar, or

Edit the Python file and change the sheet-open line:

python
sheet = client.open("YourSheetNameHere").sheet1
6. Security notes
Do not commit credentials.json to GitHub or share it publicly. It contains private keys granting access to your Google resources.
Add credentials.json to your .gitignore:

pgsql
credentials.json
If you accidentally publish the JSON, revoke the key immediately in Google Cloud Console and create a new one.

Creating an executable (optional)
To create a single Windows executable with the credentials embedded (not recommended for public distribution of keys), use:

bash
pyinstaller --onefile --noconsole --add-data "credentials.json;." inventory_manager.py
Note: embedding credentials in an exe still leaves the secret in the distributed file; keep security in mind.

Notes
The credentials.json file is not included in this repository for security reasons. You need to generate your own from the Google Cloud Console.

Contributing
Feel free to contribute with improvements to the interface, new features, or bug fixes.

Author
Nélio Barbosa
