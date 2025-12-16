import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1xR2f3FrjplZ0n8cEyMMSxJp7ttgJlyqsERELcS2cLwQ"
RANGE_NAME = "Sheet1!A2:H"

# Load credentials from ENV
service_account_info = json.loads(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
)

creds = Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()


def get_routes():
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    rows = result.get("values", [])
    data = []

    for row in rows:
        if row[1].strip().lower() == "total":
            continue

        data.append({
            "route": row[1],
            "total_seats": int(row[2]),
            "capacity": int(row[3]),
            "vacant": int(row[4]),
            "occupied": int(row[5]),
            "student": int(row[6]),
            "employee": int(row[7]),
        })

    return data


def update_count(route, user_type, change):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    rows = result.get("values", [])

    for idx, row in enumerate(rows):
        sheet_route = row[1].strip()

        if sheet_route == route.strip():
            capacity = int(row[3])
            student = int(row[6])
            employee = int(row[7])

            if user_type == "student":
                student += change
            elif user_type == "employee":
                employee += change
            else:
                raise Exception("Invalid user type")

            if student < 0 or employee < 0:
                raise Exception("Count cannot be negative")

            occupied = student + employee
            vacant = capacity - occupied

            update_range = f"Sheet1!E{idx+2}:H{idx+2}"
            body = {
                "values": [[vacant, occupied, student, employee]]
            }

            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption="RAW",
                body=body
            ).execute()

            return True

    raise Exception("Route not found")
