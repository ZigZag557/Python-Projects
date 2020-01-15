from sympy import *

x = Symbol('x')
f = Function('f')(x)
 
diff_eq = Derivative(f, x, 1) + f/2 - exp(x/3)/2


def firstOrder(fA, A, N):

	newDiffEq = diff_eq
	taylorEqStr = ""


	firstEq = diff_eq.subs(f,fA)
	firstEq = solve(firstEq, Derivative(fA, x, 1))[0]

	lastDerivative = [Derivative(f, x), firstEq]

	for k in range(N):

		eq = diff(diff_eq, x, k + 1 )
		eq = eq.replace(lastDerivative[0], lastDerivative[1])
		eq = solve(eq, Derivative(f, (x, k + 2)))[0]
		lastDerivative = [ Derivative(f, x, k + 2) ,eq.subs(x, A) ]
		print(lastDerivative)

firstOrder(1,1,3)