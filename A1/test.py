a = [17, 27 ,37]
b = [10, 20, 30]
c = [a,b]

x = ['a', 'b', 1]
y = ['z',2, 'y']
z = [x,y]

for i,j,k in c:
	print("loop")
	print(i)
	print(j)
	print(k)
	print(i + j)
	print(i + k)
	print(j + k)

print("part 2")

for i in z:
	for j in z:
		print(i+j)