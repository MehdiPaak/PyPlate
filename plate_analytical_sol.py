"""
comput analytical response of a simply-supported (SSSS) plate under uniform load
By: Mehdi Paak
"""

import numpy as np

def w(x,y,a,b,h,nu,E,P0):
	"""
	deflextion of the plate at x,y
	units are SI meter

	:param x:
	:param y:
	:param a:
	:param b:
	:param h:
	:param nu:
	:param E:
	:param P0:
	:return:  deflection
	"""
	# 10 is a reasonable value for the analytical solution
	num_mode = 10

	D=E*h**3/(12.0*(1-nu**2))
	alph = 16.0*P0/(D*np.pi**6)
	N=[2*i+1 for i in range(num_mode)]
	M = N
	w=0.0
	
	for m in M:
		for n in N:
			beta = m*n*((m/a)**2+(n/b)**2)**2
			w = w +  (1.0/beta) * np.sin(m*np.pi*x/a) * np.sin(n*np.pi*y/b)
	w = w * alph	
	return w


def wmax_nondim():
	"""
	returns nondimensional maximum deflection which
	is Wmax/(p0*a**4/D)
	D=E*h**3/(12(1-nu**2))

	:return:
	"""

	# 10 is a reasonable value for the analytical solution
	num_mode = 10
	alph = 16.0/np.pi**6
	
	N=[2*i+1 for i in range(num_mode)]
	M=N
	wmax = 0.0

	for m in M:
		for n in N:
			beta = m*n*(m**2+n**2)**2
			wmax = wmax +  (1.0/beta) * (-1.0)**((m+n-2)/2)
	return wmax*alph




