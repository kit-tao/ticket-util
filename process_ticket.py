import json
import pandas as pd
import argparse
import os
import datetime
from dateutil.relativedelta import relativedelta
import requests
from requests.structures import CaseInsensitiveDict
import traceback
import google_api




def default_date():
    # define default last run date as 18 months ago from today
    today = datetime.date.today()
    # relativedelta(months=-1)
    run_date = today + relativedelta(months=-5)
    print(run_date)
    return run_date
    


def get_last_run_date():


    if os.path.exists("last_run_date.json"):
        try:
            with open("last_run_date.json", "r") as jsonfile:
                data = json.load(jsonfile)
                if len(data) != 0:
                    return data['last_run_date']
        except:
            run_date = default_date()
            return run_date
    else:
        run_date = default_date()
        return run_date


        


def save_last_run_date(run_date):
    last_run = {'last_run_date':run_date.strftime("%d/%m/%Y")}
    with open("last_run_date.json", "w") as jsonfile:
        jsonfile.write(json.dumps(last_run))
        






def get_report_xls(location):

    """
    Read xls file
    return data in Pandas dataframe
    """
    df = pd.read_excel(location)
    # cast date column to pandas datetime
    df['Date']=pd.to_datetime(df['Date'])
    # add fullname column
    fullname=df['Firstname']+ " " + df['Lastname'] 
    df['Fullname']=fullname
    return df

    
def get_data_api(spreadsheet_id, range_name):
    

    """
    Retrieve Google spreadsheet via API
    return data in Pandas dataframe
    """
    try:
        df = google_api.get_spreadsheet_data(spreadsheet_id=spreadsheet_id, range_name= range_name)
    
        # cast date column to pandas datetime
        df['Date']=pd.to_datetime(df['Date'])
        # add fullname column
        fullname=df['Firstname']+ " " + df['Lastname'] 
        df['Fullname']=fullname
        return df
    except:
        traceback.print_exc()
        print("Error: unable to call Google API")
        raise
        
    

    



def generate_json(out_df):
    """
    input parameters: 
    df 
    last_run_date: a string representation of 'YYYY-MM-DD'
    """
    out_dict = []
    subject = "Ticket status report"
    body = ""

    

    
    if not out_df.empty:
        
        
        # get all customer by fullname
        cust_df = out_df[['Fullname','Firstname','Lastname','Email']].drop_duplicates()
        # For each customer loop
        for index, row in cust_df.iterrows():
            
            fullname = "{0} {1}".format(row["Firstname"], row["Lastname"].upper())
            print(row["Fullname"])

            # process individual ticket for customers
            detail_df = out_df[(out_df['Fullname'] == row["Fullname"])]    
            for i, det in detail_df.iterrows():
                print(det)
                body = body + "Ticket no. {0} was closed on {1}\n".format(det["Ticket"], det["Date"].strftime('%Y.%m.%d'))
                
            s_email = {'subject': subject, 'to_address': [row["Email"]], 'cc_address':[""], 'body': body}
            s_main = {'full_name':fullname, 'email_address':row["Email"], "ready_to_send": True, 'email':s_email}
            out_dict.append(s_main)

        json_data = json.dumps(out_dict)    
        return (json_data)
    else:
        print("Nothing to process")
        return ""




def filter_report(df, last_run_date):
    """
    input parameters: 
    df 
    last_run_date: a string representation of 'YYYY-MM-DD'
    """
    # Filter records where status == 'Closed' and 'LastDate' > last_run_date in config file
    out_df = df[(df['Status'] == 'Closed') &  (df['Date'] > pd.to_datetime(last_run_date))]    
    # sort by fullname
    return (out_df.sort_values(by='Fullname')) 
    
   

    

def post_json(payload, url):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data=payload)
    return (resp.status_code)



parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-sheetid', help='specify the Google spreadsheet_id.', required=True)
parser.add_argument('-range', help='specify the Google Spreadsheet Range name e.g.  Sheet1!A2:F', required=True)
parser.add_argument('-webhook_url', help='The email api web address', required=True)
parser.add_argument('-testmode', help='if yes is specified then run in test mode. It will not send json to email webhook', required=True)


args = parser.parse_args()



if __name__ == "__main__":
    last_run_date = get_last_run_date()
    
    df = get_data_api(spreadsheet_id=args.sheetid, range_name= args.range)
    out_df = filter_report(df, last_run_date)
    load = generate_json(out_df)
    
    if args.testmode != "yes":
        status = ""
        if len(load) != 0:
            try:
                status = post_json(payload = load, url = args.webhook_url)
                print(status)
                if status == 200:
                    print("success")
                    # update the config file with the max date
                    max_dt = max(out_df['LastDate'])        
                    save_last_run_date(max_dt)
            except:
                traceback.print_exc()
                print("Error: sending email via webhook")
    else:
        print("Test mode")


    


