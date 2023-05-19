#----------------------------------------------------------need version python 3.8.10 or higher----------------------------------------------------------#



import requests # <- for requests to API 
import os # <- for get envirion from OS
import json # <- for work with JSON data
from datetime import datetime 



def get_key_api(_id_company, _login_params, _base_api_url): # function for get key authentication api
    _login_params.update({'companyId':_id_company}) # <- here - {"login":API_LOGIN, "password":API_PASSWORD, "companyId":ID_COMPANY}"
    return (requests.post(f"{_base_api_url}auth/keys/get", data=_login_params)).json() # return dict with array key (now dict have one auth key) 



#----------------------------------------------------------block-for-auth----------------------------------------------------------#
API_LOGIN=os.environ.get('LOGIN_YOUGILE') # var with login from env
API_PASSWORD=os.environ.get('PASSWORD_YOUGILE') # var with password from env
BASE_API_URL="https://cazi.yougile.com/api-v2/" # var with base url for requests to api
LOGIN_PARAMS={'login':API_LOGIN, 'password':API_PASSWORD} # var with auth data for requests
ID_COMPANY=requests.post(f"{BASE_API_URL}auth/companies", data=LOGIN_PARAMS).json().get('content')[0].get('id') # get id Atomzachitainform
KEY_API=(get_key_api(ID_COMPANY, LOGIN_PARAMS, BASE_API_URL))[0].get('key') # var with private key for basic auth to api
HEADER_AUTH={"Content-Type": "application/json", "Authorization":"Bearer "+ KEY_API} # var containing main data for basic auth in headers
#----------------------------------------------------------block-for-auth----------------------------------------------------------#

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
    if (count.get('deadline') is not None) and count.get('completed') == False:
        print(f"Срок сдачи задачи - \"{count.get('title')}\" закончится:\n*************{datetime.utcfromtimestamp((count.get('deadline').get('deadline')/1000)).strftime('%Y-%m-%d %H:%M:%S')}*************")



'''
----------------------------------------------------------structure-data-yougile----------------------------------------------------------
Описание API - https://yougile.com/api-v2/

1. Проект - "Название проекта" --- https://yougile.com/api-v2#/operations/ProjectController_search
(в Проекте есть):
2. Доски - "Название доски" --- https://yougile.com/api-v2#/operations/BoardController_search
(в Досках есть):
3. Колонки - "Название колонки" --- https://yougile.com/api-v2#/operations/ColumnController_search
(в Колонках есть):
4. Задачи - "Занвание задачи" --- https://yougile.com/api-v2#/operations/TaskController_search (у Задач есть подзадачи, но мы их не рассматриваем)
(на Задачи можно вешать стикеры):
5. Стикеры - "Тип стикера" --- https://yougile.com/api-v2#/operations/StringStickerController_search (есть езще спринт стикеры, надо разобраться что они делают)

Каждый endpoint видит id endpoint сверху и endpoint снизу.

----------------------------------------------------------structure-data-yougile----------------------------------------------------------
'''
