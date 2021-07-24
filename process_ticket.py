import json

# subject = "test"

# email = {'subject':subject, 'to_address':'test@gmail.com',}

# data = {}
# data['key'] = 'value'
# json_data = json.dumps(data)

# print(json_data)


def get_last_run_date():
    with open("tutswiki.json", "r") as jsonfile:
        data = json.load(jsonfile)
        print("Read successful")
    print('test')
    return data

def save_last_run_date(run_date):
    p_json = {'last_run_date':run_date}

    
    with open("tutswiki.json", "w") as jsonfile:
        jsonfile.write(myJSON)
        print("Write successful")

def get_report():

    """
    Connect to google api to download latest ticket report
    return data in Pandas dataframe
    """
    print("test")

def process_report():
    print("test")

def build_email_json(fullname, subject, email_address, email_body, to_address, cc_address):
    s_email = {'subject':subject, 'to_address':to_address, 'cc_address':cc_address, 'body':email_body}
    s_main = {'full_name':fullname, 'email_address':email_address, "ready_to_send":True, 'email':s_email}

    json_data = json.dumps(s_main)
    print(json_data)

def send_email(p_json):
    print("test")


if __name__ == "__main__":
   build_email_json(fullname="Phil Tao", subject="test", email_address="ticket@gmaillc.om", email_body="list of tickets status", to_address=["tao@gmail.com","abc@gmail.com"], cc_address=["tao@gmail.com","abc@gmail.com"])
