import AStar
import Floodfill

class Pathfinder:
    def __init__ (self, algorithm, startingNode, endNode, heuristic) :
        if algorithm.upper() == 'A*' :
            self.solver = AStar.AStar(heuristic)
        elif algorithm.upper() == 'FLOODFILL' :
            self.solver = Floodfill.Floodfill()
        else :
            print('Invalid solver.')

        self.startingNode    = startingNode
        self.finalNode       = endNode
        self.onPathFound     = None
        self.paths           = []
        self.nodeIndexer     = None
        self.getNodeNeighbor = None
        self.isGoal          = None

    def pathFoundAction (self, paths) :
        self.paths = paths

        if self.onPathFound != None:
            self.onPathFound(paths)

    def goalFinder (self, a) :
        return self.isGoal(a, self.finalNode)

    def computePath (self) :
        self.solver.onPathFound = self.pathFoundAction

        self.solver.computePath(self.startingNode, self.nodeIndexer, self.getNodeNeighbor, self.goalFinder)
