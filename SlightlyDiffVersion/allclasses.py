from operator import methodcaller
from random import randint,randrange

class Person:
    numMade = 0

    def __init__(self,name,country,age = None):
        self.__name = name
        self.__ID = Person.numMade
        self.__country = country
        Person.numMade += 1
        self.__age = age
        self.__health = "healthy"
        self.__neighbor = []
        self.__location = None

    def setLocation(self, x, y): self.__location = [x, y]

    def getLocation(self): return self.__location[0], self.__location[1]

    def getName(self):
        return self.__name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def getID(self): return self.__ID

    def getAge(self): return self.__age

    def setAge(self,age):
        self.__age = age

    def getCountry(self): return self.__country

    def getNeighbor(self): return self.__neighbor

    def countNeighbor(self): return len(self.__neighbor)

    def hasNoNeighbor(self):
        if self.countNeighbor() == 0:
            return True

    def addNeighbor(self,neighbor):
        self.__neighbor.append(neighbor)

    def removeNeighbor(self,neighbor):
        self.__neighbor.remove(neighbor)

    def infect(self):
        self.__health = "infected"

    def isInfected(self):
        if self.__health == "infected":
            return True

    def inoculate(self):
        self.__health = "inoculated"

    def isVaccinated(self):
        if self.__health == "inoculated":
            return True

    def isInfectable(self):
        if self.__health == "healthy":
            return True

    def lessConnectedThan(self,other):
        if self.countNeighbor() < other.countNeighbor():
            return True
        return False


class Graph:
    def __init__(self):
        self.__name = None
        self.__size = 0
        self.__nodes = []
        self.__edges = []
        self.__infectedNodes = []
        self.__roundsOfInfection = 0
        self.__inoculatedNodes = []
        self.__criticalEdges = []
        self.__subGraphs = []
        self.__levelsOfInfection = []
        self.sortedCandidates = []
        self.dict = {}
        self.otherCountry = None  # the other country

    def setName(self, name):
        self.__name = name

    def getName(self): return self.__name

    def getNodes(self): return self.__nodes

    def getEdges(self): return self.__edges

    def infectionState(self): return self.__infectedNodes

    def infectionDuration(self): return self.__roundsOfInfection

    def getInfectedNodes(self): return self.__infectedNodes

    def getInoculatedNodes(self): return self.__inoculatedNodes

    def getCriticalEdges(self): return self.__criticalEdges

    def getClusters(self): return self.__subGraphs

    def getLevelsOfInfection(self): return self.__levelsOfInfection

    def getRound(self): return self.__roundsOfInfection

    def setOtherCountry(self,country):
        self.otherCountry = country

    def __str__(self):
        res = ">>> Country: "+self.getName()+"\n\tPopulation: "
        for k in self.__nodes:
            res += str(k) + ", "
        res += "\n\tConnections: "
        for edge in self.__edges:
            res += str(edge) + ", "
        res += "\n"
        return res

    def __repr__(self):
        res = ">>> Country: "+self.getName()+"\n\tPopulation: "
        for k in self.__nodes:
            res += str(k) + ", "
        res += "\n\tConnections: "
        for edge in self.__edges:
            res += str(edge) + ", "
        res += "\n"
        return res

    def isEmpty(self):
        if self.__size == 0:
            return True

    def addNode(self,node):
        if node in self.__nodes:
            print("Node already exists.")
            return None
        self.__nodes.append(node)
        self.__size += 1
        self.createEdges()

    def addNodeList(self,nodeList):
        self.__nodes = nodeList
        self.createEdges()
        self.__size += len(nodeList)

    def createEdges(self):
        self.__edges = []
        for node in self.__nodes:
            for neighbor in node.getNeighbor():
                if (neighbor, node) not in self.__edges:
                    self.__edges.append((node,neighbor))

    def BFS(self,node=None,data=None,returnList=None):
        if self.isEmpty():
            return None
        queue = []
        visited = []
        if node is None:
            node = self.getNodes()[0]
        queue.append(node)
        visited.append(node)
        while len(queue) != 0:
            node = queue.pop(0)
            for neighbor in node.getNeighbor():
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)
            if data is not None:
                if node.getName() == data:
                    return node
            else:
                continue
        if returnList:
            return visited
        elif len(visited) == len(self.getNodes()):
            return True

    def find(self, data):
        return self.BFS(None, data)

    def isConnected(self):
        return self.BFS()

    def getTraversedList(self):
        return self.BFS(None,None,True)

    def BFStime(self,node):
        return self.BFS(node,None,None)

    def makeCluster(self,node):
        nodeList = self.BFS(node,None,True)
        cluster = Graph()
        cluster.addNodeList(nodeList)
        self.__subGraphs.append(cluster)
        return cluster

    def findCluster(self):
        for edge1 in self.getEdges():
            for edge2 in self.getEdges():
                if edge2 != edge1:
                    edge1[0].removeNeighbor(edge1[1])
                    edge1[1].removeNeighbor(edge1[0])
                    edge2[0].removeNeighbor(edge2[1])
                    edge2[1].removeNeighbor(edge2[0])
                    if not self.isConnected():
                        if (edge2,edge1) not in self.__criticalEdges:
                            self.__criticalEdges.append((edge1,edge2))
                    edge1[0].addNeighbor(edge1[1])
                    edge1[1].addNeighbor(edge1[0])
                    edge2[0].addNeighbor(edge2[1])
                    edge2[1].addNeighbor(edge2[0])
        if len(self.__criticalEdges) == 0:
            print(">>> No clusters are found in this graph.")
        else:
            print(">>> Clusters are found!\n>>>", str(len(self.__criticalEdges)*2), "critical edge(s):",
                  str(self.__criticalEdges))
        return self.__criticalEdges

    def splitGraph(self,edgeList):
        for edge in edgeList:
            edge[0][0].removeNeighbor(edge[0][1])
            edge[0][1].removeNeighbor(edge[0][0])
            edge[1][0].removeNeighbor(edge[1][1])
            edge[1][1].removeNeighbor(edge[1][0])
        graphNodes = self.getNodes()[:]
        while len(graphNodes) != 0:
            cluster = self.makeCluster(graphNodes[0])
            for node in cluster.getNodes():
                graphNodes.remove(node)
        for edge in edgeList:
            edge[0][0].addNeighbor(edge[0][1])
            edge[0][1].addNeighbor(edge[0][0])
            edge[1][0].addNeighbor(edge[1][1])
            edge[1][1].addNeighbor(edge[1][0])
        return self.__subGraphs

    def findTarget(self,edgeList):
        candidates = []
        for edge in edgeList:
            candidates.append(edge[0][0])
            candidates.append(edge[0][1])
            candidates.append(edge[1][0])
            candidates.append(edge[1][1])
        temp = sorted(candidates,key = methodcaller("countNeighbor"),reverse=True)
        midIndex = len(temp)//5
        for n in range(midIndex):
            target = temp[randint(0,4)]
            if target not in self.sortedCandidates:
                self.sortedCandidates.append(target)
                self.otherCountry.getNodes()[0].addNeighbor(target)
        return candidates,self.sortedCandidates

    def sort(self):
        toBeSorted = self.getNodes()
        alreadySorted = sorted(toBeSorted,key=methodcaller("countNeighbor"),reverse=True)
        return alreadySorted

    def infectTarget(self):
        for target in self.sortedCandidates:
            target.infect()
            self.__infectedNodes.append(target)
        self.__roundsOfInfection += 1
        return self.__infectedNodes

    def spreadInfection(self):
        self.dict = {}
        temp = self.getInfectedNodes()[:]
        if len(temp) == 0:
            self.dict[self.otherCountry.getNodes()[0]] = self.sortedCandidates # for GUI
            return self.infectTarget()
        for source in temp:
            self.dict[source] = []
            for neighbor in source.getNeighbor():
                if neighbor not in temp:
                    self.dict[source].append(neighbor)
                    if neighbor.isInfectable():
                        neighbor.infect()
                        self.__infectedNodes.append(neighbor)
        self.__roundsOfInfection += 1
        return self.__infectedNodes
        # if self.__roundsOfInfection > 2:
        #     self.inoculation()
        #     return self.__infectedNodes,self.__inoculatedNodes
        # else:


    def getDict(self): return self.dict

    def inoculation(self):
        temp = []
        for node in self.__infectedNodes:
            if node.hasNoNeighbor():
                continue
            for neighbor in node.getNeighbor():
                if neighbor.isInfectable():
                    temp.append(neighbor)
        for node in temp:
            if node.hasNoNeighbor():
                continue
            for neighbor in node.getNeighbor():
                if neighbor.isInfectable():
                    neighbor.inoculate()
                    self.__inoculatedNodes.append(neighbor)

    def totalInfect(self, nodeList, time):
        self.__levelsOfInfection = [[] for x in range(time)]
        for t in range(time):
            if t == 0:
                for node in nodeList:
                    if node.isInfectable():
                        node.infect()
                        self.__levelsOfInfection[t].append(node)
        #     elif t >= 1:
        #         for node in self.__levelsOfInfection[t - 1]:
        #             if node.hasNoNeighbor():
        #                 continue
        #             for neighbor in node.getNeighbor():
        #                 if neighbor.isInfectable():
        #                     self.__levelsOfInfection[t].append(neighbor)
        #                     neighbor.infect()
        # return self.__levelsOfInfection