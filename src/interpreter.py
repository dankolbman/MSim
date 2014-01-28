"""
File: 	interpreter.py
Author:	Dan Kolbman
Description:
	A user interface for the simulation environment.
"""
import time
import os
import simulation as sim
import stats
import dataIO

class Setting():
	"""
	A Class for holding configuration settings.
	Properties
	- Name - the setting name
	- Value - the value of the setting
	- type - the type of the value stored
	- desc - description
	"""
	__slots__ = ('name','value','type','desc')

def mkSetting(conf, name, value, type, desc=''):
	""" Constructor for Setting type """
	nSetting = Setting()
	nSetting.name = name
	nSetting.value = value
	nSetting.type = type
	nSetting.desc = desc
	# Assign the setting to the dictionary
	conf[name] = nSetting
	return nSetting

##### End class definitions

def assignSetting(conf, string):
	""" assignSetting : Dict(Setting) String -> None
	Assigns a value to a setting and handles errors.
	Based on a 'setting value' string input'
	"""
	cmd = string.split()
	try:
		# Attempts to cast to the proper type
		conf[cmd[0]].value = conf[cmd[0]].type(cmd[1])
	except KeyError:	# The setting does not exist
		print('!!', cmd[0], 'is not a property.')
	except ValueError:	# The user tried to enter a different type than expected
		print('!! Could not assign. Was expecting type', conf[cmd[0]].type)

def defaultConfig():
	"""Returns the default configuration dictionary."""
	conf = dict()
	mkSetting(conf,'freq',5000,int,'The number of iterations between state saves')
	mkSetting(conf,'initIter',10000,int,'The number of iterations used to create an intial box')
	mkSetting(conf,'iter',25000,int,'The number of max iterations')
	mkSetting(conf,'initPath','data/test/init.pos',str,'The path to save the initial box to or load\n\
			from if useInit = True')
	mkSetting(conf,'useInit',False,bool,'Whether or not to start fro a prespecified file.')
	#mkSetting(conf,'keepPos',False,bool,'Whether or not to save inbetween box states,\n\
	#		0 = False, true otherwise')
	mkSetting(conf,'numPart',400,int,'The number of particles to run')
	mkSetting(conf,'size',1,int,'The size of the box')
	mkSetting(conf,'numBins',150,int,'The number of bins to use for g(r)')
	mkSetting(conf,'path', 'data/test/', str,'The path to save data output to')
	mkSetting(conf,'radSep', 0.984745, float,'The radial separaration')
	mkSetting(conf,'potRange', 0.121006, float,'The potential range')
	mkSetting(conf,'jumpSize', 0.05, float,'The jump size used to move a particle every step')
	
	return conf

def printConfig(conf):
	""" Prints the configuration output to terminal"""
	print('== Current Configuration ==')
	for key in conf:
		print('--', key, '=', conf[key].value) # Debug:,'\t',type(conf[key].value))
	print('===========================')

def saveConfig(conf, string):
	""" saveConfig : dict(conf) string -> None
	Save configuration to file
	"""
	cmd = string.split()
	try:
		dataIO.writeConfig(conf, cmd[1])
	except IndexError:
		print('!! Please specify a path')

def loadConf(conf, string):
	""" loadConf : dict(conf) string -> None
	Load a configuration from a file
	"""
	cmd = string.split()
	try:
		fin = open(cmd[1], 'r')
		for line in fin:
			assignSetting(conf, line)
		fin.close()
	except IndexError:
		print('!! Please specify a file path')
	except IOError:
		print('!! Problem reading file')

def printHelp(conf):
	""" Prints commands and properties """
	print('== Available Commands ==')
	print('-- average - average g(r) functions in the path')
	print('-- config - display current config')
	print('-- help - display this output')
	print('-- gofr - compute g(r) for boxes in the path')
	print('-- load path - load configuration from path')
	print('-- property value - change that property in the config')
	print('-- run - run simulation(s) with current config')
	print('-- save path - save the configuration to path')
	print('========================')
	print('Configuration properties:')
	for key in conf:
		print('--', key, '\t', conf[key].desc)
	print('========================')
	
def main():
	"""
	Main program loop
	Displays title and enters a terminal interface.
	User can enter commands here and run simulations.
	"""
	# Load a default configuration
	conf = defaultConfig()
	print('========================================')
	print('-------- Molecular Box Simulator -------')
	print('----------------------------------------')
	printConfig(conf)
	print('-- For a list of commands, enter "help"')
	running = True
	# Terminal loop
	while running:
		cmd = input('> ')
		cmdLower = cmd.lower()#.split()
		if cmdLower == 'exit':
			running = False
		elif cmdLower == 'config':
			printConfig(conf)
		elif cmdLower.split()[0] == 'save':
			saveConfig(conf, cmd)
		elif cmdLower.split()[0] == 'load':
			loadConf(conf, cmd)
		elif cmdLower == 'help':
			printHelp(conf)
		elif cmdLower == 'gofr':
			stats.GofRdir(conf)
		elif cmdLower.split()[0] == 'average':
			stats.avGofR(conf)
		elif len(cmd.split()) > 1:
			assignSetting(conf, cmd)	
		elif cmdLower == 'run':
			#runExperiment(conf)
			sim.runSimulation(conf)
		else:
			print('Command not found. Type \'exit\' to exit')

if __name__ == '__main__':
	main()
