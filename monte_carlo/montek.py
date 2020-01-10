
import math
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

def func(x):
	return ((x**2)-1)/((x**2)+1)

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

plt.rc('axes', axisbelow=True)
fig, ax = plt.subplots()
ax.grid(True, which='both')

def monteCarloApprox(N, start, end):

	total = 0
	incrementAmt = (end - start)/(N)
	curXpos = start

	for _ in range(N):
		if curXpos >= 0:
			r = ptc.Rectangle((curXpos,0), incrementAmt, func(curXpos), color='blue', fill=False)
		else:
			r = ptc.Rectangle((curXpos,0), incrementAmt, func(curXpos + incrementAmt), color='blue', fill=False)

		ax.add_patch(r)

		curXpos += incrementAmt
		total += incrementAmt * func(curXpos)
	return total

points = getPoints(500,-15,15)

ax.axhline(y=0, color='k', zorder = -1)
ax.axvline(x=0, color='k', zorder = -1)
ax.plot(points[0],points[1], color= 'red')

approxVal = str(monteCarloApprox(500,-10,10))
ax.set_xlabel("Integral value is approximately: " + approxVal)
plt.show()

