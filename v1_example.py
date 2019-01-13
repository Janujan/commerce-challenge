import json
import requests

def getItemList(url, token):
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    response = requests.get(url, jsondata, headers = headers)

    return response.json()

def getDetailItem(url, token):
    url = url + 'pen'
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    response = requests.get(url, jsondata, headers = headers)

    return response.json()

def getAvailableItem(url, token):
    url = url + "?avail=1"
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    response = requests.get(url, jsondata, headers = headers)

    return response.json()


def purchaseItem(url, token):
    body={ 'title': 'pen', 'quantity':10 }
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    jsondata = json.dumps(body)
    response = requests.post(url, jsondata, headers = headers)


#v1 example
if __name__=="__main__":
    #first get auth token
    username = 'shopify'
    password = 'testing12'

    url = "http://localhost:8000/api-token-auth/"
    body = { 'username':username , 'password':password }
    jsondata = json.dumps(body)
    headers = {'Content-type': 'application/json; charset=utf-8'}

    response = requests.post(url, jsondata, headers = headers)
    token = response.json()['token']
    print(token)

    #create cart
    url = "http://localhost:8000/commerce/v1/"


    items = getItemList(url, token)
    print(items)

    item = getDetailItem(url, token)
    print(item)

    items = getAvailableItem(url, token)
    print(items)

    purchaseItem(url, token)
    items = getItemList(url, token)
    print(items)
