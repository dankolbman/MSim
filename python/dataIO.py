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

def writeGofR(gofr, filen):
	"""
	Write g(r) data to file.
	
	Parameters:
		gofr - g(r) data
		filen - the file path
	"""
	fileout = open(filen, 'w')
	for dat in gofr:
		fileout.write(str(dat[0]))
		fileout.write(' ')
		fileout.write(str(dat[1]))
		fileout.write('\n')
	fileout.close()

def readGofR(path):
	""" Read g(r) file and return it """
	gofr = []
	filein = open(path,'r')
	for line in filein:
		line = line.split()
		gofr.append(line[1])
	filein.close()
	return gofr

def readPositions(path):
	"""
	Read particle positions from file
	
	Parameters:
		path - the file path
	Returns:
		a list of positions
	"""
	positions = []
	filein = open(path, 'r')
	for pos in filein:
		newPos = []
		line = pos.split()
		newPos.append( float(line[0]) )
		newPos.append( float(line[1]) )
		newPos.append( float(line[2]) )
		positions.append(newPos)
	filein.close()
	return positions
