# Shopify Commerce-Backend
A bare-bones back-end implementation of an online marketplace as described by the Shopify Intern Developer Challenge.

Table of Contents
-----------------

  * [Overview](#overview)
  * [Versions](#versions)
  * [Endpoints](#endpoints)
     * [Inventory List](#inventory-list)
     * [Inventory Detail](#inventory-detail)
   * [Security](#security)
   * [Setup](#setup)
   * [Next Steps](#next-steps)

## Overview
The purpose of this Django Web Application is to simulate an API for an online marketplace. My implementation uses a cart system to allow merchants to create, update and complete a cart object to organize customer purchases made to the marketplace back-end. The complete action for a cart can be considered the moment a customer has completed the transaction for the merchandise and allows the system to separate the financial transactions from the inventory management.

## Versions

There are two versions of the API that are available on this web application.

`commerce/v1/`

This endpoint is the most basic version of the API where a user can present an item and quantity and the inventory is adjusted immediately.

`commerce/v2/`

v2 supports the cart object. Inventory is only updated when the cart work flow is followed.

## Endpoints
### Inventory List
`commerce/v#/?avail=1`

Methods supported:
`GET` `POST`

This is the main endpoint to list all the items stored in the marketplace database.

The `GET` method lists all inventory. The query parameter `avail=1` results in only the available inventory to be returned (`inventory_count > 0`) .  In the absence of the query parameter, all inventory will be listed.

Ex:
`commerce/v1/?avail=1`

```javascript
[
    {
        "title": "pen",
        "price": 1.99,
        "inventory_count": 120
    },
    {
        "title": "shirt",
        "price": 10.99,
        "inventory_count": 167
    },
]    
```

**v1 `POST`**

The `POST` method requires a key-value pair listing the item information as follows:

```javascript
{
  "title" : "pen",
  "quantity" : 100
}
```
If a successful operation occurs, the response received will be a relay of the items passed through. A successful transaction will result in the item inventory_count updating at the `GET` endpoint.

*Note: If the quantity of an item passed through this endpoint exceeds the inventory_count available for the item, the operation will fail.*


**v2 `POST`**

Version 2 of the commerce API follows a cart workflow. The cart has three different states (`create`, `update`, `complete`) and each state is set by the command key in the json that is passed to the API.


*`create`*
A user must first create a cart using the create value. The user can also provide a name for the cart to give context as to what items might be in the cart.
```javascript
{
  "command" : "create",
  "cart_name" : "stationary"
}
```
Below is the resultant response after a create post is made to the API. The cart_id must be retained for the following steps in the cart workflow.

```javascript
{
  "cart_id" : 1
}
```

*`update`*
Once a cart has been provisioned, users can add items to the cart via the `update` command. Each item must be entered one at a time with the appropriate quantity for each item. A user can add a duplicate version of an item.
```javascript
{
  "command" : "update",
  "cart_id" : 1
  "title" : "pen",
  "quantity" : 5
}
```

*Note: If the quantity of an item order passed through this endpoint exceeds the inventory_count available for the item, the update will fail.*

*`complete`*
Finally, once all items have been added to the cart, the user can call the `complete` command and provide the cart  id. Once a cart has been completed, the inventory counts are updated and the cart can no longer be updated.
```javascript
{
  "command" : "complete",
  "cart_id" : 1
}
```
Once the cart has been completed, the return json response will detail the total value of the cart at the time of completion.
```javascript
{
  "message" : "cart complete!",
  "Total Value" : 14.95
}
```

*Note: A cart can only be completed once. An attempt at updating the cart, or completing the cart again will fail.*

 ### Inventory Detail
`commerce/v#/<str:title>/`

Methods supported:
`GET`

This API endpoint returns the item details for a given item title.

Ex:
`commerce/v2/pen/`
```javascript
{
    "title": "pen",
    "price": 1.99,
    "inventory_count": 120
}
```

## Security

To prevent unauthorized access to the API endpoints, a token based authentication is integrated into the API. With every `GET` and `POST` call to the API, a bearer token needs to be sent along with the payload to ensure that the API accepts the methods. To receive a token, the user must do the following.

The user must provide their account credentials as a key-value pair in the body of their request as shown below:
```javascript
{
	'username': 'user1',
	'password': 'userpassword'
}
```
The request must then be made to the url: `api-token-auth/`. The user must than store the token that is passed as a response. An example of the response can be seen below:
```javascript
{
	'token': 'd525e2211d3a8ad0044fdf289299f5ec7b1abca7'
}
```
With the token acquired, every call to the API needs to have the following key-value pair in the header of request.

```javascript
{
	'Authorization': 'Token d525e2211d3a8ad0044fdf289299f5ec7b1abca7'
}
```
## Setup

Details to an example script that performs the basic funcationality can be found in `v1_example.py`. The cart workflow can be found in `v2_example.py`.

## Next Steps

* Add a nice looking front-end
* Add throttling
* Integrate OAuth2.0
* Look into porting system with GraphQL
