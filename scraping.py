#import modules and packages
from datetime import datetime
from functions.send_mail import *
from functions.scraping import *
import json
from datetime import datetime


def main():
    """
    This main function pipes the overall process of scraping information and sending notification emails
    """
    #Retrieve relevant information from information.json file
    info_json = load_output_json()
    kw_txt_bags = info_json['keywords']
    last_check_time = datetime.strptime(info_json['last_check_time'],"%Y-%m-%d")

    #Obtain content list from ptt after last check time
    content_list = get_ptt_content_list(last_check_time)

    #Initiate kwyword specific content dictionary
    kw_content_dict = {}

    #Iterate through keywords to retrieve content from content list and send emails
    for keyword in kw_txt_bags:

        #Check if keyword appears in title in content list
        kw_content_dict[keyword] = [x for x in content_list if keyword in x['title']]  

        #If there is keyword appearing in title in content list, trigger email sending process
        if len(kw_content_dict[keyword]) >= 1:
            send_mail(info_json['email_receiver'], info_json['last_check_time'], keyword, kw_content_dict[keyword])

    #Modify information.json file to renew last check time
    info_json["last_check_time"] = datetime.strftime(datetime.now(),"%Y-%m-%d")

    #Update information.json with new check time
    with open('information.json','w', encoding='utf-8') as json_file:
        return json.dump(info_json, json_file, ensure_ascii = False)

main()