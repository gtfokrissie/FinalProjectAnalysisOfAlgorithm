import math
entities = []
#for the green stuff that moves
class Entity:
    def __init__ (self):
        self.posX = 0
        self.posY = 0

        self.targetX = 0
        self.targetY = 0

        self.moveVectorX_norm = 0
        self.moveVectorY_norm = 0

        self.moveSpeed = 1

        self.timeSpeedup = 1

    def changeMoveSpeed (ms) :
        self.moveSpeed = ms

    def update (self) :
        flag = 0

        while flag < self.timeSpeedup:
            distanceToTarget = (abs(self.targetX - self.posX) + abs(self.targetY - self.posY))

            if distanceToTarget > 0.6 :
                self.posX += self.moveVectorX_norm * self.moveSpeed
                self.posY += self.moveVectorY_norm * self.moveSpeed
                
            flag += 1

    def changeTarget (self, x, y):
        self.targetX = x
        self.targetY = y

        mag = (x * x + y * y)
        mag = math.sqrt(mag)

        if mag != 0:
            self.moveVectorX_norm = (self.targetX - self.posX) / mag
            self.moveVectorY_norm = (self.targetY - self.posY) / mag

        return

def getEntities () :
    return entities

def newEntity (x, y) :
    tmp = Entity()

    tmp.posX = x
    tmp.posY = y

    tmp.targetX = x
    tmp.targetY = y

    entities.append(tmp)

    return tmp
