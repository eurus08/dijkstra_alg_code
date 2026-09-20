import networkx as nx
import matplotlib.pyplot as plt 
from graph_data import ABComplex_data
from dikjstra import dikjstra

def shift_pos(pos, amount):
    new_pos = {}
    for node, (x, y) in pos.items():
        new_pos[node] = (x + amount, y+amount)
    return new_pos


def build_graph(source, destination):
    colours = ['violet', 'orange', 'yellow', 'indigo', 'blue', 'cyan', 'brown', 'violet']

    # Create graph
    G = nx.Graph()


    # Add Nodes 
    nodes = [
        '1', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', '11', '12', '13', '14',
        '15', '16', '17', '18', '19', '20', '21',
        '22', '23', '24', '25', '26', '27', '28',
        '29', '30', '31', '32', '33', '34',
        'E1', 'E2', 'E3', 'E4'
    ]
    G.add_nodes_from(nodes)


    # Extract and add edges
    edges = []
    for node in ABComplex_data:
        for neighbour_node in ABComplex_data[node]:
            if ((node, neighbour_node) in edges) or ((neighbour_node, node) in edges):
                continue

            if node.startswith("E"):
                if neighbour_node.startswith("E") and int(neighbour_node[1:]) > int(node[1:]):
                        edges.append((node, neighbour_node))
            else:
                if neighbour_node.startswith("E"):                
                    edges.append((node, neighbour_node))
                else:
                    if int(neighbour_node) > int(node):
                        edges.append((node, neighbour_node))
    G.add_edges_from(edges)


    # Set positions
    position = {
        '1': (0,0), '2': (3,0), '3': (3,3), '4': (6,0), '5': (6,3), '6': (3,-3), '7': (6,-3),
        '8': (0.5,-0.5), '9': (3.5,-0.5), '10': (3.5,2.5), '11': (6.5, -0.5), 
        '12': (6.5,2.5), '13': (3.5,-3.5), '14': (6.5, -3.5), '15': (-0.5,-0.5),
        '16': (1,-1), '17': (4,-1), '18': (4,2), '19': (7,-1), '20': (7,2), '21': (4,-4), 
        '22': (7,-4), '23': (0,-1), '24': (1.5, -1.5), '25': (4.5,-1.5), '26': (4.5, 1.5), 
        '27': (7.5,-1.5), '28': (7.5, 1.5), '29': (4.5, -4.5), '30': (7.5,-4.5), 'E2': (0.5,-1.5),
        '31': (5,1), '32': (8,-2), '33': (8,1), '34': (8,-5), 'E1': (2,-2), 'E4': (5,-5), 'E3': (5,-2),
        'E5': (5.5, 0.5), 'E7': (8.5,0.5), 'E6': (8.5,-2.5), 'E8': (8.5,-5.5), 'E9': (9,-5),
    }

    # colour particular nodes
    exit_nodes = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']
    node_colors = {}

    for node in exit_nodes:
        node_colors[node] = 'lightgreen'

    node_colors[source] = 'orange'


    fig, ax = plt.subplots()
    # Draw graph outline
    nx.draw(G, position, with_labels=True, 
            node_color=[node_colors.get(node, 'lightblue') for node in G.nodes()], node_size=400)
    

    pos = [0.04, -0.04]
    shortest_path  = dikjstra(ABComplex_data, source, destination)
    highlighted_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
    nx.draw_networkx_edges(G, shift_pos(position, 0.04), edgelist= highlighted_edges, edge_color= 'orange', 
                           width=2, ax=ax, arrows=True, arrowstyle='->', arrowsize=20)


    red_patch = plt.Line2D([], [], color='violet', linewidth=3, label= 'Node'+source) 
    ax.legend(handles=[red_patch]) 

    # plt.savefig("./exit_1.png")
    plt.show()


