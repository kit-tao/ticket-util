SET SCRIPT_PATH=.
SET WEBHOOK_URL=https://webhook.site/9edfe49b-ca08-419f-a076-acb92fe13c78
SET GOOGLE_SHEET_ID=1rXXWQdneb0d4dDQw4LOeLpa8YDTOwvlQl0Ad2xzswXc

%SCRIPT_PATH%\venv\scripts\python.exe process_ticket.py -sheetid %GOOGLE_SHEET_ID% -range "Sheet1!A2:F" -webhook_url %WEBHOOK_URL% -testmode no