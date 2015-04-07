from p2_gui import rungui
from p2_sim import runsim

# Standard format for help option message
def default(str):
	return str + ' [Default: %default]'

# Import an AI module
def loadAIModule(moduleName):
	try:
		module = __import__(moduleName)
	except ImportError:
		print 'Error: The AI module "' + moduleName + '" could not be loaded!'
		traceback.print_exc()
		return None

	# Ensure that module has required API
	if hasattr(module, 'think'):
		return module
	else:
		print 'Error: The AI module "' + moduleName + '" does not have a think function!'
		return None


if __name__ == '__main__':
	# Add command line options
	from optparse import OptionParser
	usageStr = """     python %prog <options>
Examples:   (1) python %prog
                - starts a GUI game with AI opponents set to first_bot (default)
            (2) python %prog -r first_bot -b my_bot
                - starts a GUI game with given bots controlling AI
            (3) python %prog -r first_bot -b my_bot -n 100
                - simulates 100 games between first_bot and my_bot
"""
	parser = OptionParser(usageStr)

	parser.add_option('-r', '--red', help=default('Red team AI module'), default='first_bot')
	parser.add_option('-b', '--blue', help=default('Blue team AI module'), default='first_bot')
	parser.add_option('-n', '--numGames', help='Simulate NUMGAMES between AI modules (no GUI)', type='int', default=1)

	(options, args) = parser.parse_args()

	# Load the bots
	red_bot = loadAIModule(options.red)
	blue_bot = loadAIModule(options.blue)

	if options.numGames > 1:
		# Run simulations for multiple games
		runsim(options.numGames, red_bot, blue_bot)
	else:
		# Play in GUI
		rungui(red_bot, blue_bot)
