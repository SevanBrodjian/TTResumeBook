import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Import required libraries for Google Drive API

# Function to create a Google Drive service using credentials from a file
def create_drive_service(credentials_path):
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']  # Define the required API scope

    creds = None
    # Check if token file exists and load credentials from it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, either refresh or create new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create new credentials using the specified credentials path
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials to a JSON file
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build and return the Google Drive API service
    return build('drive', 'v3', credentials=creds)

# Function to get a Google Drive link based on a file name match and an optional folder ID
def get_google_drive_link(service, name_match, folder_id = None):
    # Build query string to search for a file containing the name match
    query = f"name contains '{name_match}'"
    if folder_id:
        query += f" and parents in '{folder_id}'"  # If folder_id is provided, add it to the query

    # Execute the API request using the query and retrieve file data
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get("files", [])

    # If no matching files are found, return None
    if not items:
        return None
    else:
        # Iterate through the matching files and return the webViewLink of the first one with a matching name
        for item in items:
            if name_match.lower() in item["name"].lower():
                return item["webViewLink"]

        # Print the name match and the item's lowercased name for debugging purposes
        print(name_match)
        print(item["name"].lower())

    return None
