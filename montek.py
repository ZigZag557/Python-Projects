

import matplotlib.pyplot as plt


def func(x):
	return x**2

def getPoints(N,start,end):
	xPoints = []
	yPoints = []
	incrementAmt = (end - start)/(N-1)

	curXpos = start - incrementAmt

	for _ in range(N):
		curXpos += incrementAmt
		xPoints.append(curXpos)
		yPoints.append( func(curXpos) )

	return [xPoints,yPoints]

def monteCarloApprox(N, start, end):

	total = 0
	incrementAmt = (end - start)/(N-1)
	curXpos = start

	for _ in range(N):
		curXpos += incrementAmt
		total += incrementAmt * func(curXpos)

	return total

points = getPoints(100,-20,20)
plt.plot(points[0],points[1])
print(monteCarloApprox(450, 0, 1))
plt.show()

