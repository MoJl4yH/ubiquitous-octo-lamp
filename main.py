# ----------------------------------------------------------need version python 3.8.10 or higher----------------------------------------------------------#


import json  # for work with JSON data
from datetime import datetime  # for convert data and time from unixtime
import requests  # for requests to API
from authorization import BASE_API_URL  # cazi.yougile.com
from authorization import HEADER_AUTH # header with contetn-type and authorization

# ----------------------------------------------------------block-with-main-get-information----------------------------------------------------------#
LIST_USERS = requests.get(f"{BASE_API_URL}users", headers=HEADER_AUTH,  # get all users
                          timeout=5).json().get('content')
# print(json.dumps(LIST_USERS, indent=2, ensure_ascii=False)) # debug fir print LIST_USERS

LIST_PROJECT = requests.get(f"{BASE_API_URL}projects", headers=HEADER_AUTH,  # get all project
                            timeout=5).json().get('content')
# print(json.dumps(LIST_PROJECT, indent=2, ensure_ascii=False)) # debug for print LIST_PROJECT

LIST_BOARDS = requests.get(f"{BASE_API_URL}boards", headers=HEADER_AUTH,  # get all boards
                           timeout=5).json().get('content')
# print(json.dumps(LIST_BOARDS, indent=2, ensure_ascii=False)) # debug for print LIST_BOARDS

LIST_COLUMNS = requests.get(f"{BASE_API_URL}columns", headers=HEADER_AUTH,  # get all columns
                            timeout=5).json().get('content')
# print(json.dumps(LIST_COLUMNS, indent=2, ensure_ascii=False)) # debug for print LIST_COLUMNS

LIST_TASKS = requests.get(f"{BASE_API_URL}tasks", headers=HEADER_AUTH, params={'limit': 1000},  # get all tasks
                          timeout=5).json().get('content')
# print(json.dumps(LIST_TASKS, indent=2, ensure_ascii=False)) # debug for print LIST_TASKS
# ----------------------------------------------------------block-with-main-get-information----------------------------------------------------------#




def current_task(_list_task):  # print list with current tasks
    print_val = ""  # var for get information about current tasks
    numeration = 1  # var for enumeration
    for count in LIST_TASKS:  # cycle for find current tasks
        # if tasks have deadline and not completed then add his in "print_val"
        if (count.get('deadline') is not None) and count.get('completed') is False:
            print_val += (f"{numeration}. Срок сдачи задачи - \"<i>{count.get('title')}</i>\" закончится — <u>{datetime.utcfromtimestamp((count.get('deadline').get('deadline')/1000)).strftime('%Y-%m-%d %H:%M:%S')}</u>\n")
            numeration += 1  # just increment
    return print_val
