from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1xR2f3FrjplZ0n8cEyMMSxJp7ttgJlyqsERELcS2cLwQ"
RANGE_NAME = "Sheet1!A2:H"

creds = Credentials.from_service_account_file(
    "service_account.json", scopes=SCOPES
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
    rows = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute().get("values", [])

    for idx, row in enumerate(rows):
        if row[1] == route:
            student = int(row[6])
            employee = int(row[7])

            if user_type == "student":
                student += change
            else:
                employee += change

            occupied = student + employee
            capacity = int(row[3])

            if occupied < 0 or occupied > capacity:
                raise Exception("Invalid seat count")

            update_range = f"Sheet1!G{idx+2}:H{idx+2}"
            body = {"values": [[student, employee]]}

            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption="RAW",
                body=body
            ).execute()

            return True

    raise Exception("Route not found")
