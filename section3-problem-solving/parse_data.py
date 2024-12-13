#!/usr/bin/env python

#dummy data or data from an API
datas = [
    {"id": 1, "category": "electronics", "price": 199.99},
    {"id": 2, "category": "clothing", "price": 49.99},
    {"id": 3, "category": "electronics", "price": 299.99},
    {"id": 4, "category": "electronics", "price": 99.99},
    {"id": 5, "category": "clothing", "price": 19.99}
]

parameter = "electronics" #parameter if we need another category to be calculated

#calculating average price for item category
if datas:
    qty = 0 #reset value
    prices = 0 #reset value
    for data in datas: #iterate all data
        if data["category"] == parameter: #condition for the parameter to be calculated
            qty += 1
            prices += data["price"]
    
    #printing result
    if qty > 0:
        avg = prices / qty
        print(f"Average price of {parameter} is {avg:.2f}")
    else:
        print(f"No items found for the category: {parameter}")
