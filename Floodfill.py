# Helper function to create new compute state
def createState (node, parent) :
    return ({
        'node': node,
        'parent': parent
    })

class Floodfill:
    def __init__ (self) :
        self.onPathFound = None
        self.searchCount = 0

    # Find path with floodfill
    def computePath (self, startingNode, nodeIndexCreator, getNodeNeighbor, isGoal) :
        print('Searching path with floodfill')
        openStack = [
            createState(
                startingNode,
                None
            )
        ]

        closedStack  = []
        checkedIndex = []

        while len(openStack) != 0 :
            # Get next top state from the stack
            currentState = openStack.pop()

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
                        currentState
                    )

                    # Add new state to the open stack
                    openStack.append(newState)
