"""
File:   nn.py
Name:   Dan Kolbman
Date:   Fall 2013
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
		dx = position[0] - pos[0]
		dy = position[1] - pos[1]
		dz = position[2] - pos[2]
		
		# Periodic boundaries
		if dx > size/2:
			dx = dx - size
		elif dx <= -size/2:
			dx + size
		if dy > size/2:
			dy = dy - size
		elif dy <= -size/2:
			dy = dy + size
		if dz > size/2:
			dz = dz - size
		elif dz <= -size/2:
			dz + size
		# Append to list if in range
		if sqrt(dx**2 + dy**2 + dz**2) < potrad*2:
			withinPot.append(pos)

	return withinPot
