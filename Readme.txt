In this network epidemiology simulation, the main tasks are: 1) create population graphs of two countries, find the highly connected clusters in each country, and split country into clusters 2) choose some people from a list of people on the critical edges, infect them. Then spread infection one layer outward each time. 
In the version “FinalVirusModel,” inoculation occurs automatically after two rounds of infection. 
In “SlightlyDiffVersion,” the moment of inoculation is decided by user via button-click. There is a time lag between the click and when inoculation takes effect. Thus, if user clicks “start infection” during that lag time, it is uncertain whether the virus or the inoculation would travels faster and take effect first. 
That’s the only different between “FinalVirusModel” and “SlightlyDiffVersion.”
In each folder there are three files: 
“allclasses.py” contains class Person, and class Graph (undirected). Each country’s population is one graph, with person objects directly being the nodes. The edges in graph is constructed from the each person’s list of friends. 
In “main.py,” we constructed a Simulation class which initializes all person and graph objects, and starts the action. For security, password needs to be set and entered before starting the simulation.
“RUNme.py” contains the GUI. Besides the obvious features that need no explanation, I just want to highlight: our display of infection spreading outwards involves animated virus moving from all infected people to their neighbors. We like this feature a lot.

