import os # for get envirion from OS

# def get_key_api(_id_company, _login_params, _base_api_url): # function for get key authentication api
    # _login_params.update({'companyId':_id_company}) # <- here - {"login":API_LOGIN, "password":API_PASSWORD, "companyId":ID_COMPANY}"
    # return (requests.post(f"{_base_api_url}auth/keys/get", data=_login_params)).json() # return dict with array key (now dict have one auth key) 


#----------------------------------------------------------block-for-auth----------------------------------------------------------#
#API_LOGIN=os.environ.get('LOGIN_YOUGILE') # var with login from env
#API_PASSWORD=os.environ.get('PASSWORD_YOUGILE') # var with password from env
BASE_API_URL="https://cazi.yougile.com/api-v2/" # var with base url for requests to api
#LOGIN_PARAMS={'login':API_LOGIN, 'password':API_PASSWORD} # var with auth data for requests
#ID_COMPANY=requests.post(f"{BASE_API_URL}auth/companies", data=LOGIN_PARAMS).json().get('content')[0].get('id') # get id company
KEY_API=os.environ.get('KEY_API_YOUGILE')
#KEY_API=(get_key_api(ID_COMPANY, LOGIN_PARAMS, BASE_API_URL))[0].get('key') # get key api from requests to api
HEADER_AUTH={"Content-Type": "application/json", "Authorization":"Bearer "+ KEY_API} # var containing main data for basic auth in headers
#----------------------------------------------------------block-for-auth----------------------------------------------------------#
