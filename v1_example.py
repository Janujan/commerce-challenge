import json
import requests
import time

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

    url = "http://shopify-janujan.herokuapp.com/api-token-auth/"
    body = { 'username':username , 'password':password }
    jsondata = json.dumps(body)
    headers = {'Content-type': 'application/json; charset=utf-8'}

    response = requests.post(url, jsondata, headers = headers)
    token = response.json()['token']
    print(token)

    #create cart
    url = "http://shopify-janujan.herokuapp.com/commerce/v1/"

    start_time = time.time()
    items = getItemList(url, token)
    print('items_time')
    itemList_time = time.time()-start_time
    print(itemList_time)

    start_time = time.time()
    item = getDetailItem(url, token)
    print('detail_item_time')
    detail_time = time.time() - start_time
    print(detail_time)

    start_time = time.time()
    print('avail_time')
    items = getAvailableItem(url, token)
    avail_time = time.time() - start_time
    print(avail_time)

    #purchaseItem(url, token)
    #items = getItemList(url, token)
    #print(items)
