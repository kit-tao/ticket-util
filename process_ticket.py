import json
import pandas as pd
import argparse
import os
import datetime
from dateutil.relativedelta import relativedelta
import requests
from requests.structures import CaseInsensitiveDict



def init_conf():
    today = datetime.date.today()
    relativedelta(months=-18)
    run_date = today + relativedelta(months=-18)
    save_last_run_date(run_date)


def get_last_run_date():

    if os.path.exists("last_run_date.json"):
        try:
            with open("last_run_date.json", "r") as jsonfile:
                data = json.load(jsonfile)
                return data['last_run_date']
        except:
            init_conf()
    else:
        init_conf()
        


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
    df.rename(columns={"Date":"LastDate"},inplace=True)
    return df

    
    


def get_report_api(location):

    """
    """
    None



def process_report(df, last_run_date):
    """
    input parameters: 
    df 
    last_run_date: a string representation of 'YYYY-MM-DD'
    """
    out_dict = []

    # Filter records where status == 'Closed' and 'LastDate' > last_run_date in config file
    out_df = df[(df['Status'] == 'Closed') &  (df['LastDate'] > pd.to_datetime(last_run_date))]    
    
    
    if not out_df.empty:
        max_dt = max(out_df['LastDate'])        
        save_last_run_date(max_dt)
        # update the config file with the max date

        for index, row in out_df.iterrows():
            fullname = "{0} {1}".format(row["Firstname"], row["Lastname"].upper())
            subject = "Ticket no. {0} status".format(row["Ticket"])
            body = "Dear {0}, your ticket no. {1} was closed on {2}".format(row["Firstname"], row["Ticket"], row["LastDate"].strftime('%Y.%m.%d'))
            
            s_email = {'subject': subject, 'to_address': [row["Email"]], 'cc_address':[row["Email"]], 'body': body}
            s_main = {'full_name':fullname, 'email_address':row["Email"], "ready_to_send": True, 'email':s_email}
            out_dict.append(s_main)

        json_data = json.dumps(out_dict)    
        return (json_data)
    else:
        print("Nothing to process")

    

def post_json(payload, url):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data=payload)
    return (resp.status_code)



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-mode', help='The method to retrieve ticket report.  api or xls', required=True)
parser.add_argument('-location', help='if mode=api then location should contains url.  else the location should contain the file name of xls file', required=True)
parser.add_argument('-webhook_url', help='The email api web address', required=True)

args = parser.parse_args()



if __name__ == "__main__":
    last_run_date = get_last_run_date()
    location = args.location

    if args.mode == "xls":
        if os.path.exists(location):
            df = get_report_xls(location)
    else:
        df = get_report_api(location)
    load = process_report(df, last_run_date)
    status = post_json(payload = load, url = args.webhook_url)
    print(status)
    if status["success"]=="true":
        print("success")


    else:
        print(f"Error: xls file {location} does not exist")


