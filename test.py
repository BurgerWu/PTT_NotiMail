from datetime import datetime
from functions.scraping import *
import re
info_json = load_output_json()
D1 = datetime.strptime(info_json['forsale']['last_check_time'],"%Y-%m-%d")
D2 = datetime.strptime(datetime.strftime(datetime.now(),"%Y-%m-%d"), "%Y-%m-%d")
print(type(D2))