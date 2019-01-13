# Shopify Commerce-Backend
A bare-bones back-end implementation of an online marketplace as described by the Shopify Intern Developer Challenge.

Table of Contents
-----------------

  * [Overview](#overview)
  * [Versions](#versions)
  * [Endpoints](#endpoints)
     * [Inventory List](#inventory-list)
     * [Inventory Detail](#inventory-detail)

## Overview
The purpose of this Django Web Application is to simulate an API for an online marketplace. My implementation uses a cart system to allow merchants to create, update and complete a cart object to organize customer purchases made to the marketplace back-end. The complete action for a cart can be considered the moment a customer has completed the transaction for the merchandise and allows the system to separate the financial transactions from the inventory management.

## Versions

There are two versions of the API that are available on this web application. 

`commerce/v1/` 

This endpoint is the most basic version of the API where a user 		can present an item and quantity and the inventory is adjusted immediately.

`commerce/v2/`

v2 supports the cart object. Inventory is only updated when the cart flow model is followed.

## Endpoints
**Inventory List**
`commerce/v#/?avail=1` 

Methods supported:
`GET` `POST`

This is the main endpoint to list all the items stored in the marketplace database. 

The `GET` method lists all inventory. The query parameter `avail=1` results in only the available inventory to be returned (`inventory_count > 0`) .  In the absence of the query parameter, all inventory will be listed.

**v1 `POST`**

The `POST` method requires a key-value pair listing the item information as follows:

```javascript
{
  "title" : "pen",
  "quantity" : 100
}
```
If a successful operation occurs, the response recieved will be a relay of the items passed through. A successful transaction will result in the item inventory_count updating at the `GET` endpoint.

*Note: If the quantity of an item passed through this point exceeds the inventory_count available for the item, the transaction will fail.*


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
*`complete`*
Finally, once all items have been added to the cart, the user can call the `complete` command and provide the cart  id. Once a cart has been completed, the inventory counts are updated and the cart can no longer be updated.
```javascript
{
  "command" : "complete",
  "cart_id" : 1
}
```
 **Inventory Detail**
`commerce/v#/<str:title>/`

Methods supported:
`GET` 

This API endpoint returns the item details for a given item title. 

Ex:
`commerce/v2/pen/`

