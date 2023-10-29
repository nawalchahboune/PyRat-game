#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    Contrary to the "template.py" file, there are 2 players here.
    Here, opponent is "random_3.py".
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *
from typing import Union, List, Dict, Tuple
import numpy
import heapq
def get_neighbors ( vertex: int,
                    graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]]
                  ) ->      List[int]:
   
    # If "maze_representation" option is set to "dictionary"
    if isinstance(graph, dict):
        neighbors = list(graph[vertex].keys())
    # If "maze_representation" option is set to "matrix"
    elif isinstance(graph, numpy.ndarray):
        neighbors = graph[vertex].nonzero()[0].tolist()
    
    # Unhandled data type
    else:
        raise Exception("Unhandled graph type", type(graph))
    
    # Done
    return neighbors
def locations_to_action ( source:     int,
                          target:     int,
                          maze_width: int
                        ) ->          str: 
    # Convert indices in row, col pairs
    source_row = source // maze_width
    source_col = source % maze_width
    target_row = target // maze_width
    target_col = target % maze_width
    
    # Check difference to get direction
    difference = (target_row - source_row, target_col - source_col)
    if difference == (0, 0):
        action = "nothing"
    elif difference == (0, -1):
        action = "west"
    elif difference == (0, 1):
        action = "east"
    elif difference == (1, 0):
        action = "south"
    elif difference == (-1, 0):
        action = "north"
    else:
        raise Exception("Impossible move from", source, "to", target)
    return action


 # Function to create an empty priority queue
# External imports 
# [TODO] Put all your standard imports (numpy, random, os, heapq...) here

# Previously developed functions
# [TODO] Put imports of functions you have developed in previous lessons here
import template_2players as opponent

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################
####################################################Finding the closest piece of cheese#################################################################################################

def give_score ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                 current_vertex: int,
                 targets:        List[int]
               ) ->              Tuple[List[float], Dict[int, Union[None, int]]]:
    """
        Function that associates a score to each target.
        In:
            * graph:          Graph containing the vertices.
            * current_vertex: Current location of the player in the maze.
            
        Out:
            * scores:        Scores given to the targets.
            * routing_table: Routing table obtained from the current vertex.
    """
    routing_table,distances=dijkstra(current_vertex,graph)
    scores={}
    for vertex in targets:
        if vertex in distances:
                scores[vertex]=distances[vertex]
    return scores,routing_table
###########################################################Finding the closest piece of cheese##########################################################################################
def greedy ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             initial_vertex: int,
             vertices:       List[int]
           ) ->              List[int]:
    """
        Greedy algorithm that goes to the score maximizer in a loop.
        In:
            * graph:          Graph containing the vertices.
            * initial_vertex: Initial location of the player in the maze.
            * vertices:       Vertices to visit with the greedy heuristic.
        Out:
            * route: Route to follow to perform the path through all vertices.
    """
    route=[]
    n=len(vertices)
    for i in range(n):
        scores,routing_table=give_score(graph,initial_vertex,vertices)
        next=min(scores)
        route=route+find_route(routing_table,initial_vertex,next)
        initial_vertex=next
        vertices.remove(next)
    return route
def find_route ( routing_table: Dict[int, Union[None, int]],
                 source:        int,
                 target:        int
               ) ->             List[int]:
    """
        Function to return a sequence of locations using a provided routing table.
        In:
            * routing_table: Routing table as obtained by the traversal.
            * source:        Vertex from which we start the route (should be the one matching the routing table).
            * target:        Target to reach using the routing table.
        Out:
            * route: Sequence of locations to reach the target from the source, as perfomed in the traversal.
    """
    
    L=[]
    element=target
    while element != source :
        L.append(element)
        element=routing_table[element]
    L.append(element)
    L.reverse()
    return(L)
# Dijkstra
def dijkstra(
    source: int, graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]]
) -> Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
    Dijkstra's algorithm is a particular traversal where vertices are explored in an order that is proportional to the distance to the source vertex.
    In:
        * source: Vertex from which to start the traversal.
        * graph:  Graph on which to perform the traversal.
    Out:
        * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
        * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """

    # Function to create an empty priority queue
    def create_structure():
        priority_queue = []
        return priority_queue

    # Function to add an element to the priority queue
    def push_to_structure(structure, element):
        heapq.heappush(structure, element)

    # Function to extract an element from the priority queue
    def pop_from_structure(structure):
        return heapq.heappop(structure)

    # Perform the traversal
    distances_to_explored_vertices, routing_table = traversal(
        source, graph, create_structure, push_to_structure, pop_from_structure
    )
    
    return routing_table,distances_to_explored_vertices
def traversal(
    source: int,
    graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
    create_structure: Callable[[], Any],
    push_to_structure: Callable[[Any, Tuple[int, int, int]], None],
    pop_from_structure: Callable[[Any], Tuple[int, int, int]],
) -> Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    # We define a flag to check whether all elements have been visited
    finish = True
    # First we create a priority queue

    queuing_structure = create_structure()
    # Add the starting vertex with None as parent
    push_to_structure(queuing_structure, (0, (source, None)))
    # Initialize the outputs
    explored_vertices = []
    routing_table = {}
    distances_to_explored_vertices = {None: -1, source: 0}
    # Iterate while some vertices remain
    while len(queuing_structure) > 0:
        # Checking if all vertices were visited
        for element in queuing_structure:
            if element[0] not in explored_vertices:
                finish = False
        if finish:
            break
        # This will return the next vertex to be examined, and the choice of queuing structure will change the resulting order
        detail, (current_vertex, parent) = pop_from_structure(queuing_structure)

        # Tests whether the current vertex is in the list of explored vertices
        if current_vertex not in explored_vertices:
            # Mark the current_vertex as explored
            explored_vertices.append(current_vertex)
            if current_vertex != source:
                distances_to_explored_vertices[current_vertex] = (
                    distances_to_explored_vertices[parent]
                    + graph[parent][current_vertex]
                )
            # Update the routing table accordingly
            routing_table[current_vertex] = parent

            # Examine neighbors of the current vertex
            for neighbor in get_neighbors(current_vertex, graph):
                # We push all unexplored neighbors to the queue
                if neighbor not in explored_vertices:
                    push_to_structure(
                        queuing_structure,
                        (
                            distances_to_explored_vertices[current_vertex]
                            + graph[current_vertex][neighbor],
                            (neighbor, current_vertex),
                        ),
                    )
    distances_to_explored_vertices.pop(None)
    return (distances_to_explored_vertices, routing_table)
#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################

def preprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                    maze_width:       int,
                    maze_height:      int,
                    name:             str,
                    teams:            Dict[str, List[str]],
                    player_locations: Dict[str, int],
                    cheese:           List[int],
                    possible_actions: List[str],
                    memory:           threading.local
                  ) ->                None:

    """
        This function is called once at the beginning of the game.
        It is typically given more time than the turn function, to perform complex computations.
        Store the results of these computations in the provided memory to reuse them later during turns.
        To do so, you can crete entries in the memory dictionary as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    # [TODO] Write your preprocessing code here
    pass
    
#####################################################################################################################################################
######################################################### EXECUTED AT EACH TURN OF THE GAME #########################################################
#####################################################################################################################################################

def turn ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
           maze_width:       int,
           maze_height:      int,
           name:             str,
           teams:            Dict[str, List[str]],
           player_locations: Dict[str, int],
           player_scores:    Dict[str, float],
           player_muds:      Dict[str, Dict[str, Union[None, int]]],
           cheese:           List[int],
           possible_actions: List[str],
           memory:           threading.local
         ) ->                str:

    """
        This function is called at every turn of the game and should return an action within the set of possible actions.
        You can access the memory you stored during the preprocessing function by doing memory.my_key.
        You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * action: One of the possible actions, as given in possible_actions.
    """
    route = greedy(maze,player_locations[name],cheese)
    action = locations_to_action(player_locations[name], route[1], maze_width)
    return action

#####################################################################################################################################################
######################################################## EXECUTED ONCE AT THE END OF THE GAME #######################################################
#####################################################################################################################################################

def postprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                     maze_width:       int,
                     maze_height:      int,
                     name:             str,
                     teams:            Dict[str, List[str]],
                     player_locations: Dict[str, int],
                     player_scores:    Dict[str, float],
                     player_muds:      Dict[str, Dict[str, Union[None, int]]],
                     cheese:           List[int],
                     possible_actions: List[str],
                     memory:           threading.local,
                     stats:            Dict[str, Any],
                   ) ->                None:

    """
        This function is called once at the end of the game.
        It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    # [TODO] Write your postprocessing code here
    pass
    
#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "Template 2", "team": "You", "skin": "rat", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing},
               {"name": "greedy1", "team": "Opponent", "skin": "python", "preprocessing_function": opponent.preprocessing if "preprocessing" in dir(opponent) else None, "turn_function": opponent.turn, "postprocessing_function": postprocessing if "postprocessing" in dir(opponent) else None}]

    # Customize the game elements
    config = {"maze_width": 10,
              "maze_height": 8,
              "mud_percentage": 0.0,
              "nb_cheese": 5}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics


#####################################################################################################################################################
#####################################################################################################################################################
