import json
import requests

def createCart(url, token):
    body = {'command':'create', 'cart_name':'tests' }
    jsondata = json.dumps(body)
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    response = requests.post(url, data=jsondata, headers = headers)
    print(response.json())
    return response.json()['cart_id']

def updateCart(url, cart_id, token):
    body = {'command':'update', 'cart_id':cart_id, 'title':'pencil', 'quantity':5 }
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    jsondata = json.dumps(body)
    response = requests.post(url, data=jsondata, headers = headers)
    print(response.json())

def completeCart(url, cart_id, token):
    body = {'command':'complete', 'cart_id':cart_id }
    headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': 'Token ' + str(token)}
    jsondata = json.dumps(body)
    response = requests.post(url, data=jsondata, headers = headers)
    print(response.json())
    total_val = response.json()['Total Value']

#v2 example
if __name__=="__main__":

    #first get auth token
    username = 'shopify'
    password = 'testing12'

    url = "https://shopify-janujan.herokuapp.com/api-token-auth/"
    body = { 'username':username , 'password':password }
    jsondata = json.dumps(body)
    headers = {'Content-type': 'application/json; charset=utf-8'}

    response = requests.post(url, jsondata, headers = headers)
    token = response.json()['token']
    print(token)

    # #create cart
    url = "https://shopify-janujan.herokuapp.com/commerce/v2/"
    cart_id = createCart(url, token)
    print(int(cart_id))

    #update the cart
    updateCart(url, int(cart_id), token)

    #complete the cart
    total_val = completeCart(url,int(cart_id), token)
