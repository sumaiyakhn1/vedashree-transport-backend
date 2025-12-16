import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1xR2f3FrjplZ0n8cEyMMSxJp7ttgJlyqsERELcS2cLwQ"

# 🔐 READ FROM ENV (Render-compatible)
service_account_info = json.loads(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
)

creds = Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()
