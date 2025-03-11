from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import requests
import datetime
import shutil
import os

DRIVE_FOLDER_ID_DATABASE = "1LQPQi95MXosBrXD1MLddMoo5gtVYVn2P"

DRIVE_FOLDER_ID_MEDIA = "1ruNsHKZcJpb5nnRcDpTpRm10aVFGrBSC"

creds = Credentials.from_service_account_file(
    "credentials.json", scopes=["https://www.googleapis.com/auth/drive.file"]
)
service = build("drive", "v3", credentials=creds)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

backup_filename = f"db_{timestamp}.sqlite3"
backup_media_folder = f"media_backup_{timestamp}.zip"

db_url = "https://builderspace.onrender.com/api/download-db/"
db_response = requests.get(db_url, params={"key": os.environ.get("BUILDERSSPACE_KEY")})

zip_url = "https://builderspace.onrender.com/download-media-folder/"
zip_response = requests.get(
    zip_url, params={"key": os.environ.get("BUILDERSSPACE_KEY")}
)

with open(backup_filename, "wb") as f:
    f.write(db_response.content)

with open(backup_media_folder, "wb") as f:
    f.write(zip_response.content)


db_metadata = {"name": backup_filename, "parents": [DRIVE_FOLDER_ID_DATABASE]}
db_media = MediaFileUpload(backup_filename, mimetype="application/x-sqlite3")
db_file = (
    service.files().create(body=db_metadata, media_body=db_media, fields="id").execute()
)

print(f"Backup uploaded to Google Drive: {db_file.get('id')}")

# Upload the ZIP file to Google Drive
media_metadata = {"name": backup_media_folder, "parents": [DRIVE_FOLDER_ID_MEDIA]}
media_media = MediaFileUpload(backup_media_folder, mimetype="application/zip")
media_file = (
    service.files()
    .create(body=media_metadata, media_body=media_media, fields="id")
    .execute()
)

print(f"Media backup uploaded to Google Drive: {media_file.get('id')}")

original_db = "db.sqlite3"
shutil.copy(backup_filename, original_db)
print(f"Replaced {original_db} with {backup_filename}")
