
from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as ptc


x = Symbol('x')

primaryFunction = sin(x)


def getFuncPoints(N,start,end, function):
	xPoints = []
	yPoints = []
	incrementAmt = (end - start)/(N-1)

	curXpos = start - incrementAmt

	for _ in range(N):
		curXpos += incrementAmt
		xPoints.append(curXpos)
		yPoints.append( function.subs(x, curXpos) )

	return [xPoints,yPoints]


def getTaylorFunc(N, a):

	funcStr = str(primaryFunction.subs(x, a))
	curFuncDer = primaryFunction

	for i in range(N):
		curFuncDer = diff(curFuncDer)
		funcStr += " + " + str( (curFuncDer.subs(x, a) * (x-a)**(i+1))/factorial(i+1) )

	print(simplify(sympify(funcStr)))
	return simplify(sympify(funcStr))



plt.rc('axes', axisbelow=True)

fig, ax = plt.subplots()
ax.grid(True, which='both')
ax.axhline(y=0, color='k', zorder = -1)
ax.axvline(x=0, color='k', zorder = -1)

points = getFuncPoints(500,-20, 20, primaryFunction)
ax.plot(points[0],points[1], color= 'red')

taylorFunc = getTaylorFunc(11, 0)
taylorPoints = getFuncPoints(500,-5,5, taylorFunc)
ax.plot(taylorPoints[0], taylorPoints[1], color= 'blue')

if len(str(taylorFunc)) < 80:
	ax.set_xlabel("y = " + str(taylorFunc))

plt.show()