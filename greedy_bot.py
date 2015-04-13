def think(state, quip):
	who = state.get_whos_turn()
	legalMoves = state.get_moves()
	bestScore = float("-inf")
	nextMove = None
	quipString = ""
	for move in legalMoves:
		nextState = state.copy()
		nextState.apply_move(move)
		if nextState.is_terminal():
			quipString = "Boxin' makes me feel good!"
		score = nextState.get_score()[who]
		if (score > bestScore):
			bestScore = score
			nextMove = move
	if quipString: quip(quipString)
	return nextMove
