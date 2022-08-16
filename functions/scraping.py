#import modules and packages
import re
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def load_output_json():
    """
    This functions loads information.json
    Output: Information json object
    """
    #Open information.json file and load into Python dictionary
    with open('information.json','r', encoding='utf-8') as json_file:
        return json.load(json_file)

def get_next_index(response_txt):
    """
    This function retrieves next page index from response content
    Input: Response text
    Output: Next page index
    """
    #Use regular expression to retrieve next page index from response text
    next_pg_index = re.findall(r'index([0-9]*).html">&lsaquo; 上頁</a>', response_txt)[0]

    #Return the index as output
    return next_pg_index

def retrieve_title_date_href(div_content, last_check_date):
    """
    This function retrieve useful information including date, title and href address from input div content
    Input:
    - div_content: Div content from web content scraping
    - last_check_date: Last time performing keyword search
    Output: Dictionary containing desired information
    """
    #Declare global variable check_date_flag to track if page search has reach end of search date
    global check_date_flag

    #Initiate validity as True
    validity = True

    #Retrieve mark content to check if the content is normal content(If there is mark content, it means its management or announcement content)
    mark = re.findall(r'"mark">([a-zA-Z! ]*)</div>', div_content)[0]

    #Assign the div segment invalid if there is mark content
    if len(mark)>=1:
        validity =False
        date_dt = ""
        href = ""
        title = ""
    else:   
        #Get date information from div content
        present_year = datetime.now().year
        date_str_list = re.findall(r'"date">(.*)</div>', div_content)[0].strip().split('/')
        date_str = '{}-{}-{}'.format(present_year, date_str_list[0], date_str_list[1])
        date_dt = datetime.strptime(date_str, "%Y-%m-%d")

        #Check if the year has changed since last operation(Year information can not be directly obtained from scraping)
        if date_dt > datetime.now():
            date_str = '{}-{}-{}'.format(present_year-1, date_str_list[0], date_str_list[1])
            date_dt = datetime.strptime(date_str, "%Y-%m-%d")

        #Check if the content date has reach invalid search date(That is, the day before last search date)
        if date_dt < last_check_date:
            check_date_flag = True
            validity = False

        #Retrieve title from div content
        title = re.findall(r'html">(.*)</a>', div_content)
        if len(title) >= 1:
            title = title[0]
        else:
            #If not able to retrieve title information, label it as invalid
            title = ""
            validity = False
        
        #Retrieve href from div content
        href = re.findall(r'href="(.*)">', div_content)
        if len(href) >= 1:
            href = href[0]
        else:
            #If not able to retrieve title information, mostly it means the post has already been deleted
            href = ""
            validity = False
    #Return information dictionary
    return {'date': date_dt, 'href': href, 'title': title, 'validity': validity}

def get_ptt_content_list(last_check_date, url, content_list = []):
    """
    This function retrieves all available content list from the PPT url, and it uses recursion method to continuously dig into 
    next page until content data has reached out-of-search date(That is, one day before last check date).
    Input:
    last_check_date: Last date performing keyword search
    url: Url address of interest
    content_list: List containing information of available content(Empty list if working on latest page(index.html), else content list comes from last recursion)

    Output:Complete content list after recursion ends
    """
    #Declare global variable check_date_flag to track if page search has reach end of search date
    global check_date_flag

    #Initiate check_date_flag as False
    check_date_flag = False

    #Obtain response from desired url
    response = requests.get(url)

    #If the request works ok, process the response
    if response.status_code == requests.codes.ok:
        resp_text = response.text
        
        #Check if r-list-sep division exists, this is the separation line of normal post and managerial posts(in case some managerial posts have no marking)
        if '<div class="r-list-sep">' in resp_text:
            resp_text = resp_text[:re.search(r'<div class="r-list-sep">', resp_text).start()]

        #Process the response with html parser
        soup = BeautifulSoup(resp_text, "html.parser")

        #Retrieve next page index from response text
        next_pg_index = get_next_index(response.text)

        #Search for div content with r-ent class 
        raw_result_list = soup.find_all("div", 'r-ent')
    else:
        #Raise error message if request is not ok
        response.raise_for_status()

    #Map the retrieve information function to all div content result and filter out invalid ones
    processed_content_list = [retrieve_title_date_href(str(x), last_check_date) for x in raw_result_list]
    processed_content_list = [x for x in processed_content_list if x['validity'] == True]

    #Combine processed list of present url with input content list(from last recursion or empty if it's the first index html)
    if len(content_list) != 0:
        content_list = content_list + processed_content_list
    else:
        content_list = processed_content_list

    #If check_date_flag is triggered to True, stop further searching, else continue the recursion
    if check_date_flag != True:

        #Modify new url with next page index and pass on the content list
        new_url = re.findall(r'(.*index)[0-9 ]*.html', url)[0] + str(next_pg_index) + ".html"    
        content_list = get_ptt_content_list(last_check_date, new_url, content_list)

    #Return final content list
    return content_list