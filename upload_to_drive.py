#!/usr/bin/env python3
"""
Google Drive uploader module.
Uploads the daily Excel report to a shared Drive folder.

Requires env var:  GOOGLE_CREDENTIALS  (JSON content of service account key)
                   DRIVE_FOLDER_ID      (target folder ID)
"""

import json
import os
import sys
from pathlib import Path

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GDRIVE_AVAILABLE = True
except ImportError:
    GDRIVE_AVAILABLE = False


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_credentials():
    """Load service account credentials from env var or local file."""
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if creds_json:
        info = json.loads(creds_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)

    # Fallback: look for credentials file next to this script
    creds_file = Path(__file__).parent / "google_credentials.json"
    if creds_file.exists():
        return Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)

    raise FileNotFoundError(
        "No Google credentials found. Set the GOOGLE_CREDENTIALS env var "
        "or place google_credentials.json in the repo root."
    )


def upload_file(local_path: Path, folder_id: str) -> str:
    """
    Upload (or update) a file in the given Drive folder.
    Returns the web link to the uploaded file.
    """
    if not GDRIVE_AVAILABLE:
        print("  ⚠️  google-api-python-client not installed — skipping Drive upload.")
        print("      Run: pip install google-api-python-client google-auth")
        return ""

    creds = _get_credentials()
    service = build("drive", "v3", credentials=creds)

    file_name = local_path.name
    mime_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if local_path.suffix == ".xlsx"
        else "application/octet-stream"
    )

    # Check if file already exists in the folder (update instead of duplicate)
    existing = service.files().list(
        q=f"name='{file_name}' and '{folder_id}' in parents and trashed=false",
        fields="files(id, name)",
    ).execute().get("files", [])

    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)

    if existing:
        file_id = existing[0]["id"]
        updated = service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id, webViewLink",
        ).execute()
        link = updated.get("webViewLink", "")
        print(f"  ✅ Drive updated: {file_name}  →  {link}")
    else:
        created = service.files().create(
            body={"name": file_name, "parents": [folder_id]},
            media_body=media,
            fields="id, webViewLink",
        ).execute()
        link = created.get("webViewLink", "")
        print(f"  ✅ Drive uploaded: {file_name}  →  {link}")

    return link


def upload_report(excel_path: Path) -> str:
    """Convenience wrapper — reads folder ID from env or config."""
    folder_id = os.environ.get("DRIVE_FOLDER_ID", "")

    if not folder_id:
        # Try config.json fallback
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                cfg = json.load(f)
            folder_id = cfg.get("drive_folder_id", "")

    if not folder_id:
        print("  ⚠️  DRIVE_FOLDER_ID not set — skipping Drive upload.")
        return ""

    try:
        return upload_file(excel_path, folder_id)
    except Exception as e:
        print(f"  ❌ Drive upload failed: {e}")
        return ""


if __name__ == "__main__":
    # Quick test: python upload_to_drive.py path/to/report.xlsx
    if len(sys.argv) < 2:
        print("Usage: python upload_to_drive.py <path_to_xlsx>")
        sys.exit(1)
    link = upload_report(Path(sys.argv[1]))
    if link:
        print(f"View report: {link}")
