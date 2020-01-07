"""
To run this script:
	python shoppingCost.py

If you run the above script, a correct calculateShoppingCost function should return:

The final cost for our shopping cart is 35.58
"""

import csv

def calculateShoppingCost(productPrices, shoppingCart):
	finalCost = 0
	"*** Add your code in here ***"
	for x in shoppingCart:
		itemNum = float(shoppingCart[x])
		itemPrice = float(productPrices[x])
		itemCost = itemNum*itemPrice
		finalCost += itemCost
	return finalCost


def createPricesDict(filename):
	productPrice = {}
	"*** Add your code in here ***"
	with open(filename) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			productPrice[row[0]] = row[1]
	return productPrice


if __name__ == '__main__':
	prices = createPricesDict("Grocery.csv")
	myCart = {"Bacon": 2,
		      "Homogenized milk": 1,
		      "Eggs": 5}
	print("The final cost for our shopping cart is {}".format(calculateShoppingCost(prices, myCart)))
