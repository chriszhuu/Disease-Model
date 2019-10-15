from allclasses import Person,Graph
from random import randint
import hashlib


class Simulation: # this class starts action and stores variables
    def __init__(self):
        self.populationA = Graph()
        self.populationB = Graph()
        self.curState = ''
        self.Acluster = None
        self.Bcluster = None
        self.Atargetlist = None
        self.Btargetlist = None
        self.__password = ''

    def setPassword(self):
        '''set seure password for this program'''
        pwd = input(">>> Please SET PASSWORD for this program:")
        pwd1 = pwd.encode()
        myhash = hashlib.sha256(pwd1).hexdigest()
        self.password = myhash
        print(">>> Your password has been set!\n")

    def checkPassword(self, test):
        myhash = hashlib.sha256(test).hexdigest()
        return self.password == myhash

    def secureStart(self):
        '''start simulation after entering the correct password'''
        self.setPassword()
        test = input(">>> Please ENTER PASSWORD to run this program:")
        test1 = test.encode()
        if self.checkPassword(test1):
            print("\n>>> SUCCESS!\n")
            self.startSimulation()
        else:
            print(">>> The password you entered is not valid, please enter again...")
            self.enterPwdAgain()

    def enterPwdAgain(self):
        test = input(">>> Please ENTER PASSWORD to run this program:")
        test1 = test.encode()
        if self.checkPassword(test1):
            print("\n>>> SUCCESS!\n")
            self.startSimulation()
        else:
            print(">>> The password you entered is not valid, please enter again...")
            self.enterPwdAgain()

    def recordState(self):
        '''records information of populations'''
        self.curState += self.populationA.getName()+' and '+self.populationB.getName()
        self.curState += '\n'+str(self.populationA)
        self.curState += str(self.populationB)
        return self.curState

    def showState(self):
        '''shows information of populations'''
        self.recordState()
        print(self.curState)

    def initialize(self):
        '''create person objects and graph objects'''
        personFile = open("person and friend.txt","r")
        personData = personFile.readlines()
        # create person objects and add them to their country
        for aline in personData:
            values = aline.split(",")
            if values[1] == "A":
                self.populationA.addNode(Person(values[0],"Lilliput"))
            elif values[1] == "B":
                self.populationB.addNode(Person(values[0],"Brobdingnag"))
        self.populationA.setName("Lilliput")
        self.populationB.setName("Brobdingnag")
        self.populationA.setOtherCountry(self.populationB)
        self.populationB.setOtherCountry(self.populationA)
        # assign random age to each person
        for person in self.populationA.getNodes():
            person.setAge(randint(5,95))
        for person in self.populationB.getNodes():
            person.setAge(randint(5,95))

        # make each person's neighbors into person objects
        for aline in personData:
            values = aline.split(",")
            if values[1] == "A":
                for person in self.populationA.getNodes():
                    if values[0] == person.getName():
                        me = person
                        neighborList = values[2].split()
                        for neighbor in neighborList:
                            for person in self.populationA.getNodes():
                                if neighbor == person.getName():
                                    me.addNeighbor(person)
            elif values[1] == "B":
                for person in self.populationB.getNodes():
                    if values[0] == person.getName():
                        me = person
                        neighborList = values[2].split()
                        for neighbor in neighborList:
                            for person in self.populationB.getNodes():
                                if neighbor == person.getName():
                                    me.addNeighbor(person)

    def startSimulation(self):
        '''complete all the population graphs, identify critical edges in each,
        split each graph into clusters, identify and infect targeted people'''
        self.initialize()
        self.populationA.createEdges()
        self.populationB.createEdges()
        self.showState()
        AcriticalEdges = self.populationA.findCluster()
        BcriticalEdges = self.populationB.findCluster()
        self.Acluster = self.populationA.splitGraph(AcriticalEdges)
        self.Bcluster = self.populationB.splitGraph(BcriticalEdges)

        self.Atargetlist,self.Arefinedlist = self.populationA.findTarget(AcriticalEdges)
        self.Btargetlist,self.Brefinedlist = self.populationB.findTarget(BcriticalEdges)

    def spreadInfection(self):
        '''spread infection one layer outward'''
        listA = self.populationA.spreadInfection()
        listB = self.populationB.spreadInfection()
        print(listA)
        print(listB)
        return listA,listB

    def getDict(self): return self.populationA.getDict(),self.populationB.getDict()

    def inoculation(self):
        self.populationA.inoculation()
        self.populationB.inoculation()
        return self.populationA.getInoculatedNodes(),self.populationB.getInoculatedNodes()


