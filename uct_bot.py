import random
import time
from math import sqrt, log

def think(state, quip):
    return UCT(state, 1.0, True)

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerJustMoved = state.get_player_just_moved() # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = max(self.childNodes, key=lambda c: float(c.wins) / float(c.visits) + sqrt(2 * log(float(self.visits)) / float(c.visits)))
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def UCT(rootstate, think_duration, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    t_start = time.time()
    t_now = t_start
    t_deadline = t_start + think_duration

    iterations = 0

    while t_now < t_deadline:
        iterations += 1
        node = rootnode
        state = rootstate.copy()

        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.apply_move(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []: # while state is non-terminal
            state.apply_move(random.choice(state.get_moves()))

        # Backpropagate
        scores = state.get_score()
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(scores[node.playerJustMoved]) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

        t_now = time.time()

    # Output some information about the tree - can be omitted
    if (False): print rootnode.TreeToString(0)
    else: pass#print rootnode.ChildrenToString()

    sample_rate = float(iterations)/(t_now - t_start)

    if verbose: print "Sample rate: ", sample_rate

    return max(rootnode.childNodes, key=lambda c: c.visits).move # return the move that was most visited

