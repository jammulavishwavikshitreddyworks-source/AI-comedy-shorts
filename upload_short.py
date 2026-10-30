import os, json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    required = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [x for x in required if not os.getenv(x)]
    if missing:
        raise SystemExit("Missing GitHub Actions secrets: " + ", ".join(missing))

    creds = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    youtube = build("youtube", "v3", credentials=creds)
    meta = json.loads(Path("output/metadata.json").read_text(encoding="utf-8"))

    # Schedule 15 minutes ahead so the upload finishes before publishAt.
    publish_at = (datetime.now(timezone.utc) + timedelta(minutes=15)).replace(microsecond=0)
    body = {
        "snippet": {
            "title": meta["title"][:100],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "23",
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.isoformat().replace("+00:00", "Z"),
            "selfDeclaredMadeForKids": False
        }
    }
    # This project produces stylized cartoon graphics, not realistic synthetic footage.
    media = MediaFileUpload("output/short.mp4", mimetype="video/mp4", resumable=True)
    result = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    ).execute()
    print("Scheduled video ID:", result.get("id"))
    print("Scheduled publish time (UTC):", publish_at.isoformat())

if __name__ == "__main__":
    main()
