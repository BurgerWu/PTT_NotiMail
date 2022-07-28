import re
import bs4
from bs4 import BeautifulSoup
import requests

def get_keywords():
    with open('keyword_bags.txt','r+',encoding="utf-8") as f:
        kw_txt = f.read()
    return kw_txt

def get_max_index(soup):
    find_index = re.findall(r'index([0-9]*).html', soup)
    possible_index = []
    for i in range(len(find_index)):
        try:
            possible_index.append(int(find_index[i]))
        except:
            pass
    print(max(possible_index))   
    return(max(possible_index))

def get_ptt_content_title():
    url = "https://www.ptt.cc/bbs/forsale/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all("div", 'title')
    print(result[-1])
    return response.text

def main():
    kw_txt_bags = get_keywords()
    webpage_soup = get_ptt_content_title()
    max_pg_index = get_max_index(webpage_soup)

main()