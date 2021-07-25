# Customer ticket status notification utility


## Description

Trend Micro generate a report from their ticketing system and upload the report into Google Spreadsheet on a weekly basis. 
The purpose of this utility is to process customer ticket status report to:
1. identify which tickets have been closed from the spreadsheet data.
2. notifiy customers when their ticket was closed via email webhook 
3. Each customer should receive at most one email per week
4. the utility should run once a week



## Design assumptions

The design of this software utility assumes the following:

1. The Date column in the report contains the  timestamp of when the ticket was created or when there is changed of status. 
    e.g. when ticket is opened or when status is changed from open to closed, the Date column contains the current date.
2. No database is used to store the history of the ticket status report. Therefore it will only identify ticket with closed status from a last report run date.




# Prerequisites



### Google API
 
This utility uses Google API to retrieve data from Google spreadsheet.
Follow the instruction below to create a Google project and enable Google API.

https://developers.google.com/sheets/api/quickstart/python


### OS Environment

Windows EC2 is used to host the Ticket status notification utility.  The decision to use Windows EC2 is because the utility uses
Oauth 2.0 authentication/authorization method to access Google API. 

When OAuth 2.0 is used for authorization, Google displays a consent web page to request user's authorization.



### Python 3.6 and above

Please download 3.6 or above Python using installation link below:

https://www.python.org/downloads/




# Installation

Below is the instructions on how to install Python ticket notification utility.

1. Clone this github repo
2. Change directory into the repo directory
3. Create Python virtual environment:
    python -m venv venv
4. Activate virtual environment

Linux:

source venv/bin/activate

Windows:

run venv\scripts\activate.bat

4. Install Python packages using pip

pip install -r requirements.txt





# Usage


python process_ticket.py -sheetid "1rXXWQdneb0d4dDQw4LOeLpa8YDTOwvlQl0Ad2xzswXc" -range "Sheet1!A2:F" -webhook_url "https://webhook.site/9edfe49b-ca08-419f-a076-acb92fe13c78" -testmode yes



# ticket-util
This repo contains the ticketing utililty to process customer ticket status.

## Design

The util requires an input Google spreadsheet or excel.

Need to keep track of the last report run date to compare against the closed date in each customer record. 


## Approch

The utility is a command line tool that;


python config file:
a reference close date in the config file.

If there is more than one ticket status for the customer. it should only send one email with multiple tickets status in the body.
Only one email should be sent per week.


## Assumption
the date column in the xls file contains the last updated date.  This column will be used to compare against the last run date.

## first interation







## Future improvement

Use Python google api to retrieve data from Google spreadsheet.


Store spreadsheet in S3 bucket.   
Use AWS lambda Python runtime to host this utility and configure lambda function to listen for S3 object create event.



Configure Lamb




