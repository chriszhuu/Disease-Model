import tkinter as gwaphics
from main import Simulation
import math

class ButtonThing:
    def __init__(self,master,app):
        self.master = master
        self.app = app
        master.title("Infection and Inoculation")
        self.frame = gwaphics.Frame(master)

        self.findCritical = gwaphics.Button(master,text="Find Critical",command=self.app.changeColor)
        self.findCritical.pack(side = "top")

        self.startInfection_button = gwaphics.Button(master,text="Start Infection", command=app.infectPeople) # this can call a method which is infect
        self.startInfection_button.pack(side = "top")

        self.close_button = gwaphics.Button(master, text="Close", command=master.quit)
        self.close_button.pack(side = "top")
        self.frame.pack(side="left")


class graphOval:
    def __init__(self,canvas,*args,**kwargs):
        self.master = root
        self.canvas = canvas
        self.oval = self.canvas.create_oval(*args, **kwargs)
        self.deltaX = None
        self.deltaY = None

    def setDelta(self,x,y):
        self.deltaX = x
        self.deltaY = y

    def moveTo(self):
        self.canvas.move(self.oval, self.deltaX, self.deltaY)

class graphInfo:
    def __init__(self,canvas,*args,**kwargs):
        self.canvas = canvas
        self.Info = canvas.create_text(*args, **kwargs)

class graphArc:
    def __init__(self,canvas,*args,**kwargs):
        self.canvas = canvas
        self.Arc = canvas.create_arc(*args,**kwargs)

class connectPoint:
    def __init__(self,canvas,*args,**kwargs):
        self.canvas = canvas
        self.line = canvas.create_line(*args,**kwargs)

class coordStuff:
    def __init__(self,master,x,y,oval):
        self.master = master
        self.x0 = x
        self.y0 = y
        self.oval = oval
        self.x1 = None
        self.y1 = None
        self.count = 0

    def setNewCoord(self,x,y):
        self.x1 = x
        self.y1 = y
        deltaX = (self.x1 - self.x0) / 10
        deltaY = (self.y1 - self.y0) / 10
        self.oval.setDelta(deltaX, deltaY)

    def moveOval(self):
        if self.count < 10:
            self.oval.moveTo()
            self.master.after(100, self.moveOval)
            self.count += 1
        else: return


class Application:
    def __init__(self,master):
        self.master = master
        self.criticalColor = "red"
        self.normalColor = "green"
        self.infectColor = "orange"
        self.canvas = None
        self.virusList = None
        self.targetA = None
        self.targetB = None
        self.clusterA = None
        self.clusterB = None
        self.infectedListA = None
        self.infectedListB = None
        self.inoculateA = None
        self.inoculateB = None
        self.time = 0


    def createCanvas(self):
        self.canvas = gwaphics.Canvas(root, width=1500, height=600,
                                      background="white")  # when creating canvas, the first is root
        self.canvas.pack(fill="both", expand=True)

    def graphSign(self):
        graphOval(self.canvas, 1100, 30, 1130, 60, outline="white", fill="red")
        graphInfo(self.canvas, 1200, 40, fill='black', text="           Critical Connection", font=("Purisa", 17))
        graphOval(self.canvas, 1100, 80, 1130, 110, outline="white", fill="green")
        graphInfo(self.canvas, 1180, 90, fill='black', text="Healthy", font=("Purisa", 17))
        graphOval(self.canvas, 1100, 130, 1130, 160, outline="white", fill="orange")
        graphInfo(self.canvas, 1180, 140, fill='black', text=" Infected", font=("Purisa", 17))
        graphOval(self.canvas, 1102, 180, 1132, 210, outline="white", fill="blue")
        graphInfo(self.canvas, 1180, 190, fill='black', text="     Inoculated", font=("Purisa", 17))
        graphOval(self.canvas, 1115, 230, 1125, 240, outline="white", fill="red")
        graphInfo(self.canvas, 1170, 235, fill='black', text="Virus", font=("Purisa", 17))
        graphInfo(self.canvas, 600, 30, fill='black', text="Lilliput", font=("Purisa", 20))
        graphInfo(self.canvas, 600, 350, fill='black', text="Brobdingnag", font=("Purisa", 20))


    def setTarget(self,list):
        self.targetA = list[0]
        self.targetB = list[1]

    def setInfectedList(self,listA,listB):
        self.infectedListA = listA
        self.infectedListB = listB

    def polarTOcart(self,rho, phi):  # phi is angle
        x = rho * math.cos(phi)
        y = rho * math.sin(phi)
        return x, y

    def drawCluster(self,clusterList, i, j):  # i,j is the center of the cluster of people
        for cluster in clusterList:
            rho = 120
            phi = 0
            clusterNode = cluster.sort()
            person = clusterNode[0]
            person.setLocation(i, j)
            graphOval(self.canvas, i, j, i + 30, j + 30, outline="white", fill="green")
            graphInfo(self.canvas, i + 20, j + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))
            for x in range(1, len(clusterNode)):
                person = clusterNode[x]
                split = 2 * math.pi / (len(cluster.getNodes()) - 1)
                phi += split
                x, y = self.polarTOcart(rho, phi)
                x += i
                y += j
                person.setLocation(x, y)
                graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill="green")
                graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))
            i += 300

    def changeColor(self):
        for person in self.targetA:
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill="red")
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))
        for person in self.targetB:
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill="red")
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))


    def connectPeople(self, population):
        for person in population.getNodes():
            x0, y0 = person.getLocation()
            for friend in person.getNeighbor():
                x1, y1 = friend.getLocation()
                connectPoint(self.canvas, x0 + 15, y0 + 15, x1 + 15, y1 + 15, fill="blue")


    def moveVirus(self,A,B):
        for k, v in A.items():
            for m in range(len(v)):
                x, y = k.getLocation()
                oval = graphOval(self.canvas, x, y, x + 10, y + 10, outline="white", fill="red")
                coords = coordStuff(self.master,x, y, oval)
                x, y = v[m].getLocation()
                coords.setNewCoord(x,y)
                coords.moveOval()
        for k, v in B.items():
            for m in range(len(v)):
                x, y = k.getLocation()
                oval = graphOval(self.canvas, x, y, x + 10, y + 10, outline="white", fill="red")
                coords = coordStuff(self.master,x, y, oval)
                x, y = v[m].getLocation()
                coords.setNewCoord(x,y)
                coords.moveOval()

    def subInfect(self):
        for person in self.infectedListA:  # should add a index
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill=self.infectColor)
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))
        for person in self.infectedListB:  # should add a index
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill=self.infectColor)
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))

    def subInoculate(self):
        for person in self.inoculateA:
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill="blue")
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))
        for person in self.inoculateB:
            x, y = person.getLocation()
            graphOval(self.canvas, x, y, x + 30, y + 30, outline="white", fill="blue")
            graphInfo(self.canvas, x + 20, y + 20, fill='black', text=str(person.getName()), font=("Purisa", 10))


    def infectPeople(self):
        self.time += 1
        if self.time > 2:
            totalA, totalB = simulate.spreadInfection()
            self.infectedListA,self.inoculateA = totalA
            self.infectedListB,self.inoculateB = totalB
            A,B = simulate.getDict()
            self.moveVirus(A,B)
            self.master.after(1000,self.subInfect)
            self.master.after(1500,self.subInoculate)
            return

        self.infectedListA, self.infectedListB = simulate.spreadInfection()
        A, B = simulate.getDict()
        self.master.after(1000, self.subInfect)
        self.moveVirus(A, B)


# create button that does startsSimulation
# use self.blahblah as variables
simulate = Simulation()
simulate.secureStart()
clusterA = simulate.populationA.getClusters()
clusterB = simulate.populationB.getClusters()
populationA = simulate.populationA
populationB = simulate.populationB
targetA = simulate.Atargetlist
targetB = simulate.Btargetlist
infectListA = populationA.getLevelsOfInfection()
infectListB = populationB.getLevelsOfInfection()

root = gwaphics.Tk()
app = Application(root)
ButtonThing(root,app)
app.createCanvas()
app.graphSign()
app.setTarget([targetA,targetB])
app.setInfectedList(infectListA,infectListB)
app.drawCluster(clusterA,150,160)
app.drawCluster(clusterB,150,500)
app.connectPeople(populationA)
app.connectPeople(populationB)

root.mainloop()