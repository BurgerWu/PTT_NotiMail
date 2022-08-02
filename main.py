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
    print('Retrieving information from json file')
    info_json = load_output_json()
    print(list(info_json.keys()))

    #Iterate through different board of interest
    for board_name in list(info_json.keys()):
        print(board_name)
        #Retrieving keywords from board of interest
        kw_txt_bags = info_json[board_name]['keywords']

        #If last check date is today, stop the operation for this board. 
        #If last check date is empty, fill it with today.
        if len(info_json[board_name]['last_check_time']) != 0:
            print("1")
            if info_json[board_name]['last_check_time'] != datetime.now().date():
                print("2")
                last_check_time = datetime.strptime(info_json[board_name]['last_check_time'],"%Y-%m-%d")
            else:
                print("Already performed search for today, see ya tomorrow!")
                continue
        else:
            print('3')
            last_check_time = datetime.strptime(datetime.strftime(datetime.now(),"%Y-%m-%d"), "%Y-%m-%d")


        #Obtain content list from ptt after last check time
        print('Retrieving content list in {}'.format(board_name))
        content_list = get_ptt_content_list(last_check_time, "https://www.ptt.cc/bbs/{}/index.html".format(board_name))

        #Initiate kwyword specific content dictionary
        kw_content_dict = {}

        #Iterate through keywords to retrieve content from content list and send emails
        for keyword in kw_txt_bags:

            #Check if keyword appears in title in content list
            print('Working on keyword {} in {}.'.format(keyword, board_name))
            kw_content_dict[keyword] = [x for x in content_list if keyword in x['title']]  

            #If there is keyword appearing in title in content list, trigger email sending process
            if len(kw_content_dict[keyword]) >= 1:
                print('Sending email on keyword {} in {}.'.format(keyword, board_name))
                send_mail(info_json[board_name]['email_receiver'], info_json[board_name]['last_check_time'], keyword, board_name, kw_content_dict[keyword])

        # #Modify information.json file to renew last check time
        print('Updating information json file')
        info_json[board_name]["last_check_time"] = datetime.strftime(datetime.now(),"%Y-%m-%d")

     #Update information.json with new check time
    with open('information.json','w', encoding='utf-8') as json_file:
        json.dump(info_json, json_file, ensure_ascii = False)

main()