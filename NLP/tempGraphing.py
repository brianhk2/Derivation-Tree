from preProcessing import eqno
from preProcessing import output
from preProcessing import paraBreak
from preProcessing import exten
import networkx as nx
import matplotlib.pyplot as plt

# Class for Adjacency List for Directed Graphs
class directGraph:
    # Dictionary for directed graph representation
    def __init__(self):
        self.graph = {}

    # Function for adding directed edge
    def addEdge(self, node1, node2):
        # create an empty list for a key node
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []
        self.graph[node1].append(node2)

    # Print graph
    def printGraph(self):
        print(self.graph)

    # Retrieve all directed edges
    def getEdges(self, node):
        if node in self.graph:
            return self.graph[node]
        else:
            return []

# BFS function for removing repetitive edges. (Ex. a->b->c then edge a->c would be unecessary)
# Return true if there is already a existing path. Else, false
def bfs(src, dest, directedGraph):
    visited = [src]
    que = [src]
    while que:
        node = que.pop(0)
        if node == dest:
            return True
        for i in directedGraph.getEdges(node):
            if i not in visited:
                visited.append(i)
                que.append(i)
    return False

# Calculating Seed Equation: Finding number of incoming x outgoing nodes
def seedEq(directedGraph):
    max = 0
    eqNum = 'NULL'
    for key, value in directedGraph.graph.items():
        tempMax = 0
        tempMax += len(value)
        for key1, value1 in directedGraph.graph.items():
            if key1 == key:
                continue
            else:
                for i in value1:
                    if key == i:
                        tempMax += 1
        if max < tempMax:
            max = tempMax
            eqNum = key
    print('Seed Equation: ', eqNum)

# Graphing
counter = 0                                                 # Counting number of elements between intervals
adjList = directGraph()                                     # Create Adjacency List Object            
G = nx.DiGraph()                                            # Create Directed Graph

for i in range(len(eqno)):
    if eqno[i][0] == 1:                                         # If scanning through paragraph before first equation, skip since no prior equations for linkage
        continue
    for idx in range(eqno[i][0]-1):                                 # Scanning for possible edges ex. 1 to 3; 1 to 7 (-1 since not looking for current equation number)
        counter = 0                                                 # Counter for number of words between paragraphs/equations
        eqNum = str(eqno[idx][0])                                   # eqNum = current possible edge
        for j in range (paraBreak[i][1]+1, eqno[i][1]-1):           # Iterating through the strings between start and actual equation ex. 433 to 573; 573 to 643
            counter += 1                                            # Increment word counter                                            
            if (j >= 2 and eqNum in output[j]) and ('equationlink' in output[j-1]) and ('Fig' not in output[j-2]):         # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'equationlink' is NOT in element before that                         
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:         # If there is no path between the two edges,
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
        # If number of words between equations is less then arbitrary number (20) 
        # and we are on last iteration of equations, 
        if counter < 20 and (idx+1 == eqno[i][0]-1):                 
            adjList.addEdge(eqno[idx][0], eqno[i][0])                       # Set manual edge between two equations. Ex. 6->7, 3->4
            G.add_edge(eqno[idx][0], eqno[i][0])                            # Set manual edge between two equations. Ex. 6->7, 3->4
        for j in range (eqno[i][1]+1, exten[i][1]):                 # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            if (j >= 2 and eqNum in output[j]) and ('equationlink' in output[j-1]) and ('Fig' not in output[j-2]):          # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'equationlink' is NOT in element before that                         
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:         # If there is no path between the two edges,
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
nx.draw_shell(G, with_labels = True)                                        # Taking graph G, add labels
plt.savefig("DerivationTree.png")                                           # Output onto DerivationTree.png
seedEq(adjList)

# Debugging 
# adjList.printGraph()

# Issues with logic:    
#               - Increase paragraph intervals to one more after each equation (I do not feel ok with this) (Still really good idea since ive seen several examples already, but needs tweaking)
#               - Creating edges between equations with few words between them (I also do not feel ok with this) ex. 0907.2720
#               - Ideas for miscellaneous edges: Incorporating grammar (transition words) 
#               - If paragraph before equation has capital letter with no period before, equationlink, Fig, eq, parabreak then equation is of important has a name, so shouldnt be any incoming edge
# TODO LIST:    - Think of ideas for finding identical texts from conclusion to different areas of text.
#               - Figure out how to store mathML components 
#                 (Create array of mathML componenets and run some sort of algorithm that gives similarity levels. Edit graph so that this array of mathML is part of the class)
#                 (Look at 0907.2744)
#                 (Look over website with different strategies)
#               - Edge priority levels: Is there reference to author?/is there an equation directly linked? (same priority level) If not mve onto finding similar texts from other equations ex. 0907.2648 and ex 0907.2794
#               - Find longest path in DAG by dynamic programming to figure out root of tree
#               - Seed equation: Conclusion should hold analysis ONLY so find see equation based on outgoing directed edges?? Also, if i take out equation which causes most subgraphs???
#               - Write down all logic/bugs fixed/how i fixed them
#               - overleaf
# Questions:    - Write Python Script for parsing through corpus and finding papers that have >= 10 equations
#               - Should i figure out how i should start formulating paper? Assumptions that I made, intro conclusion, etc
#               - Can I assume there is a reference to an equation ex 0907.2798
