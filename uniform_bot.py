import random

def think(state, quip):
	legalMoves = state.get_moves()
	quip("Is that all you got?")
	return random.choice(legalMoves)
