
#--------------------------------------
# TODO: Mix first and second order functions into one.
#--------------------------------------


from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as ptc


x = Symbol('x')
f = Function('f')(x)


# Make axes below the graphs.
plt.rc('axes', axisbelow=True)

# Enable multi graph drawing.
fig, ax = plt.subplots()

# Enable grids.
ax.grid(True, which='both')

# Draw x and y axes.
ax.axhline(y=0, color='k', zorder = -1)
ax.axvline(x=0, color='k', zorder = -1)


def firstOrderTaylorEq(fA, A, N, function):

	taylorEq = fA

	#First derivative is problematic in the for loop so we do it here.
	firstEq = function.subs(f,fA)
	firstEq = solve(firstEq, Derivative(fA, x, 1))[0]

	lastDerivative = [Derivative(f, x), firstEq]
	#--------------------------------------------

	# Find the value of (k+2)th derivative and then expand the taylor series (N-1) times.
	for k in range(N - 1):

		# Finding the value of (k+2)th derivative.
		eq = diff(function, x, k + 1 )
		eq = eq.replace(lastDerivative[0], lastDerivative[1])
		eq = solve(eq, Derivative(f, (x, k + 2)))[0]
		eqDerivativeVal = eq.subs(x, A)

		# Store the (k+2)th derivative so it can be used to find the value of (k+3)th derivative.
		lastDerivative = [ Derivative(f, x, k + 2), eqDerivativeVal ]

		#Expand the taylor series.
		taylorEq += (eqDerivativeVal * (x-A)**(k+1))/factorial(k+1)

	print(taylorEq)
	drawFunction(500, -20, 20, taylorEq)


def secondOrderTaylorEq(fA, f1A, A, N, function):

	taylorEq = fA

	#First derivative is problematic in the for loop so we do it here.
	firstEq = function.subs(f, fA)
	firstEq = solve(firstEq, Derivative(fA, x, 2))[0]

	higherFuncVal = firstEq
	lesserFuncVal = f1A
	#-------------------------------------------------------------------

	# Find the value of (k+2)th derivative and then expand the taylor series (N-1) times.
	for k in range(N-1):

		# Finding the value of (k+2)th derivative.
		eq = diff(function, x, k + 1 )
		eq = eq.replace(Derivative(f, x, k + 2), higherFuncVal)
		eq = eq.replace(Derivative(f, x, k + 1), lesserFuncVal)
		eq = solve(eq, Derivative(f, x, k + 3))[0]
		eqDerivativeVal = eq.subs(x, A)

		# Store both values of (k+2)th and (k+3)th derivative so it can be used to find the value of (k + 4)th derivative.
		lesserFuncVal = higherFuncVal
		higherFuncVal = eqDerivativeVal

		#Expand the taylor series.
		taylorEq += (eqDerivativeVal * (x-A)**(k))/factorial(k)

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


# Tests
eq = f + Derivative(f, x) + (Derivative(f, x, 2) + exp(x/2)) + 5*x**4
secondOrderTaylorEq(-20, 1, 0, 5, eq)
secondOrderTaylorEq(-10, 1, 0, 5, eq)
secondOrderTaylorEq(0, 1, 0, 5, eq)
secondOrderTaylorEq(10, 1, 0, 5, eq)
secondOrderTaylorEq(20, 1, 0, 5, eq)
#----------------------------------------------------------------------

plt.show()