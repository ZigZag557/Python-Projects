
import matplotlib.pyplot as plt
import matplotlib.patches as ptc



# Function to be integrated.
def func(x):
	return ((x**2)-1)/((x**2)+1)
#-----------------------------



# Get N amount of (x,y) points on the function from the starting point to the end point.

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

#------------------------------------------------------------

# Make axes below the graphs.
plt.rc('axes', axisbelow=True)

# Enable multi graph drawing.
fig, ax = plt.subplots()

# Enable grids.
ax.grid(True, which='both')


# Draw N amount of rectangles with same width under the graph from the start point to the end point.
# Return sum of the rectangles' area.
def riemannSum(N, start, end):

	total = 0
	incrementAmt = (end - start)/(N)
	curXpos = start

	for _ in range(N):
		r1 = ptc.Rectangle((curXpos,0), incrementAmt, func(curXpos), color='blue', fill=False)
		r2 = ptc.Rectangle((curXpos,0), incrementAmt, func(curXpos + incrementAmt), color='blue', fill=False)

		if curXpos >= 0:
			if func(curXpos) >= 0:
				ax.add_patch(r1)
			else:
				ax.add_patch(r2)
		else:
			if func(curXpos) >= 0:
				ax.add_patch(r2)
			else:
				ax.add_patch(r1)


		curXpos += incrementAmt
		total += incrementAmt * func(curXpos)
	return total
#-------------------------------------------------------------------------------------------------


# Draw x and y axes.
ax.axhline(y=0, color='k', zorder = -1)
ax.axvline(x=0, color='k', zorder = -1)

#Draw the graph.
points = getPoints(1200,-15,15)
approxVal = str(riemannSum(2000,-10,10))


# Draw the rectangles and write approximated integral value.
ax.plot(points[0],points[1], color= 'red')
ax.set_xlabel("Integral value is approximately: " + approxVal)

plt.show()

