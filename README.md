# Customer ticket status notification utility


## Description

TM generate a report from their ticketing system and upload the report into Google Spreadsheet on a weekly basis. 
The purpose of this utility is to process customer ticket status report to:
1. identify which tickets have been closed from the spreadsheet data.
2. notifiy customers when their ticket was closed via email webhook 
3. Each customer should receive at most one email per week
4. the utility will be run once a week


## Design assumptions

The design of this software utility assumes the following:

1. The Date column in the report contains the  timestamp of when the ticket was created or when there is changed of status. 
    i.e. when ticket's status is changed, the Date column contains the date when status change occurred.
2. No database is used to store the history of the ticket status report. Therefore it can only identify ticket with closed status from a last report run date.


# Prerequisites

### Google API
 
This utility uses Google API to retrieve data from Google spreadsheet.
Follow the instruction below to create a Google project and enable Google API for Google spreadsheet.

https://developers.google.com/sheets/api/quickstart/python

Download the client_secret_key credential and save the file as credential.json in the same folder as process_ticket.py.

### OS Environment

Windows EC2 is used to host the Ticket status notification utility.  The decision to use Windows EC2 is because the utility uses
Oauth 2.0 authentication/authorization method to access Google API. 
When the utility is executed the first time, during Google  API authentication, it will open web browser to Google to authenticate Google workspace userd.  The user must grant consent to allow access to Spreadsheet content.
Once the authentication has completed the first titme, the authentication token is stored in the local file system for future use.



### Python 3.6 and above

Please download 3.6 or above Python using installation link below:

https://www.python.org/downloads/



# Installation

On Windows, Git Bash

Below is the instructions on how to install Python ticket notification utility.

1. Clone this github repo or Download as Zip file
2. Change directory into the repo directory
3. Create Python virtual environment:
    python -m venv venv
4. Activate virtual environment

On Windows:

Run venv\scripts\activate.bat

4. Install Python packages using pip

pip install -r requirements.txt


## Files

* Main program : process_ticket.py
* Google api module: google_api.py
* run_util.bat: Windows batch file run the main program in the Python virtual environment
* Pip package list:  requirements.txt
* Readme.md : This Documentation




## Prepare the host to authenticate with Google API 

* Ensure that the credential.json which contains the Google client_secret_key credential is present in the same folder as process_ticket.py.


Run the following Python script file to authenticate with Google API:

In the Window command:

Ensure that virtual environment has been activated. See Installation step above.

python google_api.py

The google_api.py utility will open web browser to authenticate user to Google.  

If the authentication and authorization is successful then the util will display records of the Google spreadsheet.


# First time Setup

The utility has one json config file "last_run_date.json" which stores the last_run_date.  
This date is used to process new records in the spreadsheet where Date > last_run_date.

If the "last_run_date.json" file does not exist, it will be created by the proces_ticket.py script with the default last_run_date of 18 months ago(from today).

When the utility has completed successfully i.e. email api has been invoked without problem.  It will update the date in the last_run_date.json to the max(date) of all Closed records.

User can create the file last_run_date.json manually in the same folder as process_ticket.py,
if a different default date is required, with one entry like below(where DD/MM/YYYY: e.g. 02/10/2010):

{"last_run_date": "DD/MM/YYYY"}





# Windows scheduler setup

On the Windows EC2, 

Create Windows scheduler task to call the batch file run_util.bat on a weekly basis.




# Utility Command line usage
e.g.
python process_ticket.py -sheetid <google sheet id> -range "Sheet1!A2:F" -webhook_url <webhook url> -testmode yes

-sheetid <google sheet id>
-webhook_url <webhook url>
-testmode yes (when testmode is yes then no email api will be invoked).




## Future improvements

* Use Google API keys instead of OAuth. so that application can pass API keys to Google API without getting prompted for Oauth Consent page.

* Instead of using Google Spreadsheet, If the Excel report can be uploaded to AWS S3 bucket.  Then a AWS lambda Python runtime can be used to host this utility and configured to run based on S3 object creation event.

* If lambda runtime is used then Dynamo DB table can be used to store the last_run_date. 










