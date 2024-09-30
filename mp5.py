# submitted.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# submitted should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi)
import queue
def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    #TODO: Implement bfs function
    path = []
    explored = set()
    root = dict()
    start = maze.start
    end = maze.waypoints[0]
    q = queue.Queue()
    q.put(start)
    explored.add(start)
    while not q.empty():
        point = q.get()
        if point == end:
            path = []
            
        neighbors = maze.neighbors(point[0], point[1])
        for i in range(len(neighbors)):
            if neighbors[i] not in explored and maze.navigable(neighbors[i][0], neighbors[i][1]) :
                root[neighbors[i]] = point
                explored.add(neighbors[i])
                q.put(neighbors[i])
                
    
    path.append(end)
    a = end
    while a != start:
        a = root[a]
        path.append(a)
                
    path.reverse()
    return path

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    #TODO: Implement astar_single
    
    path = []
    q = queue.PriorityQueue()
    end = maze.waypoints[0]
    explored = set()
    root = dict()
   
    start = maze.start
    explored.add(start)
    q1 = (abs(start[0] - end[0]) + abs(start[1] - end[1]) + 0, 0, start)
    q.put(q1)
    while not q.empty():
        point = q.get()
        if point[2] == end:
            break;
        neighbors = maze.neighbors(point[2][0], point[2][1])
        for i in range(len(neighbors)):
            if neighbors[i] not in explored and maze.navigable(neighbors[i][0], neighbors[i][1]) :
                root[neighbors[i]] = point[2]
                explored.add(neighbors[i]) 
                g = abs(neighbors[i][0] - start[0]) + abs(neighbors[i][1] - start[1])
                h = abs(neighbors[i][0] - end[0]) + abs(neighbors[i][1] - end[1])
                q.put((h + point[1] + 1, point[1]+1, neighbors[i]))
                

    path.append(end)
    a = end
    while a != start:
        a = root[a]
        path.append(a)
                
    path.reverse()
    return path

# This function is for Extra Credits, please begin this part after finishing previous two functions
def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    
    path = []
    start = maze.start
    q = queue.PriorityQeue()
    root = dict()
    
    

    return []
