from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import requests,json
# Create your views here.

class HomeView(View):


    def get(self,request):
        access_Token=get_new_token()
        login("http://services.rouhinasteel.com/ords/fnd/public/ords_issuite_login",access_Token)
        str_data=get_data("http://services.rouhinasteel.com/ords/mam/mam/p1230sup_2021/?offset=150",access_Token)
        full_json_data=json.loads(str_data)
        #filtered_json = [x for x in full_json_data['items'] if x['f8'] == '116']
        print(full_json_data)
        return render(request,'irisa/main.html',{'dataset':full_json_data})
    






def get_new_token():
    acc_token_url = "http://services.rouhinasteel.com/ords/oauth/token"
    client_id = 'sPBgTn3ndgT270eRqSUHNw..'
    client_secret = 'H_oq95t8hVZ-_etF6Grh8Q..'
    token_req_payload = {'grant_type': 'client_credentials'}
    token_response = requests.post(acc_token_url , data = token_req_payload, verify = False, allow_redirects = False, auth = (client_id, client_secret))
          
    if token_response.status_code != 200:
        print("Failed to obtain token from OAuth2 server")
    else:
        print("Successfuly obtained a new token from OAuth2 server")
        tokens = json.loads(token_response.text)
    return tokens['access_token']


def login(url,access_token):
    data = {"grant_type": "client_credentials","P_USER_NAME": "229173", "P_PASS": "123456789"}
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.post(url, headers=headers,data=data)
    return response.text


def get_data(url,access_token):
    data = {"grant_type": "client_credentials","P_USER_NAME": "229173", "P_PASS": "123456789"}
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=headers,data=data,verify = False, allow_redirects = False)
    return response.text
