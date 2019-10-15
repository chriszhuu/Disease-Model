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

    def getName(self): return self.__name

    def __str__(self): return self.__name

    def __repr__(self): return self.__name

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


class Graph:
    def __init__(self):
        self.__name = None
        self.__size = 0
        self.__nodes = []
        self.__edges = []
        self.__infectedNodes = []
        self.__roundsOfInfection = 0  # counts units of time passed
        self.__inoculatedNodes = []
        self.__criticalEdges = []
        self.__subGraphs = []  # list of clusters in the graph
        self.__levelsOfInfection = []  # list of lists containing result from all stages of infection
        self.sortedCandidates = []  # the first group to be infected
        self.dict = {}  # for GUI purposes
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
        '''constructs all edges based on each node's list of neighbors'''
        self.__edges = []
        for node in self.__nodes:
            for neighbor in node.getNeighbor():
                if (neighbor, node) not in self.__edges:
                    self.__edges.append((node,neighbor))

    def BFS(self,node=None,data=None,returnList=None):
        '''a multipurpose method that uses BFS, can be used to:
        check if graph is connected or not;
        find node in the graph that contains particular data
        traverse graph from a particular node and return all visited nodes'''
        if self.isEmpty():
            return None
        queue = []
        visited = []
        if node is None:  # if the starting node is unspecified
            node = self.getNodes()[0]  # start traversal from the first node in nodeList
        queue.append(node)
        visited.append(node)
        while len(queue) != 0:
            node = queue.pop(0)
            for neighbor in node.getNeighbor():
                if neighbor not in visited:
                    queue.append(neighbor)  # standard BFS stuff
                    visited.append(neighbor)
            if data is not None:  # if there is specific data we want to search for
                if node.getName() == data:  # find the node and return it
                    return node
            else:
                continue
        if returnList:  # if parameter includes returnList
            return visited  # return all visited nodes
        elif len(visited) == len(self.getNodes()):
            return True  # checking if graph is still connected or not

    def find(self, data):
        '''find node in the graph that contains particular data'''
        return self.BFS(None, data)

    def isConnected(self):
        '''check if graph is connected or not'''
        return self.BFS()

    def getTraversedList(self):
        '''traverse graph from a particular node and return all visited nodes'''
        return self.BFS(None,None,True)

    def makeCluster(self,node):
        '''make subgraphs by traversing from a particular node'''
        nodeList = self.BFS(node,None,True)
        cluster = Graph()
        cluster.addNodeList(nodeList)
        self.__subGraphs.append(cluster)
        return cluster

    def findCluster(self):
        '''find critical edges by brute force :(
        cut each edge and use BFS to check if graph is still connected or not
        (knows a priori that clusters are connected by two edges)'''
        for edge1 in self.getEdges():
            for edge2 in self.getEdges():
                if edge2 != edge1:
                    edge1[0].removeNeighbor(edge1[1])
                    edge1[1].removeNeighbor(edge1[0])
                    edge2[0].removeNeighbor(edge2[1])
                    edge2[1].removeNeighbor(edge2[0])
                    if not self.isConnected():
                        # if graph becomes disconnected, we got a pair of critical edges
                        if (edge2,edge1) not in self.__criticalEdges:
                            # undirected graph, thus need to filter out duplicate edges
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
        '''cut critical edges and make clusters'''
        for edge in edgeList:
            edge[0][0].removeNeighbor(edge[0][1])
            edge[0][1].removeNeighbor(edge[0][0])
            edge[1][0].removeNeighbor(edge[1][1])
            edge[1][1].removeNeighbor(edge[1][0])
        graphNodes = self.getNodes()[:] # copy a list of all nodes that are not yet traversed
        while len(graphNodes) != 0:
            cluster = self.makeCluster(graphNodes[0])
            # traverse from one of the remaining nodes in list and make cluster
            for node in cluster.getNodes():
                graphNodes.remove(node) # remove traversed nodes from list
        for edge in edgeList:
            edge[0][0].addNeighbor(edge[0][1])
            edge[0][1].addNeighbor(edge[0][0])
            edge[1][0].addNeighbor(edge[1][1])
            edge[1][1].addNeighbor(edge[1][0]) # restore the critical edges
        return self.__subGraphs

    def findTarget(self,edgeList):
        '''put people on critical edges into a list
        select infection targets from them'''
        candidates = []
        for edge in edgeList:
            candidates.append(edge[0][0])
            candidates.append(edge[0][1])
            candidates.append(edge[1][0])
            candidates.append(edge[1][1])
        temp = sorted(candidates,key = methodcaller("countNeighbor"),reverse=True)
        midIndex = len(temp)//5  # select a small number of highly connected nodes to infect
        for n in range(midIndex):
            target = temp[randint(0,4)]  # I used randint because many people have the same number of friends
            if target not in self.sortedCandidates:
                self.sortedCandidates.append(target)
                self.otherCountry.getNodes()[0].addNeighbor(target)
        return candidates,self.sortedCandidates

    def sort(self):
        '''sort people based on their connectivity'''
        toBeSorted = self.getNodes()
        alreadySorted = sorted(toBeSorted,key=methodcaller("countNeighbor"),reverse=True)
        return alreadySorted

    def infectTarget(self):
        '''initial infection for targets'''
        for target in self.sortedCandidates:
            target.infect()
            self.__infectedNodes.append(target)
        self.__roundsOfInfection += 1
        return self.__infectedNodes

    def spreadInfection(self):
        '''spreads infection from infected nodes to their neighbors'''
        self.dict = {}  # for GUI purposes
        temp = self.getInfectedNodes()[:]  # list of previously infected nodes
        if len(temp) == 0:  # when all nodes are healthy
            self.dict[self.otherCountry.getNodes()[0]] = self.sortedCandidates # for GUI
            return self.infectTarget()  # we infect the chosen targets
        for source in temp:  # if some nodes are already infected
            self.dict[source] = [] # GUI
            for neighbor in source.getNeighbor():
                if neighbor not in temp:
                    self.dict[source].append(neighbor)
                    if neighbor.isInfectable():
                        neighbor.infect() # infect the healthy neighbors
                        self.__infectedNodes.append(neighbor)
        self.__roundsOfInfection += 1  # update time
        if self.__roundsOfInfection > 2: # when rounds of infection reach 2
            self.inoculation() # start innoculation
            return self.__infectedNodes,self.__inoculatedNodes
        else:
            return self.__infectedNodes

    def getDict(self): return self.dict # for GUI

    def inoculation(self):
        '''innoculate healthy nodes that are one layer away from infected nodes'''
        temp = []
        for node in self.__infectedNodes: # get immediate neighbors of all infected nodes
            if node.hasNoNeighbor():
                continue
            for neighbor in node.getNeighbor():
                if neighbor.isInfectable():
                    temp.append(neighbor)
        for node in temp: # innoculate the neighbors of neighbors
            if node.hasNoNeighbor():
                continue
            for neighbor in node.getNeighbor():
                if neighbor.isInfectable():
                    neighbor.inoculate()
                    self.__inoculatedNodes.append(neighbor)
        return self.__inoculatedNodes

    def totalInfect(self, nodeList, time):
        '''another method of infection that operates n rounds continuously'''
        self.__levelsOfInfection = [[] for x in range(time)]
        for t in range(time):
            if t == 0:
                for node in nodeList:
                    if node.isInfectable():
                        node.infect()
                        self.__levelsOfInfection[t].append(node)
            elif t >= 1:
                for node in self.__levelsOfInfection[t - 1]:
                    if node.hasNoNeighbor():
                        continue
                    for neighbor in node.getNeighbor():
                        if neighbor.isInfectable():
                            self.__levelsOfInfection[t].append(neighbor)
                            neighbor.infect()
        return self.__levelsOfInfection
