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



## first interation




The email body should contain all the tickets status.


## Future improvement
Use Python  google api to connect to read from spreadsheet.
download the spreadsheet from the google link.
Open the spreadsheet.

Load the spreadsheet into Panda data frame.


