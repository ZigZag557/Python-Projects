

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as ptc


x = Symbol('x')
f = Function('f')(x)
 
diff_eq = Derivative(f, x) + f/2 + x


# Make axes below the graphs.
plt.rc('axes', axisbelow=True)

# Enable multi graph drawing.
fig, ax = plt.subplots()

# Enable grids.
ax.grid(True, which='both')

# Draw x and y axes.
ax.axhline(y=0, color='k', zorder = -1)
ax.axvline(x=0, color='k', zorder = -1)


def firstOrderTaylorEq(fA, A, N):

	newDiffEq = diff_eq
	taylorEq = fA

	#First derivative is problematic in the for loop so we do it here.
	firstEq = diff_eq.subs(f,fA)
	firstEq = solve(firstEq, Derivative(fA, x, 1))[0]

	lastDerivative = [Derivative(f, x), firstEq]
	#--------------------------------------------

	for k in range(N - 1):

		eq = diff(diff_eq, x, k + 1 )
		eq = eq.replace(lastDerivative[0], lastDerivative[1])
		eq = solve(eq, Derivative(f, (x, k + 2)))[0]
		eqDerivativeVal = eq.subs(x, A)
		lastDerivative = [ Derivative(f, x, k + 2), eqDerivativeVal ]

		taylorEq += (eqDerivativeVal * (x-A)**(k+1))/factorial(k+1)
	print(taylorEq)
	drawFunction(500, -20, 20, taylorEq)


def drawFunction(N,start,end, function):
	xPoints = []
	yPoints = []
	incrementAmt = (end - start)/(N-1)

	curXpos = start - incrementAmt

	for _ in range(N):
		curXpos += incrementAmt
		xPoints.append(curXpos)
		yPoints.append( function.subs(x, curXpos) )

	ax.plot(xPoints, yPoints, color = "blue")


firstOrderTaylorEq(-20,0,40)
firstOrderTaylorEq(-10,0,40)
firstOrderTaylorEq(0,0,40)
firstOrderTaylorEq(10,0,40)
firstOrderTaylorEq(20,0,40)


plt.show()