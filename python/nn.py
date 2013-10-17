"""
File:   nn.py
Name:   Dan Kolbman
Date:   10/11/2013
Description:
        A nearest neigbor search.
"""


def dist(pos1, pos2):
	"""
	The 3D pythagorean distance to a point
	
	Parameters:
		pos1 - point 1
		pos2 - point 2
	Returns:
		Distance between points
	"""
	return sqrt( (pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2 + (pos2[3]-pos1[3])**2 )

def searchRange( positions, position, potrad, size ):
	"""
	Return a list of partilces within the potential radius.
	TODO: Find alternative to brute force.
	
	Parameters:
		positions - the positions to search
		position - the position to search around
		potrad - the potential distance
	Returns:
		A list of particles within the potrad
	"""
	withinPot = []
	for pos in positions:
		if dist(position, pos) <= potrad:
			withinPot.append(pos)

	return withinPot




