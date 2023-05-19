#----------------------------------------------------------need version python 3.8.10 or higher----------------------------------------------------------#


import json # for work with JSON data
from datetime import datetime  # for convert data and time from unixtime  
import requests # for requests to API
from authorization import BASE_API_URL # cazi.yougile.com
from authorization import HEADER_AUTH # header with contetn-type and authorization

#----------------------------------------------------------block-with-main-get-information----------------------------------------------------------#
LIST_USERS = requests.get(f"{BASE_API_URL}users", headers=HEADER_AUTH).json().get('content') # get all users
#print(json.dumps(LIST_USERS, indent=2, ensure_ascii=False)) # debug fir print LIST_USERS

LIST_PROJECT = requests.get(f"{BASE_API_URL}projects", headers=HEADER_AUTH).json().get('content') # get all project
#print(json.dumps(LIST_PROJECT, indent=2, ensure_ascii=False)) # debug for print LIST_PROJECT

LIST_BOARDS = requests.get(f"{BASE_API_URL}boards", headers=HEADER_AUTH).json().get('content') # get all boards
#print(json.dumps(LIST_BOARDS, indent=2, ensure_ascii=False)) # debug for print LIST_BOARDS

LIST_COLUMNS = requests.get(f"{BASE_API_URL}columns", headers=HEADER_AUTH).json().get('content') # get all columns
#print(json.dumps(LIST_COLUMNS, indent=2, ensure_ascii=False)) # debug for print LIST_COLUMNS

LIST_TASKS = requests.get(f"{BASE_API_URL}tasks", headers=HEADER_AUTH, params={'limit':1000}).json().get('content') # get all tasks
#print(json.dumps(LIST_TASKS, indent=2, ensure_ascii=False)) # debug for print LIST_TASKS

#----------------------------------------------------------block-with-main-get-information----------------------------------------------------------#


for count in LIST_TASKS: # print list with current tasks
    if (count.get('deadline') is not None) and count.get('completed') is False:
        print(f"Срок сдачи задачи - \"{count.get('title')}\" закончится:\n-{datetime.utcfromtimestamp((count.get('deadline').get('deadline')/1000)).strftime('%Y-%m-%d %H:%M:%S')}")


