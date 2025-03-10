from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import requests
import datetime

DRIVE_FOLDER_ID = "1LQPQi95MXosBrXD1MLddMoo5gtVYVn2P"

creds = Credentials.from_service_account_file(
    "credentials.json", scopes=["https://www.googleapis.com/auth/drive.file"]
)
service = build("drive", "v3", credentials=creds)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f"db_{timestamp}.sqlite3"
db_url = "https://builderspace.onrender.com/api/download-db/"
response = requests.get(db_url)
with open("db.sqlite3", "wb") as f:
    f.write(response.content)


file_metadata = {"name": backup_filename, "parents": [DRIVE_FOLDER_ID]}
media = MediaFileUpload(backup_filename, mimetype="application/x-sqlite3")
file = (
    service.files().create(body=file_metadata, media_body=media, fields="id").execute()
)

print(f"Backup uploaded to Google Drive: {file.get('id')}")
