# library
import os, sys
import csv
sys.path.insert(1, splunk_sdx_python_path)
import splunklib.client as client

#GLOBAL
DEFAULT_HOST="localhost"
DEFAULT_PORT="8089"
DEFAULT_USERNAME="admin"
DEFAULT_PASSWD="ADMINADMIN"

#PATH
#splunk python sdk path
splunk_sdk_python_path="/opt/splunk/lib/python3.7/site-packages/splunk-sdk-python"
# splunk python path
splunk_python_path="/opt/splunk/bin/python"
# CSV file path
csv_path = ""




# search 
def search_command():
    search "search SPL" --earliest_time="2011-03-12T17:15:00.000-07:00" --output_mode=csv --vrbose=verbose
    return res

# save as .csv file
save_csv(f1, res1)
save_csv(f2, res2)

# compare


# save csv
def save_csv(filename, data):
    file = csv_path + filename
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)




def main():
    s = client.connect(host=DEFAULT_HOST, port=DEFAULT_PORT, username=DEFAULT_USERNAME password=DEFAULT_PASSWD)
    res1 = search()
    res2 = search()
    #applications = s.apps
    #new_app = applications.create("my_fake_app")
    

if __name__ == "__main__":
    main()
