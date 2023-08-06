"""parab.py: Parabola fit around three points to find a true vertex."""

import numpy as np


def fit_peak(f, x):
	'''
	Uses solution to parabola to fit peak and two surrounding points
	This assumes there is a peak (i.e. parabola second deriv is negative)
	
	Parameters
	----------
	f : array f(x)
	x : array x with the indices corresponding to f
	
	
	If interested, this is educational to see with sympy
	 import sympy
	 y1, y2, y3 = sympy.symbols('y1 y2 y3')
	 A = sympy.Matrix([[(-1)**2, -1, 1],[0**2, 0, 1],[(1)**2,1,1]]) 
	 C = sympy.Matrix([[y1],[y2],[y3]])
	 D = A.inv().multiply(C)
	 D contains the values of a, b, c in ax**2 + bx + c
	 Peak position is at x = -D[1]/(2D[0])   
	'''

	pk = np.argmax(f)

	y1 = f[pk - 1]
	y2 = f[pk]
	y3 = f[pk + 1]

	a = 0.5 * y1 - y2 + 0.5 * y3
	b = -0.5 * y1 + 0.5 * y3
	c = y2

	xindex = -b / (2 * a)
	findex = xindex * (x[1] - x[0]) + x[1]
	yindex = a * xindex ** 2 + b * xindex + c

	return findex, yindex, xindex


def ridge_finder(spectrogram, freq_bin):
	'''
	Uses parabolda to fit peak and two surrounding points
	This takes a spectrogram and the frequency bin spacing and wraps parab.fit_2d
	
	Parameters
	----------
	spectrogram : ndarray 
		Returned by scipy.signal.spectrogram or stft or cwt
		Arranged in (frequencies, times) shape
		
	freq_bin : ndarray
		arrays corresponding the frequencies in the spectrogram
		
	Returns
	-------
	xindex : ndarray
		1D array of the frequency bins returned by parabolic approximation
	yindex : ndarray
		1D array of the peak values at the xindices supplied
	'''
	_argmax = np.argmax(np.abs(spectrogram), axis=0)
	cols = spectrogram.shape[1]

	# generate a (3, cols) matrix of the spectrogram values
	maxspec = np.array([spectrogram[(_argmax - 1, range(cols))],
						spectrogram[(_argmax, range(cols))],
						spectrogram[(_argmax + 1, range(cols))]])

	return fit_2d(maxspec, _argmax, freq_bin)


def fit_2d(f, p, dx):
	'''
	Uses solution to parabola to fit peak and two surrounding points
	This assumes there is a peak (i.e. parabola second deriv is negative).
	
	This is a broadcast version for speed purposes
	
	Parameters
	----------
	f : 2-d array f(x) of size (3 , samples)
	
	p : 1-d array with the peak positions for f

	dx : 1-d array with the frequency (x values) of f
	'''

	if f.shape[0] != 3:
		raise ValueError('Must be exactly 3 rows')

	a = 0.5 * f[0, :] - f[1, :] + 0.5 * f[2, :]
	b = -0.5 * f[0, :] + 0.5 * f[2, :]
	c = f[1, :]

	xindex = -b / (2 * a)
	findex = xindex * (dx[1] - dx[0]) + dx[p]
	yindex = a * (xindex ** 2) + b * xindex + c

	return findex, yindex, xindex


def fit_peak_old(f, x):
	"""
	f = array
	x = index of peak, typically just argmax

	Uses parabola equation to fit to the peak and two surrounding points
	"""

	x1 = x - 1
	x2 = x
	x3 = x + 1

	y1 = f[x - 1]
	y2 = f[x]
	y3 = f[x + 1]

	d = (x1 - x3) * (x1 - x2) * (x2 - x3)

	A = (x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)) / d

	B = (x1 ** 2.0 * (y2 - y3) +
		 x2 ** 2.0 * (y3 - y1) +
		 x3 ** 2.0 * (y1 - y2)) / d

	C = (x2 * x3 * (x2 - x3) * y1 +
		 x3 * x1 * (x3 - x1) * y2 +
		 x1 * x2 * (x1 - x2) * y3) / d

	xindex = -B / (2.0 * A)
	yindex = C - B ** 2.0 / (4.0 * A)

	return xindex, yindex
