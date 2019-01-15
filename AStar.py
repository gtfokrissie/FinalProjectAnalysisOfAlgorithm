# Default heuristics
def manhattanDistance (a, b) :
    return ( abs(a[0] - b[0]) + abs(a[1] - b[1]) )

# Helper function to create new compute state
def createState (node, parent, score) :
    return ({
        'node': node,
        'parent': parent,
        'score': score,
        'depth': 0
    })

class AStar:
    def __init__ (self, heur) :
        self.heuristic = heur
        self.onPathFound = None
        self.searchCount = 0

    # Find path with A*
    def computePath (self, startingNode, nodeIndexCreator, getNodeNeighbor, isGoal) :
        print('Searching path with A*')
        openStack = [
            createState(
                startingNode,
                None,
                0
            )
        ]

        closedStack  = []
        checkedIndex = []

        while len(openStack) != 0 :
            # Get next top state from the priority queue
            currentState = openStack.pop(0)

            # Get the current node's index
            boardIndex   = nodeIndexCreator(currentState['node'])

            if isGoal(currentState['node']) :
                print('Searched ' + str(self.searchCount) + ' node(s)')
                goalNode = []
                returnPaths = []

                while currentState['parent'] != None :
                    goalNode.append(currentState['node'])
                    currentState = currentState['parent']

                goalNode.append(startingNode)
                for node in reversed(goalNode):
                    returnPaths.append(node)

                self.onPathFound(returnPaths)
                break

            if boardIndex not in checkedIndex :
                # Increment node search count
                self.searchCount += 1
                
                # Add current state to the closed state
                closedStack.append(currentState)

                # Add state index to do not check
                checkedIndex.append(boardIndex)

                # Get current state's node neighbor
                nodeNeighbors = getNodeNeighbor(currentState['node'])

                for neighbor in nodeNeighbors:
                    newState = createState(
                        neighbor,
                        currentState,
                        self.heuristic(neighbor, startingNode)
                    )

                    newState['depth'] = currentState['depth'] + 1

                    # Add new state to the open priority queue
                    openStack.append(newState)

                    # Sort the open stack
                    openStack.sort(key = lambda x : x['score'])
