from pyrat import *
import numpy
import heapq
import template_2players as opponent
from typing import Union, List, Dict, Tuple,Any

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


pieces=[]
moves=[]
eaten_pieces=[]
moving=False
meta_graph={}
best_paths={}
testing={}
path_to_new_target=[]
is_following_me=0
is_matched=0
consider_as_eaten=[]
tempted=tuple()
#Function to create an empty priority queue
def _create_structure():
        return []
   #Function to add an element to the priority queue
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


# Dijkstra
def dijkstra(
    source: int, graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]]
) -> Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
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

####################################################Finding the closest piece of cheese#################################################################################################

def give_score ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                 current_vertex: int,
                 targets:        List[int]
               ) ->              Tuple[List[float], Dict[int, Union[None, int]]]:
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
    
    n=len(vertices)
    scores,routing_table=give_score(graph,initial_vertex,vertices)
    next=min(scores)
    route=find_route(routing_table,initial_vertex,next)
    return next,route  
###########################################################definition de min##########################################################################################
def min(my_dict):
    liste=list(my_dict.values())
    liste=sorted(liste)
    l=liste[0]
    for cle in my_dict:
        if my_dict[cle]==l:
            vertice=cle
    return vertice
#####################################################################################################################################################
def find_route ( routing_table: Dict[int, Union[None, int]],
                 source:        int,
                 target:        int
               ) ->             List[int]:
    
    L=[]
    element=target
    while element != source :
        L.append(element)
        element=routing_table[element]
    L.append(element)
    L.reverse()
    return(L)       
###################################################### GOdef locations_to_actions###################################################################################
def locations_to_actions ( locations:  List[int],
                           maze_width: int
                         ) ->          List[str]: 
    actions = []
    for i in range(len(locations) - 1):
        action = locations_to_action(locations[i], locations[i + 1], maze_width)
        actions.append(action)
    return actions
#####################################################################################################################################################
def updatepieces (metaGraph,location):
    test=False
    if location in metaGraph :
        eaten_pieces.append(location)
        test=True
    return eaten_pieces,test
def graph_to_metagraph ( graph:    Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                         vertices: List[int]
                       ) ->        Tuple[numpy.ndarray, Dict[int, Dict[int, Union[None, int]]]]:
    complete_graph = {}
    routing_tables = {}
    for vertice in vertices:
        complete_graph[vertice] = {}
        routing_table_loc,distance = dijkstra(vertice, graph)
        routing_tables[vertice] = routing_table_loc
        for nei in vertices:
            if nei != vertice:
                complete_graph[vertice][nei] = distance[nei]
    

    return complete_graph, routing_tables
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

    # [TODO] Write your preprocessing code here
    global meta_graph, best_paths,pieces
    pieces=cheese[:]
    meta_graph,best_paths=graph_to_metagraph (maze,cheese)
    memory.nb0_cheese=len(cheese)
    memory.path_taken=[]
    pass
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

    # [TODO] Write your turn code here and do not forget to return a possible action
    global meta_graph,eaten_pieces,testing,path_to_new_target,pieces,is_following_me
    global moving
    global tempted,is_matched
    # Si l'ennemi mange une pièce de fromage et que je n'y suis pas, on la compte
    eaten_pieces,test = updatepieces(meta_graph,player_locations['opponent'])


    # Si une pièce de fromage a été mangée, on la compte
    eaten_pieces,test = updatepieces (meta_graph,player_locations[name])
    listcheese=cheese


    if moving: 
        if (not path_to_new_target) or (test and testing[-1]==eaten_pieces[-1]) or (is_following_me==3) :
                is_following_me=0
                moving = False
    if not moving:
        opponent_score= memory.nb0_cheese-len(cheese)-player_scores[name]
        if is_matched==3 and opponent_score>player_scores[name]:
            is_matched=0
            listcheese.remove(tempted)
            new_target,path_to_new_target=greedy(maze,player_locations[name],listcheese)
            moving=True
            testing=path_to_new_target
            path_to_new_target.pop(0)
        else:
            new_target,path_to_new_target=greedy(maze,player_locations[name],listcheese)
            tempted=new_target
            testing=path_to_new_target
            path_to_new_target.pop(0)
            moving = True
            if len(path_to_new_target)>=3:
                if player_locations['opponent'] in [path_to_new_target[1],path_to_new_target[2]]:
                    is_following_me+=1
            else:
                is_following_me=3
            if player_locations['opponent']==player_locations[name]:
                is_matched+=1
    next_location = path_to_new_target.pop(0)
    UDRL=locations_to_action(player_locations[name], next_location, maze_width)
    memory.path_taken.append(player_locations[name])
    return UDRL

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################
if __name__ == "__main__":
   
    # Map the functions to the character
    players = [{"name": "JOHN DOE", "team": "You", "skin": "rat", "preprocessing_function": preprocessing, "turn_function": turn},
               {"name": "opponent", "team": "Opponent", "skin": "python", "preprocessing_function": opponent.preprocessing if "preprocessing" in dir(opponent) else None, "turn_function": opponent.turn}]
    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage":40.0,
              "nb_cheese": 20}
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()    
    # Show statistics
    
#####################################################################################################################################################
#####################################################################################################################################################
