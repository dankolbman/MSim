"""
File:   dataIO.py
Name:   Dan Kolbman
Date:   Fall 2013
Description:
	A module for handling data read/writing.
"""

def writePositions(positions, filen):
	"""
	write particle positions to file.

	parameters:
		postitions - the particle positions
		filen - the file name to write to
	"""
	fileout = open(filen, 'w')
	for pos in positions:
		fileout.write(str(pos[0]))
		fileout.write(' ')
		fileout.write(str(pos[1]))
		fileout.write(' ')
		fileout.write(str(pos[2]))
		fileout.write('\n')
	fileout.close()

