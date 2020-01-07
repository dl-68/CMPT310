"""
To run this script:
	python EvenOdd.py

In order to pass the autograder your function should
return a list of even numbers given any list of integers.
If you run the above script, a correct function should return:

Even numbers are [2, 4]

Feedback
At the moment, the most difficult section is understanding and
comparing the various different searching algorithm. The topic
I look forward to is neural networks. It is a topic I want to 
build a better understanding of. If you include reading various
python tutorials, then I have spent ~ 3 hours on this assignment.


"""

def getEvenNumbers(numbers):
	evens = []
	"*** Add your code in here ***"
	for x in numbers:
		if (x % 2) == 0:
			evens.append(x)

	return evens


if __name__ == '__main__':
	myList = [1, 2, 3, 4, 5]
	print("Even numbers are {}".format(getEvenNumbers(myList)))