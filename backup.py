from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import requests
import datetime
import shutil
import os

# Google Drive Folder IDs
DRIVE_FOLDER_ID_DATABASE = "1LQPQi95MXosBrXD1MLddMoo5gtVYVn2P"
DRIVE_FOLDER_ID_MEDIA = "1ruNsHKZcJpb5nnRcDpTpRm10aVFGrBSC"

# Load Google Drive credentials
creds = Credentials.from_service_account_file(
    "credentials.json", scopes=["https://www.googleapis.com/auth/drive.file"]
)
service = build("drive", "v3", credentials=creds)

# Generate timestamped filenames
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f"db_{timestamp}.sqlite3"
backup_media_folder = f"media_backup_{timestamp}.zip"

# API endpoints for database and media backup
db_url = "https://builderspace.onrender.com/api/download-db/"
zip_url = "https://builderspace.onrender.com/api/download-media-folder/"

api_key = "Hello"

# Download database backup
db_response = requests.get(db_url, params={"key": api_key})
if db_response.status_code == 200:
    with open(backup_filename, "wb") as f:
        f.write(db_response.content)
    print(f"Database backup saved: {backup_filename}")
else:
    print(f"ERROR: Failed to download database. Status Code: {db_response.status_code}")
    print(f"Response: {db_response.text}")
    exit(1)  # Stop execution if download fails

# Download media backup
zip_response = requests.get(zip_url, params={"key": api_key})
if zip_response.status_code == 200:
    with open(backup_media_folder, "wb") as f:
        f.write(zip_response.content)
    print(f"Media backup saved: {backup_media_folder}")
else:
    print(
        f"ERROR: Failed to download media backup. Status Code: {zip_response.status_code}"
    )
    print(f"Response: {zip_response.text}")
    exit(1)  # Stop execution if download fails

# Upload database backup to Google Drive
try:
    db_metadata = {"name": backup_filename, "parents": [DRIVE_FOLDER_ID_DATABASE]}
    db_media = MediaFileUpload(backup_filename, mimetype="application/x-sqlite3")
    db_file = (
        service.files()
        .create(body=db_metadata, media_body=db_media, fields="id")
        .execute()
    )
    print(f"Database backup uploaded to Google Drive: {db_file.get('id')}")
except Exception as e:
    print(f"ERROR: Failed to upload database backup to Google Drive. {e}")
    exit(1)

# Upload media backup to Google Drive
try:
    media_metadata = {"name": backup_media_folder, "parents": [DRIVE_FOLDER_ID_MEDIA]}
    media_media = MediaFileUpload(backup_media_folder, mimetype="application/zip")
    media_file = (
        service.files()
        .create(body=media_metadata, media_body=media_media, fields="id")
        .execute()
    )
    print(f"Media backup uploaded to Google Drive: {media_file.get('id')}")
except Exception as e:
    print(f"ERROR: Failed to upload media backup to Google Drive. {e}")
    exit(1)

# Replace local database file safely
original_db = "db.sqlite3"
if os.path.exists(backup_filename) and os.path.getsize(backup_filename) > 0:
    shutil.copy(backup_filename, original_db)
    print(f"Replaced {original_db} with {backup_filename}")
else:
    print(
        f"ERROR: Backup file {backup_filename} is invalid or empty. Skipping replacement."
    )
    exit(1)
